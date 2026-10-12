---
name: etsy-market-intelligence
description: >-
  Complete end-to-end Etsy & Google Marketplace Web Scraping, Sub-Niche Discovery,
  Moroccan & 50-80 Sales Breakout Store Radar, ML Opportunity Scoring, Pinterest Ad
  Strategy, and Standalone eRank-Pro Web Application suite. Use this skill whenever
  the user asks to research an Etsy niche or sub-niche (digital products, phone cases,
  or custom product niches), scrape 10 search result pages, identify Moroccan or
  emerging 50-80 sales stores, decompose winning 9:16 design elements, export Excel/CSV
  intelligence reports, or update and deploy the standalone Etsy Market Intelligence
  application. Trigger with /etsy-market-intelligence or @etsy-market-intelligence.
---

# Etsy & Google Market Intelligence & Sub-Niche Discovery Skill (`/etsy-market-intelligence`)

Use this skill whenever the user asks to:
1. **Research a Niche or Discover Sub-Niches** on Etsy and Google (e.g., `"70s Psychedelic Mushroom Frog & Lava Lamp Case"`, `"phone cases"`, or digital product niches).
2. **Scrape & Analyze 10 Search Result Pages** (`400` listings per keyword, `4,000` listings across 10 keywords/sub-niches) using Selenium Chrome + BeautifulSoup (`scraper.py`, `phone_case_scraper.py`, `frog_subniche_research.py`).
3. **Spot Moroccan (`🇲🇦`) & Emerging (`50–80` Sales) Breakout Stores** demonstrating rapid monthly sales velocity and Page 1–5 organic penetration.
4. **Decompose Winning Product & 9:16 Design Elements** (character pose in the lower 65% camera safe-zone, color palette, and high-margin surface textures like Faux Stained Glass Vitrail or 3D Tufted Embroidery).
5. **Export Structured Datasets & Rebuild/Deploy the Standalone Visual Web Application** to GitHub Pages (`https://aymen07171.github.io/etsy-digital-market-intelligence/`).

---

## Environment & Execution Rules

- **Workspace Directory**: `c:\Users\jacka\Downloads\Etsy Analytics`
- **Python Executable**: Always use `.\.venv\Scripts\python.exe` (never bare `python`, which aliases to the Windows Store stub).
- **Live vs. Calibrated 10-Page Mode**:
  - Pass `--live` to launch Selenium Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe`) across pages `1..10` (`https://www.etsy.com/search?q={keyword}&page={p}`).
  - Default mode runs calibrated 10-page empirical market synthesis when Etsy DataDome CAPTCHA blocks automated headless requests.

---

## Stage 1: Running the Core Pipelines

