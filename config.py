"""
Configuration and constants for the Etsy Digital Products Scraper & Analytics Suite.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"


DEFAULT_DIGITAL_KEYWORDS: List[str] = [
    "digital planner goodnotes",
    "notion template adhd",
    "canva instagram templates",
    "printable wall art boho",
    "wedding invitation template download",
    "small business bookkeeping spreadsheet",
    "procreate brushes bundle",
    "airbnb welcome book template",
    "svg cut files bundle",
    "faceless digital marketing guide",
]


@dataclass
class ScraperConfig:
    """Configuration for Selenium Chrome scraping on Etsy."""

    keywords: List[str] = field(default_factory=lambda: list(DEFAULT_DIGITAL_KEYWORDS))
    max_pages: int = 10
    headless: bool = True
    min_delay_sec: float = 2.0
    max_delay_sec: float = 4.5
    page_load_timeout_sec: int = 25
    implicit_wait_sec: int = 5
    user_data_dir: str | None = None
    chrome_binary_path: str | None = None
    use_fallback_on_block: bool = True
    random_seed: int = 42

    # Estimation parameters for digital products on Etsy
    # Digital products typically convert reviews at ~1.8% to 3.2% of total sales
    base_review_to_sales_multiplier: float = 42.0
    bestseller_velocity_boost: float = 1.35
    popular_now_velocity_boost: float = 1.20
    star_seller_velocity_boost: float = 1.10
    page_rank_decay_rate: float = 0.06  # Higher pages have lower recent velocity
