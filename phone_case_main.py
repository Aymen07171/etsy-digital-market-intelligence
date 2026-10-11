r"""
CLI Entrypoint for the Etsy Phone Case Niche Scraper & Analytics Solution.

Scrapes 10 result pages per phone case keyword, identifies Moroccan stores and
emerging breakout stores (50-80 sales), evaluates digital case design themes,
and exports structured Excel/CSV datasets, charts, and strategic recommendations.

Usage:
  .\.venv\Scripts\python.exe phone_case_main.py --pages 10 --mode auto
  .\.venv\Scripts\python.exe phone_case_main.py --pages 10 --mode benchmark
"""

from __future__ import annotations

import argparse
import logging
import sys

from phone_case_analyzer import PhoneCaseMarketAnalyzer
from phone_case_scraper import DEFAULT_PHONE_CASE_KEYWORDS, EtsyPhoneCaseScraper


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("phone_case_analytics")

    parser = argparse.ArgumentParser(description="Etsy Phone Case Niche Scraper & Analytics")
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=DEFAULT_PHONE_CASE_KEYWORDS,
        help="Phone case keywords to scrape across 10 pages each.",
    )
    parser.add_argument("--pages", type=int, default=10, help="Pages per keyword (default: 10)")
    parser.add_argument(
        "--mode",
        choices=["auto", "live", "benchmark"],
        default="auto",
        help="Execution mode: 'auto' (Selenium + fallback), 'live', or 'benchmark'.",
    )
    parser.add_argument("--headed", action="store_true", help="Run Chrome in headed mode.")
    args = parser.parse_args()

    logger.info(
        "Starting Etsy Phone Case Intelligence Pipeline | Keywords=%d | Pages/Keyword=%d | Mode=%s",
        len(args.keywords),
        args.pages,
        args.mode,
    )

    scraper = EtsyPhoneCaseScraper(
        keywords=args.keywords,
        max_pages=args.pages,
        headless=not args.headed,
        use_fallback_on_block=(args.mode != "live"),
    )
    listings = scraper.scrape_all_keywords(force_simulation=(args.mode == "benchmark"))

    analyzer = PhoneCaseMarketAnalyzer(listings=listings)
    kw_df = analyzer.aggregate_keywords()
    all_stores_df, moroccan_df, emerging_df = analyzer.aggregate_all_stores()
    enriched_df, design_df, ml_diag = analyzer.evaluate_digital_case_designs_and_cluster(kw_df)

    saved_paths = analyzer.export_all_phone_case_deliverables(
        enriched_df=enriched_df,
        kw_df=kw_df,
        all_stores_df=all_stores_df,
        moroccan_df=moroccan_df,
        emerging_df=emerging_df,
        design_df=design_df,
        ml_diag=ml_diag,
    )

    print("\n" + "=" * 96)
    print("ETSY PHONE CASE MARKETPLACE INTELLIGENCE SUMMARY (10 PAGES / KEYWORD)")
    print("=" * 96)
    cols = [
        "keyword",
        "est_monthly_search_volume",
        "total_competing_listings",
        "avg_price_usd",
        "moroccan_stores_present",
        "emerging_50_80_stores_present",
        "demand_score",
        "competition_score",
        "opportunity_score",
    ]
    print(kw_df[cols].to_string(index=False))
    print("-" * 96)
    print(f"Moroccan Stores Highlighted:         {len(moroccan_df)} stores")
    print(f"Emerging Stores (50-80 Sales):       {len(emerging_df)} stores")
    print(f"Digital Case Design Themes Ranked:   {len(design_df)} themes")
    print(f"Excel Workbook:                      {saved_paths['excel_workbook']}")
    print(f"Strategic Report:                    {saved_paths['markdown_report']}")
    print("=" * 96 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
