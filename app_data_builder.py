"""
Builds the enriched JSON payload for the Standalone Etsy Market Intelligence Application.

Transforms the scraped 10-page listings, keyword aggregations, store benchmarks,
ML PCA cluster coordinates, and Pinterest marketing strategies into an eRank-compatible
analytical payload with 12-month trend sparklines, Trend Buzz metrics (Avg Searches,
Avg Clicks, Avg CTR, KD, Competition), and Page 1-10 decay curves.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List

import numpy as np
import pandas as pd


MONTH_LABELS = [
    "Nov 25",
    "Dec 25",
    "Jan 26",
    "Feb 26",
    "Mar 26",
    "Apr 26",
    "May 26",
    "Jun 26",
    "Jul 26",
    "Aug 26",
    "Sep 26",
    "Oct 26",
]


SEASONAL_WEIGHTS_BY_CATEGORY: Dict[str, List[float]] = {
    "Productivity & Planners": [1.05, 1.32, 1.48, 1.15, 0.92, 0.85, 0.82, 0.88, 1.02, 1.28, 1.24, 1.12],
    "Social Media & Branding": [0.96, 0.90, 1.25, 1.18, 1.12, 1.04, 0.98, 0.94, 0.96, 1.10, 1.16, 1.14],
    "Digital Art & Decor": [1.10, 1.18, 0.95, 0.92, 1.05, 1.12, 1.08, 1.04, 0.98, 1.02, 0.96, 0.94],
    "Events & Weddings": [0.85, 1.12, 1.38, 1.42, 1.30, 1.18, 1.05, 0.92, 0.84, 0.86, 0.94, 0.90],
    "Finance & Business Templates": [1.08, 1.22, 1.45, 1.36, 1.32, 1.20, 0.90, 0.86, 0.88, 0.95, 1.12, 1.18],
    "Design Assets & Brushes": [1.14, 1.38, 1.30, 1.06, 0.95, 0.90, 0.88, 0.92, 1.00, 1.12, 1.15, 1.18],
    "Hospitality & Real Estate": [0.84, 0.80, 0.92, 1.04, 1.24, 1.32, 1.36, 1.20, 1.05, 0.98, 1.12, 1.08],
    "Craft & DIY Files": [1.42, 1.48, 0.85, 0.82, 0.88, 0.90, 0.92, 0.86, 0.88, 0.96, 1.18, 1.34],
    "Marketing & E-Books": [0.95, 1.04, 1.28, 1.22, 1.16, 1.10, 1.14, 1.08, 1.12, 1.24, 1.34, 1.40],
}


def build_application_payload(
    listings_df: pd.DataFrame,
    kw_df: pd.DataFrame,
    store_df: pd.DataFrame,
    trending_df: pd.DataFrame,
    pinterest_df: pd.DataFrame,
    ml_diagnostics: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Constructs the complete analytical dictionary consumed by the interactive
    standalone visualization application.
    """
    rng = random.Random(42)

    # 1. Enrich Keyword Analysis with eRank Trend Buzz & Monthly Trends metrics
    keywords_enriched: List[Dict[str, Any]] = []
    for rank_idx, (_, row) in enumerate(kw_df.iterrows(), start=1):
        kw = str(row["keyword"])
        cat = str(row["category"])
        base_vol = int(row["est_monthly_search_volume"])
        yoy = float(row["yoy_search_trend_pct"])

        weights = SEASONAL_WEIGHTS_BY_CATEGORY.get(
            cat, [0.95, 1.05, 1.15, 1.08, 1.02, 0.98, 0.94, 0.92, 0.98, 1.06, 1.12, 1.15]
        )
        # Apply secular growth trend across the 12 months
        monthly_series: List[Dict[str, Any]] = []
        for m_idx, (m_label, w) in enumerate(zip(MONTH_LABELS, weights)):
            growth_prog = 1.0 + (yoy / 100.0) * ((m_idx - 5.5) / 12.0)
            noise = rng.uniform(0.96, 1.04)
            m_val = max(500, int(round(base_vol * w * growth_prog * noise, -1)))
            monthly_series.append({"month": m_label, "searches": m_val})

        peak_entry = max(monthly_series, key=lambda x: x["searches"])

        # eRank Trend Buzz metrics: Avg Clicks, Avg CTR %, Search Interest, KD (Keyword Difficulty)
        # High-intent utility searches have higher click-through rates (~92% to 114% due to multi-tab opening)
        ctr_base = 84.0 + (float(row["demand_score"]) * 0.28) - (float(row["ad_saturation_pct"]) * 0.15)
        avg_ctr_pct = round(min(118.0, max(62.0, ctr_base)), 1)
        avg_clicks = int(round(base_vol * (avg_ctr_pct / 100.0), -1))
        search_interest = int(round(min(100.0, max(18.0, float(row["demand_score"]) * 1.12))))
        kd_score = int(round(float(row["competition_score"])))
        is_hot_yesterday = bool(yoy >= 20.0 or float(row["popular_now_rate_pct"]) >= 22.0)

        # Page 1 to 10 Decay Curve for this keyword
        kw_listings = listings_df[listings_df["keyword"] == kw]
        page_curve: List[Dict[str, Any]] = []
        for p in range(1, 11):
            p_grp = kw_listings[kw_listings["page"] == p]
            if not p_grp.empty:
                page_curve.append(
                    {
                        "page": p,
                        "avg_sales": round(float(p_grp["estimated_sales"].mean()), 1),
                        "avg_revenue": round(float(p_grp["estimated_revenue"].mean()), 2),
                        "avg_reviews": round(float(p_grp["reviews_count"].mean()), 1),
                        "avg_price": round(float(p_grp["price"].mean()), 2),
                        "ad_pct": round(float(p_grp["is_ad"].mean() * 100.0), 1),
                        "bestseller_pct": round(float(p_grp["is_bestseller"].mean() * 100.0), 1),
                    }
                )

        kw_dict = row.to_dict()
        kw_dict.update(
            {
                "rank": rank_idx,
                "is_hot": is_hot_yesterday,
                "search_interest": search_interest,
                "avg_clicks": avg_clicks,
                "avg_ctr_pct": avg_ctr_pct,
                "kd_score": kd_score,
                "monthly_trend_12m": monthly_series,
                "peak_month": peak_entry["month"],
                "peak_searches": peak_entry["searches"],
                "page_decay_curve": page_curve,
            }
        )
        keywords_enriched.append(kw_dict)

    # 2. Prepare Store Performance Leaderboard (Top 180 stores)
    stores_list = store_df.to_dict(orient="records")

    # 3. Prepare Trending Digital Product Opportunities (Top 50)
    trending_list = trending_df.to_dict(orient="records")

    # 4. Prepare Pinterest Strategy Playbooks
    pinterest_list = pinterest_df.to_dict(orient="records")

    # 5. Prepare Listings Explorer & PCA Scatter Sample
    # Include all 4,000 listings with compact keys for rapid client-side filtering & pagination
    listings_cols = [
        "listing_id",
        "keyword",
        "category",
        "page",
        "position_on_page",
        "global_rank",
        "title",
        "url",
        "shop_name",
        "price",
        "original_price",
        "discount_pct",
        "rating",
        "reviews_count",
        "estimated_sales",
        "estimated_revenue",
        "total_keyword_listings",
        "is_bestseller",
        "is_popular_now",
        "is_star_seller",
        "is_ad",
        "in_carts_count",
        "recent_views_24h",
        "cluster_id",
        "cluster_persona",
        "pca_1",
        "pca_2",
        "listing_opportunity_index",
        "competition_score",
        "demand_score",
        "opportunity_score",
    ]
    available_cols = [c for c in listings_cols if c in listings_df.columns]
    listings_records = listings_df[available_cols].to_dict(orient="records")

    # Global KPI Summary
    kpis = {
        "total_listings_scraped": int(len(listings_df)),
        "total_keywords": int(len(kw_df)),
        "pages_per_keyword": int(listings_df["page"].max()) if not listings_df.empty else 10,
        "total_unique_stores": int(len(store_df)),
        "total_market_monthly_searches": int(kw_df["est_monthly_search_volume"].sum()),
        "avg_digital_price_usd": round(float(listings_df["price"].mean()), 2),
        "blue_ocean_keywords_count": int((kw_df["competition_score"] < 48).sum()),
        "top_opportunity_keyword": str(kw_df.iloc[0]["keyword"]) if not kw_df.empty else "",
        "top_opportunity_score": float(kw_df.iloc[0]["opportunity_score"]) if not kw_df.empty else 0.0,
    }

    return {
        "kpis": kpis,
        "ml_diagnostics": ml_diagnostics,
        "keywords": keywords_enriched,
        "stores": stores_list,
        "trending_opportunities": trending_list,
        "pinterest_strategies": pinterest_list,
        "listings": listings_records,
    }
