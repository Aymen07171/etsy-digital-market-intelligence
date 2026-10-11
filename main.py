r"""
Main CLI Entrypoint for the Etsy Digital Product Scraper & Market Intelligence Suite.

Usage examples:
  # Run full pipeline (auto-detects live Selenium vs calibrated fallback if DataDome blocks):
  .\.venv\Scripts\python.exe main.py --pages 10 --mode auto

  # Run with custom keywords in headed Chrome browser:
  .\.venv\Scripts\python.exe main.py --keywords "notion template adhd" "digital planner goodnotes" --pages 10 --headed

  # Fast benchmark run across all 10 digital product niches (10 pages each = 4,000 listings):
  .\.venv\Scripts\python.exe main.py --pages 10 --mode benchmark
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from analyzer import EtsyMarketAnalyzer
from config import DEFAULT_DIGITAL_KEYWORDS, OUTPUT_DIR, ScraperConfig
from exporter import MarketIntelligenceExporter
from pinterest_strategy import PinterestStrategyGenerator
from scraper import EtsySeleniumScraper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Etsy Digital Product Web Scraper & Market Intelligence Suite"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=DEFAULT_DIGITAL_KEYWORDS,
        help="List of digital product keywords to search on Etsy (default: 10 curated digital niches).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Number of Etsy search result pages to scrape per keyword (default: 10).",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "live", "benchmark"],
        default="auto",
        help=(
            "'auto' = attempt live Chrome Selenium scrape & fall back to calibrated 10-page model if "
            "DataDome CAPTCHA blocks; 'live' = strict live Selenium only; 'benchmark' = calibrated 10-page dataset."
        ),
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run Chrome in headed (visible window) mode instead of headless.",
    )
    parser.add_argument(
        "--user-data-dir",
        type=str,
        default=None,
        help="Optional path to Chrome user profile directory to reuse cookies/sessions.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUTPUT_DIR),
        help="Output directory for CSVs, Excel workbook, charts, and Markdown report.",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("etsy_analytics")

    args = parse_args()
    out_dir = Path(args.output_dir)
    charts_dir = out_dir / "charts"

    config = ScraperConfig(
        keywords=args.keywords,
        max_pages=args.pages,
        headless=not args.headed,
        user_data_dir=args.user_data_dir,
        use_fallback_on_block=(args.mode != "live"),
    )

    logger.info(
        "Starting Etsy Digital Product Intelligence Pipeline | Keywords=%d | Pages/Keyword=%d | Mode=%s",
        len(config.keywords),
        config.max_pages,
        args.mode,
    )

    scraper = EtsySeleniumScraper(config=config)
    listings = scraper.scrape_all_keywords(force_simulation=(args.mode == "benchmark"))

    if not listings:
        logger.error("No listings were collected. Try running with '--mode auto' or '--headed'.")
        return 1

    logger.info("Collected %d total listings across %d keywords. Running analytics & ML clustering...", len(listings), len(config.keywords))

    analyzer = EtsyMarketAnalyzer(listings=listings)
    kw_df = analyzer.aggregate_keyword_insights()
    store_df = analyzer.aggregate_store_performance()
    enriched_listings_df, trending_df, ml_diagnostics = analyzer.identify_trending_and_cluster_products(kw_df)

    logger.info("Generating Pinterest marketing & paid advertising unit economics...")
    pinterest_df = PinterestStrategyGenerator.generate_strategy_table(kw_df)

    exporter = MarketIntelligenceExporter(output_dir=out_dir, charts_dir=charts_dir)
    saved_files = exporter.export_datasets(
        listings_df=enriched_listings_df,
        kw_df=kw_df,
        store_df=store_df,
        trending_df=trending_df,
        pinterest_df=pinterest_df,
        ml_diagnostics=ml_diagnostics,
    )
    chart_files = exporter.generate_charts(
        listings_df=enriched_listings_df,
        kw_df=kw_df,
        store_df=store_df,
        ml_diagnostics=ml_diagnostics,
    )
    report_path = exporter.generate_markdown_report(
        listings_df=enriched_listings_df,
        kw_df=kw_df,
        store_df=store_df,
        trending_df=trending_df,
        pinterest_df=pinterest_df,
        ml_diagnostics=ml_diagnostics,
    )

    print("\n" + "=" * 92)
    print("ETSY DIGITAL PRODUCT MARKETPLACE INTELLIGENCE SUMMARY (10 PAGES / KEYWORD)")
    print("=" * 92)
    display_cols = [
        "keyword",
        "est_monthly_search_volume",
        "total_competing_listings",
        "avg_price_usd",
        "avg_est_revenue_per_listing_usd",
        "demand_score",
        "competition_score",
        "opportunity_score",
    ]
    print(kw_df[display_cols].to_string(index=False))
    print("-" * 92)
    print(f"Optimal ML Clustering: k={ml_diagnostics['optimal_k']} (Silhouette={ml_diagnostics['best_silhouette_score']})")
    print(f"Excel Workbook:        {saved_files['excel_workbook']}")
    print(f"Strategic Report:      {report_path}")
    print(f"Charts Generated:      {len(chart_files)} PNG charts in {charts_dir}")
    print("=" * 92 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
