"""
Market Intelligence & Machine Learning Analytics Engine for Etsy Digital Products.

Aggregates keyword research insights (search volume, competition levels, demand/opportunity
scores), evaluates store-level performance, and applies K-Means Clustering (with Silhouette
Score optimization and PCA 2D projection) + anomaly detection to identify trending digital
products with high demand and low competition.
"""

from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from scraper import EtsyListing, NICHE_ARCHETYPES

logger = logging.getLogger(__name__)


class EtsyMarketAnalyzer:
    """Performs keyword aggregation, store benchmarking, and ML niche clustering."""

    def __init__(self, listings: List[EtsyListing]):
        self.raw_df = pd.DataFrame([item.to_dict() for item in listings])
        self.clean_df = self._clean_and_validate(self.raw_df)

    @staticmethod
    def _clean_and_validate(df: pd.DataFrame) -> pd.DataFrame:
        """
        Validates schema, inspects missing/null values, and imputes contextually
        appropriate values without unnecessarily dropping valid listings.
        """
        if df.empty:
            return df.copy()

        cleaned = df.copy()

        # Check and handle missing values per ml-best-practices
        numeric_defaults = {
            "price": cleaned["price"].median() if "price" in cleaned else 12.99,
            "original_price": cleaned["price"].median() if "price" in cleaned else 12.99,
            "discount_pct": 0.0,
            "rating": 4.80,
            "reviews_count": 0,
            "estimated_sales": 1,
            "estimated_revenue": 12.99,
            "total_keyword_listings": 10000,
            "in_carts_count": 0,
            "recent_views_24h": 0,
        }
        for col, default_val in numeric_defaults.items():
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce").fillna(default_val)

        # Ensure positive prices and non-negative counts
        cleaned["price"] = cleaned["price"].clip(lower=0.99)
        cleaned["reviews_count"] = cleaned["reviews_count"].clip(lower=0).astype(int)
        cleaned["estimated_sales"] = cleaned["estimated_sales"].clip(lower=1).astype(int)
        cleaned["estimated_revenue"] = (cleaned["estimated_sales"] * cleaned["price"]).round(2)

        return cleaned

    def aggregate_keyword_insights(self) -> pd.DataFrame:
        """
        Aggregates 10-page listing data by keyword to compute search volume, competition
        levels, store concentration, demand scores, and growth potential scores.
        """
        df = self.clean_df
        if df.empty:
            return pd.DataFrame()

        records: List[Dict[str, Any]] = []
        for keyword, grp in df.groupby("keyword", sort=False):
            arch = NICHE_ARCHETYPES.get(keyword.lower(), {})
            total_competing = int(grp["total_keyword_listings"].median())
            scraped_count = len(grp)

            avg_price = float(grp["price"].mean())
            median_price = float(grp["price"].median())
            q75, q25 = np.percentile(grp["price"], [75, 25])
            price_iqr = float(q75 - q25)

            total_reviews = int(grp["reviews_count"].sum())
            avg_reviews = float(grp["reviews_count"].mean())
            total_sales = int(grp["estimated_sales"].sum())
            avg_sales = float(grp["estimated_sales"].mean())
            total_revenue = float(grp["estimated_revenue"].sum())
            avg_revenue_per_listing = float(grp["estimated_revenue"].mean())

            bestseller_rate = float(grp["is_bestseller"].mean() * 100.0)
            popular_now_rate = float(grp["is_popular_now"].mean() * 100.0)
            star_seller_rate = float(grp["is_star_seller"].mean() * 100.0)
            ad_saturation_pct = float(grp["is_ad"].mean() * 100.0)
            active_cart_rate = float((grp["in_carts_count"] > 0).mean() * 100.0)
            avg_views_24h = float(grp["recent_views_24h"].mean())

            # Top-5 store sales share (measures market monopoly / barrier to entry)
            store_sales = grp.groupby("shop_name")["estimated_sales"].sum().sort_values(ascending=False)
            top5_share_pct = float(store_sales.head(5).sum() / max(1, total_sales) * 100.0)
            unique_stores = int(grp["shop_name"].nunique())

            # Estimated Monthly Search Volume & YoY Trend
            # Combines baseline search volume index with observed active cart & velocity signals
            base_search_vol = arch.get(
                "monthly_search_vol_base",
                int(min(120000, max(8000, avg_sales * 4.2 + avg_views_24h * 850))),
            )
            velocity_factor = 0.85 + 0.15 * ((bestseller_rate + popular_now_rate) / 35.0)
            est_monthly_search_volume = int(round(base_search_vol * velocity_factor, -2))
            yoy_trend_pct = float(arch.get("trend_YoY_pct", round((popular_now_rate - 12.0) * 2.8, 1)))
            category = arch.get("category", "Digital Downloads")

            records.append(
                {
                    "keyword": keyword,
                    "category": category,
                    "scraped_listings": scraped_count,
                    "pages_scraped": int(grp["page"].nunique()),
                    "est_monthly_search_volume": est_monthly_search_volume,
                    "yoy_search_trend_pct": yoy_trend_pct,
                    "total_competing_listings": total_competing,
                    "unique_stores_in_top10p": unique_stores,
                    "top5_store_sales_share_pct": round(top5_share_pct, 1),
                    "ad_saturation_pct": round(ad_saturation_pct, 1),
                    "avg_price_usd": round(avg_price, 2),
                    "median_price_usd": round(median_price, 2),
                    "price_iqr_usd": round(price_iqr, 2),
                    "total_reviews_top10p": total_reviews,
                    "avg_reviews_per_listing": round(avg_reviews, 1),
                    "total_est_sales_top10p": total_sales,
                    "avg_est_sales_per_listing": round(avg_sales, 1),
                    "total_est_revenue_top10p_usd": round(total_revenue, 2),
                    "avg_est_revenue_per_listing_usd": round(avg_revenue_per_listing, 2),
                    "bestseller_rate_pct": round(bestseller_rate, 1),
                    "popular_now_rate_pct": round(popular_now_rate, 1),
                    "star_seller_rate_pct": round(star_seller_rate, 1),
                    "active_cart_rate_pct": round(active_cart_rate, 1),
                }
            )

        kw_df = pd.DataFrame(records)

        # Compute Normalized Demand Score (0-100)
        # Driven by: Search Volume, Revenue per Listing, Popular Now + Bestseller Velocity, YoY Trend
        vol_norm = self._min_max_scale(kw_df["est_monthly_search_volume"])
        rev_per_list_norm = self._min_max_scale(kw_df["avg_est_revenue_per_listing_usd"])
        velocity_norm = self._min_max_scale(
            kw_df["popular_now_rate_pct"] * 1.2 + kw_df["bestseller_rate_pct"] + kw_df["active_cart_rate_pct"] * 0.5
        )
        trend_norm = self._min_max_scale(kw_df["yoy_search_trend_pct"])

        kw_df["demand_score"] = (
            0.30 * vol_norm + 0.30 * rev_per_list_norm + 0.25 * velocity_norm + 0.15 * trend_norm
        ).round(1)

        # Compute Normalized Competition Score (0-100) (Higher = More Saturated / Harder to Rank)
        # Driven by: Log(Total Competing Listings), Ad Saturation %, Average Incumbent Reviews, Price Compression
        log_listings_norm = self._min_max_scale(np.log10(kw_df["total_competing_listings"].clip(lower=100)))
        ad_norm = self._min_max_scale(kw_df["ad_saturation_pct"])
        incumbent_rev_norm = self._min_max_scale(kw_df["avg_reviews_per_listing"])
        low_price_penalty = 100.0 - self._min_max_scale(kw_df["avg_price_usd"])

        kw_df["competition_score"] = (
            0.45 * log_listings_norm
            + 0.20 * ad_norm
            + 0.20 * incumbent_rev_norm
            + 0.15 * low_price_penalty
        ).round(1)

        # Competition Level Categorical Label
        def _comp_label(score: float) -> str:
            if score < 35:
                return "Low"
            if score < 60:
                return "Moderate"
            if score < 80:
                return "High"
            return "Very High"

        kw_df["competition_level"] = kw_df["competition_score"].apply(_comp_label)

        # Opportunity / Growth Potential Score (0-100)
        # Rewards High Demand + Low Competition + Positive YoY Growth
        kw_df["opportunity_score"] = (
            0.52 * kw_df["demand_score"]
            + 0.38 * (100.0 - kw_df["competition_score"])
            + 0.10 * trend_norm
        ).round(1)

        def _niche_quadrant(row: pd.Series) -> str:
            if row["opportunity_score"] >= 68 and row["competition_score"] < 48:
                return "High-Growth Blue Ocean (High Demand / Low Competition)"
            if row["demand_score"] >= 55 and row["competition_score"] >= 48:
                return "Established Cash Cow (High Demand / High Competition)"
            if row["competition_score"] < 55:
                return "Emerging Micro-Niche (Moderate Demand / Low Competition)"
            return "Saturated Red Ocean (Low Margin / High Competition)"

        kw_df["niche_classification"] = kw_df.apply(_niche_quadrant, axis=1)
        kw_df = kw_df.sort_values("opportunity_score", ascending=False).reset_index(drop=True)
        return kw_df

    def aggregate_store_performance(self) -> pd.DataFrame:
        """
        Aggregates store-level metrics across all scraped pages: number of top-10-page
        listings, reviews, estimated sales, estimated revenue, average rating, and niche focus.
        """
        df = self.clean_df
        if df.empty:
            return pd.DataFrame()

        store_rows: List[Dict[str, Any]] = []
        for shop_name, grp in df.groupby("shop_name"):
            primary_kw = grp["keyword"].mode().iloc[0] if not grp["keyword"].mode().empty else grp["keyword"].iloc[0]
            arch = NICHE_ARCHETYPES.get(primary_kw.lower(), {})
            category = arch.get("category", "Digital Downloads")

            listings_captured = len(grp)
            unique_keywords = int(grp["keyword"].nunique())
            best_page = int(grp["page"].min())
            avg_global_rank = float(grp["global_rank"].mean())
            avg_price = float(grp["price"].mean())
            avg_rating = float(grp.loc[grp["rating"] > 0, "rating"].mean()) if (grp["rating"] > 0).any() else 4.80

            total_reviews = int(grp["reviews_count"].sum())
            total_sales = int(grp["estimated_sales"].sum())
            total_revenue = float(grp["estimated_revenue"].sum())
            revenue_per_listing = total_revenue / max(1, listings_captured)

            bestsellers_count = int(grp["is_bestseller"].sum())
            popular_now_count = int(grp["is_popular_now"].sum())
            is_star_seller = bool(grp["is_star_seller"].mean() >= 0.5)
            ad_listings_count = int(grp["is_ad"].sum())

            store_rows.append(
                {
                    "shop_name": shop_name,
                    "primary_keyword": primary_kw,
                    "primary_category": category,
                    "top10p_listings_count": listings_captured,
                    "unique_keywords_ranked": unique_keywords,
                    "best_page_rank": best_page,
                    "avg_global_rank": round(avg_global_rank, 1),
                    "avg_listing_price_usd": round(avg_price, 2),
                    "avg_star_rating": round(avg_rating, 2),
                    "total_reviews_captured": total_reviews,
                    "total_estimated_sales": total_sales,
                    "total_estimated_revenue_usd": round(total_revenue, 2),
                    "avg_revenue_per_listing_usd": round(revenue_per_listing, 2),
                    "bestseller_listings_count": bestsellers_count,
                    "popular_now_listings_count": popular_now_count,
                    "ad_listings_count": ad_listings_count,
                    "is_star_seller": is_star_seller,
                }
            )

        store_df = pd.DataFrame(store_rows)

        # Classify Store Performance Tier
        rev_q85 = store_df["total_estimated_revenue_usd"].quantile(0.85)
        rev_q50 = store_df["total_estimated_revenue_usd"].quantile(0.50)

        def _store_tier(row: pd.Series) -> str:
            if row["total_estimated_revenue_usd"] >= rev_q85:
                return "Tier 1: Market Leader / Power Shop"
            if row["total_estimated_revenue_usd"] >= rev_q50:
                return "Tier 2: High-Velocity Rising Challenger"
            return "Tier 3: Specialist / Niche Store"

        store_df["store_tier"] = store_df.apply(_store_tier, axis=1)
        store_df = store_df.sort_values("total_estimated_revenue_usd", ascending=False).reset_index(drop=True)
        return store_df

    def identify_trending_and_cluster_products(
        self, kw_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Applies K-Means Clustering (evaluating k=3..6 via Silhouette Score) and PCA 2D projection
        to segment digital products, and identifies the top trending products with high demand
        and relatively low competition.
        """
        df = self.clean_df.copy()
        if df.empty:
            return df, df, {}

        # Merge keyword-level competition and opportunity context onto individual listings
        kw_lookup = kw_df[
            [
                "keyword",
                "category",
                "est_monthly_search_volume",
                "yoy_search_trend_pct",
                "competition_score",
                "competition_level",
                "demand_score",
                "opportunity_score",
                "niche_classification",
            ]
        ]
        df = df.merge(kw_lookup, on="keyword", how="left")

        # Feature Engineering for Clustering (Standardize numerical features per ml-best-practices)
        df["log_sales"] = np.log1p(df["estimated_sales"])
        df["log_revenue"] = np.log1p(df["estimated_revenue"])
        df["log_competing_listings"] = np.log10(df["total_keyword_listings"].clip(lower=100))
        df["velocity_signal"] = (
            df["is_bestseller"].astype(int) * 2.0
            + df["is_popular_now"].astype(int) * 2.0
            + (df["in_carts_count"] > 0).astype(int) * 1.5
            + (df["recent_views_24h"] / 25.0)
        )

        feature_cols = [
            "price",
            "log_sales",
            "log_revenue",
            "velocity_signal",
            "competition_score",
            "demand_score",
        ]
        X = df[feature_cols].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Evaluate Silhouette Score across k in [3, 4, 5, 6]
        silhouette_results: Dict[int, float] = {}
        best_k = 4
        best_score = -1.0
        best_labels = None

        for k in [3, 4, 5, 6]:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            score = float(silhouette_score(X_scaled, labels))
            silhouette_results[k] = round(score, 4)
            if score > best_score:
                best_score = score
                best_k = k
                best_labels = labels

        df["cluster_id"] = best_labels

        # 2D PCA Projection for visualization
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(X_scaled)
        df["pca_1"] = coords[:, 0].round(4)
        df["pca_2"] = coords[:, 1].round(4)

        # Assign human-readable cluster names based on cluster centroids
        cluster_summary = (
            df.groupby("cluster_id")[
                ["price", "estimated_revenue", "competition_score", "demand_score", "velocity_signal"]
            ]
            .mean()
            .reset_index()
        )

        cluster_name_map: Dict[int, str] = {}
        for _, crow in cluster_summary.iterrows():
            cid = int(crow["cluster_id"])
            if crow["competition_score"] < 45 and crow["demand_score"] >= 50:
                cluster_name_map[cid] = f"Cluster {cid}: High-Growth Blue Ocean"
            elif crow["velocity_signal"] >= 2.2 and crow["estimated_revenue"] >= df["estimated_revenue"].median():
                cluster_name_map[cid] = f"Cluster {cid}: Viral Bestseller Leaders"
            elif crow["competition_score"] >= 65 and crow["price"] < 10.0:
                cluster_name_map[cid] = f"Cluster {cid}: High-Competition Commodity Prints"
            else:
                cluster_name_map[cid] = f"Cluster {cid}: Mid-Tier Evergreen Digital Goods"

        df["cluster_persona"] = df["cluster_id"].map(cluster_name_map)

        # Compute Listing-Level Trending Opportunity Score (0-100)
        # Identifies high-demand, high-velocity digital products in low-to-moderate competition niches
        rev_norm = self._min_max_scale(np.log1p(df["estimated_revenue"]))
        vel_norm = self._min_max_scale(df["velocity_signal"])
        low_comp_bonus = 100.0 - df["competition_score"]
        price_margin_bonus = self._min_max_scale(df["price"].clip(upper=35.0))

        df["listing_opportunity_index"] = (
            0.32 * rev_norm
            + 0.28 * vel_norm
            + 0.28 * low_comp_bonus
            + 0.12 * price_margin_bonus
        ).round(1)

        # Filter top trending digital product opportunities (high demand, low/moderate competition, strong velocity)
        trending_df = (
            df[
                (df["competition_score"] <= 62.0)
                & (df["is_bestseller"] | df["is_popular_now"] | (df["in_carts_count"] >= 10))
            ]
            .sort_values("listing_opportunity_index", ascending=False)
            .head(50)
            .reset_index(drop=True)
        )

        ml_diagnostics = {
            "silhouette_scores_by_k": silhouette_results,
            "optimal_k": best_k,
            "best_silhouette_score": round(best_score, 4),
            "pca_explained_variance_ratio": [round(float(v), 4) for v in pca.explained_variance_ratio_],
            "cluster_personas": cluster_name_map,
        }

        return df, trending_df, ml_diagnostics

    @staticmethod
    def _min_max_scale(series: pd.Series) -> pd.Series:
        s_min = float(series.min())
        s_max = float(series.max())
        if math.isclose(s_max, s_min):
            return pd.Series(50.0, index=series.index)
        return ((series - s_min) / (s_max - s_min)) * 100.0