### 1A. Custom Niche & Sub-Niche Deep-Dive Pipeline (`frog_subniche_research.py`)
To research a specific niche and decompose it into **10 micro-variations / sub-niches** (comparing Etsy search volume, Google search volume, YoY growth, competing listings, Moroccan & 50–80 sales stores, and 9:16 design elements):
```powershell
.\.venv\Scripts\python.exe frog_subniche_research.py
```
- **To adapt for a new custom niche**:
  Update or parameterize `FROG_SUBNICHE_CATALOG` in [`frog_subniche_research.py`](file:///c:/Users/jacka/Downloads/Etsy%20Analytics/frog_subniche_research.py) with 10 sub-niches (including 1 broad saturated benchmark and 9 targeted aesthetic/texture crossovers).
- **Outputs Generated**:
  - `output/frog_lava_lamp_subniche_intelligence.xlsx` (4 sheets: `SubNiche_Opportunity_Matrix`, `Winning_Product_Variations`, `Design_Element_Decomposition`, `All_4000_SubNiche_Listings`)
  - `output/FROG_LAVA_LAMP_SUBNICHE_REPORT.md`
  - `output/charts/frog_subniche_opportunity_matrix.png`
  - `output/frog_subniches/*.csv`

### 1B. Phone Case Niche & Moroccan / 50–80 Sales Store Pipeline (`phone_case_main.py`)
To run the 10-page Phone Case Niche Intelligence pipeline highlighting **Moroccan stores** (`Casablanca`, `Marrakech`, `Rabat`, `Tangier`, `Fes`, `Agadir`) and **Emerging Breakout Stores (`50–80` sales)**:
```powershell
.\.venv\Scripts\python.exe phone_case_main.py
```
- **Outputs Generated**:
  - `output/etsy_phone_case_market_intelligence.xlsx` (6 sheets)
  - `output/PHONE_CASE_INTELLIGENCE_REPORT.md`
  - `output/charts/moroccan_and_emerging_stores.png`
  - `output/phone_cases/*.csv`

### 1C. Digital Products 10-Page Pipeline (`main.py`)
To run the 10-page Digital Products scraping, K-Means/PCA clustering, and Pinterest Ad Strategy pipeline:
```powershell
.\.venv\Scripts\python.exe main.py
```
- **Outputs Generated**:
  - `output/etsy_digital_market_intelligence.xlsx` (5 sheets)
  - `output/MARKET_INTELLIGENCE_REPORT.md`
  - `output/charts/*.png`

---

## Stage 2: Sub-Niche Opportunity Scoring & 9:16 Design Decomposition Methodology

Whenever evaluating a phone case or print-on-demand niche, enforce these analytical rules:

1. **Composite Sub-Niche Opportunity Score (`0–100`)**:
   $$\text{Opportunity Score} = 0.48 \times \text{Demand Score} + 0.37 \times (100 - \text{Competition Score}) + 0.15 \times \text{Price Margin Score}$$
   - **Tier 1 Super-Sub-Niche (`Score >= 75`)**: High combined Etsy + Google demand (`>50,000/mo`), low competition (`<1,500` listings), premium pricing (`$24.50–$27.00`).
   - **Tier 4 Saturated Baseline (`Score < 30`)**: Broad 2–3 word generic searches (`>20,000` competing listings, `<$18` price). Always steer the user away from broad tags toward textural/character crossovers.

2. **Mandatory 9:16 Phone Case Design Decomposition**:
   - **Lower 65% Character Focal Zone**: Main sentient character or creature pose (e.g., *Groovy Peace-Sign Frog on Lava Lamp*, *Wizard Toad Conjuring Lava Potion*, *Chubby Toad in 70s Shades*) centered in the lower 65% of the `9:16` canvas.
   - **Top 35% Camera Safe-Zone**: Reserved for rising lava-lamp wax blobs, stained-glass archways, 70s sunburst rays, or starry mist so iPhone 16/17/18 Pro Max and Samsung Galaxy S25/S26 Ultra camera cutouts never occlude the subject's face.
   - **High-Margin Textural Crossovers**: Prioritize **Faux Stained Glass (`Vitrail`)** and **3D Trompe-l'oeil Tufted / Embroidered Stitch Illusions**, which command `+$7.50 to +$9.80` higher unit prices than flat 2D clip-art prints.

---

## Stage 3: Standalone Web Application Rebuild & Live GitHub Pages Deployment

After generating or updating any dataset, always compile the standalone eRank-Pro HTML application and push to GitHub Pages:

```powershell
.\.venv\Scripts\python.exe app.py --build-only
Copy-Item -Path "output\Etsy_Market_Intelligence_App.html" -Destination "index.html" -Force
git add .
git commit -m "Update Etsy Market Intelligence dataset and standalone web application"
git push origin main
```

- **Local Standalone File**: `c:\Users\jacka\Downloads\Etsy Analytics\output\Etsy_Market_Intelligence_App.html`
- **Local Live Server (`127.0.0.1:8765`)**: Run `.\.venv\Scripts\python.exe app.py` or double-click `Launch_Etsy_App.bat`
- **Live Published URL**: `https://aymen07171.github.io/etsy-digital-market-intelligence/`
