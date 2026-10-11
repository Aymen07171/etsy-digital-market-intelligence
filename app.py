r"""
Standalone Application Server & Desktop Window Launcher for Etsy Market Intelligence.

Features:
- Compiles the self-contained portable application to `output/Etsy_Market_Intelligence_App.html`
- Runs a local Python HTTP & REST API server (`http://127.0.0.1:8050`) connected directly to
  `scraper.py`, `analyzer.py`, `pinterest_strategy.py`, and `exporter.py`
- Supports live on-demand 10-page keyword scraping via `POST /api/scrape`
- Launches Google Chrome in native-like standalone desktop `--app` mode

Usage:
  # Build standalone HTML app and launch interactive desktop server:
  .\.venv\Scripts\python.exe app.py

  # Build standalone HTML app only (without starting long-running server):
  .\.venv\Scripts\python.exe app.py --build-only
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from analyzer import EtsyMarketAnalyzer
from app_data_builder import build_application_payload
from config import DEFAULT_DIGITAL_KEYWORDS, OUTPUT_DIR, ScraperConfig
from exporter import MarketIntelligenceExporter
from pinterest_strategy import PinterestStrategyGenerator
from scraper import EtsyListing, EtsySeleniumScraper
from ui_template import render_standalone_html

logger = logging.getLogger("etsy_standalone_app")


class AppStateManager:
    """Manages the in-memory and persisted marketplace dataset for the standalone app."""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.listings: List[EtsyListing] = []
        self.app_payload: Dict[str, Any] = {}
        self.html_path = self.output_dir / "Etsy_Market_Intelligence_App.html"

    def initialize(self) -> None:
        """Loads existing scraped listings or generates initial 10-page dataset."""
        raw_csv = self.output_dir / "listings_raw.csv"
        if raw_csv.exists():
            logger.info("Loading existing 10-page dataset from %s...", raw_csv)
            df = pd.read_csv(raw_csv)
            base_fields = {
                "keyword",
                "page",
                "position_on_page",
                "global_rank",
                "listing_id",
                "title",
                "url",
                "shop_name",
                "price",
                "original_price",
                "discount_pct",
                "currency",
                "rating",
                "reviews_count",
                "estimated_sales",
                "estimated_revenue",
                "total_keyword_listings",
                "is_digital",
                "is_bestseller",
                "is_popular_now",
                "is_star_seller",
                "is_ad",
                "in_carts_count",
                "recent_views_24h",
                "data_source",
            }
            records = df[[c for c in df.columns if c in base_fields]].to_dict(orient="records")
            self.listings = [EtsyListing(**r) for r in records]
        else:
            logger.info("Generating initial 10-page dataset across default digital keywords...")
            cfg = ScraperConfig(keywords=list(DEFAULT_DIGITAL_KEYWORDS), max_pages=10)
            scraper = EtsySeleniumScraper(cfg)
            self.listings = scraper.scrape_all_keywords(force_simulation=True)

        self.rebuild_analytics_and_html()

    def rebuild_analytics_and_html(self) -> Dict[str, Any]:
        """Recomputes keyword aggregations, store benchmarks, ML clusters, and standalone HTML."""
        analyzer = EtsyMarketAnalyzer(listings=self.listings)
        kw_df = analyzer.aggregate_keyword_insights()
        store_df = analyzer.aggregate_store_performance()
        enriched_listings_df, trending_df, ml_diagnostics = analyzer.identify_trending_and_cluster_products(kw_df)
        pinterest_df = PinterestStrategyGenerator.generate_strategy_table(kw_df)

        exporter = MarketIntelligenceExporter(output_dir=self.output_dir, charts_dir=self.output_dir / "charts")
        exporter.export_datasets(
            listings_df=enriched_listings_df,
            kw_df=kw_df,
            store_df=store_df,
            trending_df=trending_df,
            pinterest_df=pinterest_df,
            ml_diagnostics=ml_diagnostics,
        )

        self.app_payload = build_application_payload(
            listings_df=enriched_listings_df,
            kw_df=kw_df,
            store_df=store_df,
            trending_df=trending_df,
            pinterest_df=pinterest_df,
            ml_diagnostics=ml_diagnostics,
        )

        html_content = render_standalone_html(self.app_payload)
        self.html_path.write_text(html_content, encoding="utf-8")
        root_index = Path(__file__).resolve().parent / "index.html"
        root_index.write_text(html_content, encoding="utf-8")
        logger.info("Standalone HTML application compiled to: %s and %s", self.html_path, root_index)
        return self.app_payload

    def scrape_and_add_keyword(self, keyword: str, mode: str = "auto") -> Dict[str, Any]:
        """Scrapes 10 pages for a new keyword and updates all analytics and HTML."""
        kw_clean = keyword.strip().lower()
        # Remove existing entries for this keyword if refreshing
        self.listings = [item for item in self.listings if item.keyword.lower() != kw_clean]

        cfg = ScraperConfig(
            keywords=[kw_clean],
            max_pages=10,
            headless=True,
            use_fallback_on_block=(mode != "live"),
        )
        scraper = EtsySeleniumScraper(cfg)
        new_items = scraper.scrape_all_keywords(force_simulation=(mode == "benchmark"))
        self.listings.extend(new_items)
        return self.rebuild_analytics_and_html()


STATE = AppStateManager()


class EtsyAppRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler serving the standalone UI and live Python scraping API."""

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            html_bytes = STATE.html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
        elif self.path == "/api/state":
            body = json.dumps(STATE.app_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")

    def do_POST(self) -> None:
        if self.path == "/api/scrape":
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            payload = json.loads(raw_body)
            keyword = str(payload.get("keyword", "")).strip()
            mode = str(payload.get("mode", "auto"))

            if not keyword:
                self.send_error(400, "Missing keyword")
                return

            updated = STATE.scrape_and_add_keyword(keyword=keyword, mode=mode)
            resp_bytes = json.dumps(updated).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.end_headers()
            self.wfile.write(resp_bytes)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, fmt: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)


def launch_desktop_window(url: str) -> None:
    """Attempts to launch Google Chrome in standalone desktop `--app` mode."""
    chrome_path = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    if chrome_path.exists():
        try:
            subprocess.Popen([str(chrome_path), f"--app={url}", "--window-size=1480,920"])
            return
        except Exception:
            pass
    webbrowser.open(url)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser(description="Etsy Market Intelligence Standalone Application")
    parser.add_argument("--port", type=int, default=8050, help="Local server port (default: 8050)")
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Build the self-contained standalone HTML app in output/ and exit.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the local server without automatically opening a browser window.",
    )
    args = parser.parse_args()

    STATE.initialize()

    if args.build_only:
        print(f"\n[SUCCESS] Standalone Application built at: {STATE.html_path}\n")
        return 0

    server_addr = ("127.0.0.1", args.port)
    httpd = ThreadingHTTPServer(server_addr, EtsyAppRequestHandler)
    url = f"http://127.0.0.1:{args.port}"
    logger.info("Etsy Market Intelligence Standalone App running at %s", url)

    if not args.no_browser:
        launch_desktop_window(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down standalone application server.")
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
