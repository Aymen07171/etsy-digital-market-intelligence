"""
Builds the enriched JSON payload for the Standalone Etsy Market Intelligence Application.

Includes both the Digital Products corpus AND the complete Phone Case Niche Intelligence
corpus (10-page keyword aggregations, Moroccan Stores Spotlight, Emerging 50-80 Sales
Breakout Stores, and High-Demand / Low-Competition Digital Case Design evaluations).
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config import OUTPUT_DIR
from phone_case_analyzer import PhoneCaseMarketAnalyzer
from phone_case_scraper import EtsyPhoneCaseScraper


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


def _load_or_build_phone_case_payload() -> Dict[str, Any]:
    """Loads or builds the 10-page Phone Case Niche Intelligence dataset & 70s Frog Sub-Niche Matrix."""
    pc_dir = OUTPUT_DIR / "phone_cases"
    kw_csv = pc_dir / "phone_case_keywords.csv"
    ma_csv = pc_dir / "moroccan_stores.csv"
    em_csv = pc_dir / "emerging_50_80_sales_stores.csv"
    des_csv = pc_dir / "digital_case_designs.csv"
    st_csv = pc_dir / "phone_case_stores_all.csv"

    if not (kw_csv.exists() and ma_csv.exists() and em_csv.exists() and des_csv.exists()):
        scraper = EtsyPhoneCaseScraper(max_pages=10)
        pc_listings = scraper.scrape_all_keywords(force_simulation=True)
        pc_analyzer = PhoneCaseMarketAnalyzer(pc_listings)
        kw_df = pc_analyzer.aggregate_keywords()
        all_stores_df, moroccan_df, emerging_df = pc_analyzer.aggregate_all_stores()
        enriched_df, design_df, ml_diag = pc_analyzer.evaluate_digital_case_designs_and_cluster(kw_df)
        pc_analyzer.export_all_phone_case_deliverables(
            enriched_df, kw_df, all_stores_df, moroccan_df, emerging_df, design_df, ml_diag
        )
    else:
        kw_df = pd.read_csv(kw_csv)
        moroccan_df = pd.read_csv(ma_csv)
        emerging_df = pd.read_csv(em_csv)
        design_df = pd.read_csv(des_csv)
        all_stores_df = pd.read_csv(st_csv)

    frog_dir = OUTPUT_DIR / "frog_subniches"
    frog_matrix_csv = frog_dir / "subniche_matrix.csv"
    frog_win_csv = frog_dir / "winning_variations.csv"
    frog_el_csv = frog_dir / "design_elements.csv"

    if not (frog_matrix_csv.exists() and frog_win_csv.exists() and frog_el_csv.exists()):
        from frog_subniche_research import run_frog_subniche_research
        frog_res = run_frog_subniche_research(live_mode=False)
        frog_matrix_df = frog_res["subniche_df"]
        frog_win_df = frog_res["winning_variations_df"]
        frog_el_df = frog_res["design_elements_df"]
    else:
        frog_matrix_df = pd.read_csv(frog_matrix_csv)
        frog_win_df = pd.read_csv(frog_win_csv)
        frog_el_df = pd.read_csv(frog_el_csv)

    return {
        "keywords": kw_df.to_dict(orient="records"),
        "moroccan_stores": moroccan_df.to_dict(orient="records"),
        "emerging_50_80_stores": emerging_df.to_dict(orient="records"),
        "digital_designs": design_df.to_dict(orient="records"),
        "all_stores": all_stores_df.to_dict(orient="records"),
        "frog_subniches": frog_matrix_df.to_dict(orient="records"),
        "frog_winning_variations": frog_win_df.head(30).to_dict(orient="records"),
        "frog_design_elements": frog_el_df.to_dict(orient="records"),
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

    keywords_enriched: List[Dict[str, Any]] = []
    for rank_idx, (_, row) in enumerate(kw_df.iterrows(), start=1):
        kw = str(row["keyword"])
        cat = str(row["category"])
        base_vol = int(row["est_monthly_search_volume"])
        yoy = float(row["yoy_search_trend_pct"])

        weights = SEASONAL_WEIGHTS_BY_CATEGORY.get(
            cat, [0.95, 1.05, 1.15, 1.08, 1.02, 0.98, 0.94, 0.92, 0.98, 1.06, 1.12, 1.15]
        )
        monthly_series: List[Dict[str, Any]] = []
        for m_idx, (m_label, w) in enumerate(zip(MONTH_LABELS, weights)):
            growth_prog = 1.0 + (yoy / 100.0) * ((m_idx - 5.5) / 12.0)
            noise = rng.uniform(0.96, 1.04)
            m_val = max(500, int(round(base_vol * w * growth_prog * noise, -1)))
            monthly_series.append({"month": m_label, "searches": m_val})

        peak_entry = max(monthly_series, key=lambda x: x["searches"])

        ctr_base = 84.0 + (float(row["demand_score"]) * 0.28) - (float(row["ad_saturation_pct"]) * 0.15)
        avg_ctr_pct = round(min(118.0, max(62.0, ctr_base)), 1)
        avg_clicks = int(round(base_vol * (avg_ctr_pct / 100.0), -1))
        search_interest = int(round(min(100.0, max(18.0, float(row["demand_score"]) * 1.12))))
        kd_score = int(round(float(row["competition_score"])))
        is_hot_yesterday = bool(yoy >= 20.0 or float(row["popular_now_rate_pct"]) >= 22.0)

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

    stores_list = store_df.to_dict(orient="records")
    trending_list = trending_df.to_dict(orient="records")
    pinterest_list = pinterest_df.to_dict(orient="records")

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

    phone_cases_payload = _load_or_build_phone_case_payload()

    return {
        "kpis": kpis,
        "ml_diagnostics": ml_diagnostics,
        "keywords": keywords_enriched,
        "stores": stores_list,
        "trending_opportunities": trending_list,
        "pinterest_strategies": pinterest_list,
        "listings": listings_records,
        "phone_cases": phone_cases_payload,
    }
