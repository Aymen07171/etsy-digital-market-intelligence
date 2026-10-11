# Etsy Digital Product Scraper, Market Intelligence & Standalone Analytics Application

A complete Python-based web scraping, machine learning segmentation, and interactive visual analytics suite built with **Selenium (Chrome WebDriver)**, **BeautifulSoup4**, **Pandas**, **Scikit-Learn**, and an **eRank-inspired Standalone Application (`app.py`)** to evaluate Etsy marketplace opportunities for digital products.

---

## 1. Launching the Standalone Application

You can launch the standalone visual analytics application in three ways:

1. **One-Click Windows Desktop App Launcher:**
   Double-click [`Launch_Etsy_App.bat`](file:///c:/Users/jacka/Downloads/Etsy%20Analytics/Launch_Etsy_App.bat) to start the local Python backend server (`http://127.0.0.1:8050`) and open the application in a native-style Chrome `--app` window.
2. **Command-Line Server Mode (with Live On-Demand 10-Page Scraping):**
   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```
3. **Zero-Dependency Portable HTML Application:**
   Open [`output/Etsy_Market_Intelligence_App.html`](file:///c:/Users/jacka/Downloads/Etsy%20Analytics/output/Etsy_Market_Intelligence_App.html) directly in any browser—all 4,000 scraped listings, 10 keyword analyses, 180 store benchmarks, ML PCA clusters, and Pinterest marketing strategies are pre-compiled inside.

---

## 2. Application Modules & Interactive Views (eRank Pro Inspired)

- **🏠 Executive Dashboard:**
  - Interactive **Niche Opportunity Matrix** bubble chart (Demand Score vs. Competition Score, sized by Monthly Search Volume; click any bubble to drill down).
  - Dual-axis **Avg Estimated Revenue per Listing vs. Paid Etsy Ad Saturation (%)** chart.
- **📈 Monthly Trends (Aligned with eRank Reference #1):**
  - Real-time keyword filtering, Category selector, Seasonality window selector, and quick filters (`🔥 Hot Trends`, `💎 Blue Ocean`, `⭐ Bookmarked`).
  - Inline **12-Month Trend Graph Sparklines** with highlighted current-month bar, peak volume badge, and interactive **12-Month Search Seasonality Trajectory** chart.
- **🔥 Trend Buzz (Aligned with eRank Reference #2):**
  - Multi-metric table featuring `Rank`, `Keywords`, `Search Interest` progress bar, `Search Trend` sparkline, `Change %`, `Avg Searches`, `Avg Clicks`, `Avg CTR %`, color-coded `Etsy Competition` bar, `KD` (Keyword Difficulty), and `Opportunity Score`.
- **🔍 Keyword Research & Comparative Studio:**
  - Compare up to **3 keywords side-by-side** across a **6-Dimension Strategic Radar Chart**, a **Page 1 to Page 10 Rank Decay Curve** (Revenue, Sales, Reviews, or Ad Density by search page), and a full comparison matrix.
- **📊 Competitor Research (180 Store Leaderboard):**
  - Filter stores by Niche, Store Tier (`Tier 1: Market Leader`, `Tier 2: Rising Challenger`, `Tier 3: Specialist`), or `Star Seller` status, and click any shop to inspect all of its captured listings.
- **🏷️ Listing Optimization, 4,000-Listing Explorer & ML Cluster Map:**
  - Interactive **2D PCA Machine Learning Cluster Scatterplot** (`k = 6` K-Means clusters optimized via Silhouette Score).
  - Built-in **Etsy Digital Margin & Share-and-Save Fee Calculator**.
  - Multi-filter **4,000-Listing Browser** across Pages 1–10.
- **📌 Pinterest Ad Studio & Shop Insights:**
  - Interactive **Pinterest ROAS & Bundle Unit Economics Simulator** (dynamically recalculates Target Bundle AOV, Net Margin with Etsy's `4%` Share & Save rebate, Target CPA, Max Profitable CPC, and Daily Revenue).
  - Copy-ready 9:16 Video/Carousel Pin Hooks, Board Taxonomy, Interest Targeting, and Lead-Magnet Funnels.
