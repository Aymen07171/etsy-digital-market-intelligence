"""
HTML5 + Chart.js + Interactive JS Application Builder for the Etsy Market Intelligence Suite.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from ui_styles import APP_CSS


def render_standalone_html(app_data: Dict[str, Any]) -> str:
    """Renders the complete standalone HTML application with embedded JSON state."""
    json_payload = json.dumps(app_data, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>eRank Pro · Etsy Digital Product Market Intelligence & Pinterest Studio</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
  <style>
{APP_CSS}
  </style>
</head>
<body>

  <!-- ================= LEFT NAVIGATION SIDEBAR (eRank Deep Forest Green) ================= -->
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-logo">
        <span class="e-mark">e</span>
        <span>eRank</span>
      </div>
      <span class="brand-badge">PRO SUITE</span>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-item active" data-view="dashboard" onclick="switchView('dashboard')">
        <div class="nav-item-left"><span class="nav-icon">🏠</span><span>Dashboard</span></div>
      </div>

      <div class="nav-item" data-view="keyword-research" onclick="switchView('keyword-research')">
        <div class="nav-item-left"><span class="nav-icon">🔍</span><span>Keyword Research</span></div>
        <span>▾</span>
      </div>

      <div class="nav-item" data-view="competitor-research" onclick="switchView('competitor-research')">
        <div class="nav-item-left"><span class="nav-icon">📊</span><span>Competitor Research</span></div>
        <span>▾</span>
      </div>

      <div class="nav-item" data-view="listing-optimization" onclick="switchView('listing-optimization')">
        <div class="nav-item-left"><span class="nav-icon">🏷️</span><span>Listing Optimization</span></div>
        <span>▾</span>
      </div>

      <div class="nav-item" data-view="shop-insights" onclick="switchView('shop-insights')">
        <div class="nav-item-left"><span class="nav-icon">📌</span><span>Pinterest & Shop Insights</span></div>
        <span>▾</span>
      </div>

      <div class="nav-item" onclick="toggleTrendsMenu()">
        <div class="nav-item-left"><span class="nav-icon">🔥</span><span>Trends</span></div>
        <span id="trends-chevron">▴</span>
      </div>
      <div class="nav-submenu" id="trends-submenu">
        <div class="nav-subitem" data-view="trend-buzz" onclick="switchView('trend-buzz')">
          <span>Trend Buzz</span>
          <span style="font-size:11px;opacity:0.8;">🔥</span>
        </div>
        <div class="nav-subitem" data-view="monthly-trends" onclick="switchView('monthly-trends')">
          <span>Monthly Trends</span>
          <span style="font-size:11px;opacity:0.8;">📈</span>
        </div>
      </div>

      <div class="nav-item" data-view="reference-design" onclick="switchView('reference-design')">
        <div class="nav-item-left"><span class="nav-icon">🎨</span><span>Design & Methodology</span></div>
      </div>
    </nav>

    <div class="sidebar-footer">
      <button class="btn-upgrade" onclick="openScrapeModal()">
        <span>⚡</span><span>Scrape New Keyword (10p)</span>
      </button>
      <div class="sidebar-status">
        <span class="status-dot"></span>
        <span id="sidebar-corpus-status">4,000 Listings · 180 Stores</span>
      </div>
    </div>
  </aside>

  <!-- ================= MAIN VIEWPORT ================= -->
  <div class="main-wrapper">

    <!-- TOP BAR (Matches eRank Top Utility Bar) -->
    <header class="topbar">
      <div class="search-group">
        <select class="search-select" id="global-marketplace">
          <option value="Etsy">Etsy Digital</option>
          <option value="Pinterest">Pinterest SEO</option>
        </select>
        <input
          type="text"
          id="global-search-input"
          class="search-input"
          placeholder="Enter keyword (filter existing or press Enter to inspect / scrape)..."
          onkeydown="if(event.key==='Enter') handleGlobalSearch()"
        />
        <div class="country-badge">🇺🇸 USA ▾</div>
        <button class="search-btn" title="Search or Scrape Keyword" onclick="handleGlobalSearch()">🔍</button>
      </div>

      <div class="topbar-right">
        <div class="quota-pill">
          <span>🕒 Active Dataset:</span>
          <strong id="topbar-kw-count">10 Keywords (10 Pages Each)</strong>
          <a href="javascript:void(0)" onclick="openScrapeModal()" style="color:var(--erank-orange);font-weight:700;text-decoration:none;margin-left:4px;">+ Add Keyword ↑</a>
        </div>
        <button class="btn-outline" onclick="exportCurrentCSV()">📥 Export CSV</button>
        <button class="btn-primary" onclick="switchView('monthly-trends')">📈 Monthly Trends</button>
      </div>
    </header>

    <!-- SCROLLABLE CONTENT AREA -->
    <main class="content-area">

      <!-- ===================================================================== -->
      <!-- VIEW 1: EXECUTIVE DASHBOARD                                           -->
      <!-- ===================================================================== -->
      <section id="view-dashboard" class="view-panel active">
        <div class="page-header">
          <div>
            <h1 class="page-title">Etsy Digital Product Market Intelligence Dashboard</h1>
            <p class="page-subtitle">Aggregated across the first 10 search result pages per keyword · Identifying high-demand, low-competition digital opportunities.</p>
          </div>
          <div style="display:flex;gap:10px;">
            <button class="btn-outline" onclick="switchView('trend-buzz')">🔥 Open Trend Buzz</button>
            <button class="btn-primary" onclick="switchView('shop-insights')">📌 Pinterest Ad Studio</button>
          </div>
        </div>

        <div class="kpi-grid" id="dashboard-kpi-grid"></div>

        <div class="chart-grid-2">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Niche Opportunity Matrix: Demand vs. Competition (Bubble Size = Monthly Searches)</div>
                <div class="card-subtitle">Click any bubble to drill down into that keyword's 10-page decay & seasonality. Top-Left = High-Growth Blue Ocean.</div>
              </div>
              <span class="badge-pill badge-low">Interactive Drilldown</span>
            </div>
            <div class="chart-box">
              <canvas id="chartOpportunityMatrix"></canvas>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Avg Estimated Revenue per Listing vs. Ad Saturation (%)</div>
                <div class="card-subtitle">Comparing top-10-page listing revenue against paid Etsy Ad crowding</div>
              </div>
            </div>
            <div class="chart-box">
              <canvas id="chartRevenueVsAds"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Strategic Keyword Ranking Summary (Pages 1–10 Aggregated)</div>
              <div class="card-subtitle">Click any keyword to inspect its 12-month search trend, Page 1–10 rank decay, and Pinterest marketing blueprint</div>
            </div>
            <div style="display:flex;gap:8px;">
              <input type="text" id="dash-kw-filter" class="filter-input" placeholder="Filter keywords..." oninput="renderDashboardTable()" style="height:32px;width:210px;" />
            </div>
          </div>
          <div class="table-container">
            <table class="erank-table" id="dashboard-kw-table">
              <thead>
                <tr>
                  <th onclick="sortKeywords('rank')"># ⇅</th>
                  <th onclick="sortKeywords('keyword')">Keyword ⇅</th>
                  <th>12-Mo Trend Graph</th>
                  <th class="num" onclick="sortKeywords('est_monthly_search_volume')">Monthly Searches ⇅</th>
                  <th class="num" onclick="sortKeywords('yoy_search_trend_pct')">YoY Trend ⇅</th>
                  <th class="num" onclick="sortKeywords('total_competing_listings')">Competing Listings ⇅</th>
                  <th class="num" onclick="sortKeywords('avg_price_usd')">Avg Price ⇅</th>
                  <th class="num" onclick="sortKeywords('avg_est_revenue_per_listing_usd')">Avg Rev / Listing ⇅</th>
                  <th class="num" onclick="sortKeywords('demand_score')">Demand ⇅</th>
                  <th class="num" onclick="sortKeywords('competition_score')">Competition ⇅</th>
                  <th class="num" onclick="sortKeywords('opportunity_score')">Opp Score ⇅</th>
                  <th>Strategic Classification</th>
                </tr>
              </thead>
              <tbody id="dashboard-kw-tbody"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 2: MONTHLY TRENDS (Matches eRank Screenshot 1)                   -->
      <!-- ===================================================================== -->
      <section id="view-monthly-trends" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">Monthly Trends <span style="font-size:15px;color:#84948e;font-weight:400;" title="12-Month Search Volume & Seasonality Tracker">ⓘ</span></h1>
            <p class="page-subtitle">The most popular digital product search terms on Etsy for September–October 2026. Keywords marked with 🔥 were very popular yesterday.</p>
          </div>
        </div>

        <div class="filter-card">
          <div class="filter-field" style="flex:1.5;">
            <label>FILTER</label>
            <input type="text" id="mt-filter-input" class="filter-input" placeholder="🔍 Filter keywords..." oninput="renderMonthlyTrendsTable()" />
          </div>
          <div class="filter-field">
            <label>CATEGORIES</label>
            <select id="mt-category-select" class="filter-select" onchange="renderMonthlyTrendsTable()">
              <option value="ALL">All Categories</option>
            </select>
          </div>
          <div class="filter-field">
            <label>DATE / SEASON WINDOW</label>
            <select id="mt-date-select" class="filter-select" onchange="renderMonthlyTrendsTable()">
              <option value="Sep 2026">Sep 2026 (Current)</option>
              <option value="Oct 2026">Oct 2026 (Forecast)</option>
              <option value="Jan 26">Jan 2026 (Q1 Peak)</option>
            </select>
          </div>
          <div class="filter-field" style="flex:0.6;min-width:140px;">
            <label>QUICK FILTER</label>
            <select id="mt-hot-select" class="filter-select" onchange="renderMonthlyTrendsTable()">
              <option value="ALL">All Keywords</option>
              <option value="HOT">🔥 Hot Trends Only</option>
              <option value="BLUE">💎 Blue Ocean Only</option>
              <option value="STAR">⭐ Bookmarked Only</option>
            </select>
          </div>
        </div>

        <div class="table-container" style="margin-bottom:20px;">
          <table class="erank-table">
            <thead>
              <tr>
                <th style="width:70px;"># ⇅</th>
                <th>Keywords ⇅</th>
                <th>Category</th>
                <th style="text-align:center;">Trend Graph (12 Months)</th>
                <th class="num">Average Searches ⇅</th>
                <th class="num">YoY Surge ⇅</th>
                <th class="num">Competing Listings ⇅</th>
                <th class="num">Avg Price ($) ⇅</th>
                <th class="num">Avg Rev / Listing ⇅</th>
                <th class="num">Opportunity Score ⇅</th>
              </tr>
            </thead>
            <tbody id="mt-tbody"></tbody>
          </table>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title" id="mt-detail-chart-title">12-Month Search Volume Seasonality Trajectory</div>
              <div class="card-subtitle">Click any keyword row above to overlay and compare its monthly search curve</div>
            </div>
          </div>
          <div class="chart-box-sm">
            <canvas id="chartMonthlySeasonality"></canvas>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 3: TREND BUZZ (Matches eRank Screenshot 2)                       -->
      <!-- ===================================================================== -->
      <section id="view-trend-buzz" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">Trend Buzz <span style="font-size:15px;color:#84948e;font-weight:400;">ⓘ</span></h1>
            <p class="page-subtitle">Discover what digital product buyers are searching for on Etsy, Pinterest, and digital marketplaces right now.</p>
          </div>
        </div>

        <div class="filter-card">
          <div class="filter-field">
            <label>Marketplace</label>
            <select id="tb-marketplace" class="filter-select" onchange="renderTrendBuzzTable()">
              <option value="Etsy">Etsy (Digital Marketplace)</option>
              <option value="Pinterest">Pinterest Cross-Channel</option>
            </select>
          </div>
          <div class="filter-field">
            <label>Country</label>
            <select id="tb-country" class="filter-select" onchange="renderTrendBuzzTable()">
              <option value="USA">🇺🇸 USA (Primary)</option>
              <option value="GLOBAL">🌐 Global English</option>
            </select>
          </div>
          <div class="filter-field">
            <label>Timeframe</label>
            <select id="tb-timeframe" class="filter-select" onchange="renderTrendBuzzTable()">
              <option value="Yesterday">Yesterday (Real-Time Velocity)</option>
              <option value="Past 7 Days">Past 7 Days</option>
              <option value="Past 30 Days">Past 30 Days</option>
            </select>
          </div>
          <div class="filter-field" style="flex:1.4;">
            <label>Search Keyword Filter</label>
            <input type="text" id="tb-search" class="filter-input" placeholder="🔍 Filter Trend Buzz..." oninput="renderTrendBuzzTable()" />
          </div>
        </div>

        <div class="table-container" style="margin-bottom:20px;">
          <table class="erank-table">
            <thead>
              <tr>
                <th onclick="sortKeywords('rank')">Rank ⇅</th>
                <th onclick="sortKeywords('keyword')">Keywords ⇅</th>
                <th onclick="sortKeywords('search_interest')">Search Interest ⇅</th>
                <th style="text-align:center;">Search Trend</th>
                <th class="num" onclick="sortKeywords('yoy_search_trend_pct')">Change ⇅</th>
                <th class="num" onclick="sortKeywords('est_monthly_search_volume')">Avg Searches ⇅</th>
                <th class="num" onclick="sortKeywords('avg_clicks')">Avg Clicks ⇅</th>
                <th class="num" onclick="sortKeywords('avg_ctr_pct')">Avg CTR ⇅</th>
                <th class="num" onclick="sortKeywords('total_competing_listings')">Etsy Competition ⇅</th>
                <th class="num" onclick="sortKeywords('kd_score')">KD ⇅</th>
                <th class="num" onclick="sortKeywords('opportunity_score')">Opp Score ⇅</th>
              </tr>
            </thead>
            <tbody id="tb-tbody"></tbody>
          </table>
        </div>

        <div class="chart-grid-equal">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Avg Monthly Searches vs. Estimated Monthly Clicks</div>
                <div class="card-subtitle">High-intent utility keywords generate >95% multi-tab click-through rates</div>
              </div>
            </div>
            <div class="chart-box-sm">
              <canvas id="chartBuzzSearchesClicks"></canvas>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Popular Now & Active Cart Velocity by Niche (%)</div>
                <div class="card-subtitle">% of Page 1–10 listings with 'Popular Now', 'Bestseller', and 'In 20+ Carts' badges</div>
              </div>
            </div>
            <div class="chart-box-sm">
              <canvas id="chartBuzzVelocity"></canvas>
            </div>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 4: KEYWORD RESEARCH & COMPARATIVE STUDIO                         -->
      <!-- ===================================================================== -->
      <section id="view-keyword-research" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">Comparative Keyword Research & Page 1–10 Decay Studio</h1>
            <p class="page-subtitle">Compare up to 4 keywords side-by-side across radar dimensions and inspect how sales, revenue, and reviews decay from Page 1 to Page 10.</p>
          </div>
        </div>

        <div class="filter-card">
          <div class="filter-field">
            <label>Primary Keyword (A)</label>
            <select id="comp-kw-1" class="filter-select" onchange="updateKeywordComparison()"></select>
          </div>
          <div class="filter-field">
            <label>Comparison Keyword (B)</label>
            <select id="comp-kw-2" class="filter-select" onchange="updateKeywordComparison()"></select>
          </div>
          <div class="filter-field">
            <label>Comparison Keyword (C)</label>
            <select id="comp-kw-3" class="filter-select" onchange="updateKeywordComparison()"></select>
          </div>
          <div class="filter-field">
            <label>Page 1–10 Decay Metric</label>
            <select id="comp-decay-metric" class="filter-select" onchange="updateKeywordComparison()">
              <option value="avg_revenue">Avg Estimated Revenue ($ USD) by Page</option>
              <option value="avg_sales">Avg Estimated Unit Sales by Page</option>
              <option value="avg_reviews">Avg Item Reviews by Page</option>
              <option value="ad_pct">Paid Etsy Ad Saturation (%) by Page</option>
            </select>
          </div>
        </div>

        <div class="chart-grid-2">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Page 1 to Page 10 Search Rank Decay Curve</div>
                <div class="card-subtitle">Visualizing performance drop-off across the first 10 Etsy search result pages</div>
              </div>
            </div>
            <div class="chart-box">
              <canvas id="chartPageDecay"></canvas>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Multi-Keyword Strategic Radar Comparison</div>
                <div class="card-subtitle">Normalized 0–100 benchmark across 6 core profitability dimensions</div>
              </div>
            </div>
            <div class="chart-box">
              <canvas id="chartKeywordRadar"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="card-title">Side-by-Side Keyword Comparison Matrix</div>
          </div>
          <div class="table-container">
            <table class="erank-table" id="kw-compare-table">
              <thead id="kw-compare-thead"></thead>
              <tbody id="kw-compare-tbody"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 5: COMPETITOR RESEARCH (180 STORES BENCHMARKING)                 -->
      <!-- ===================================================================== -->
      <section id="view-competitor-research" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">Competitor Store Performance & Market Share</h1>
            <p class="page-subtitle">Benchmarking 180 digital product stores captured across Pages 1–10: listing saturation, review volume, estimated unit sales, and gross revenue.</p>
          </div>
        </div>

        <div class="filter-card">
          <div class="filter-field" style="flex:1.4;">
            <label>Search Shop Name</label>
            <input type="text" id="store-search-input" class="filter-input" placeholder="🔍 Search shop name..." oninput="renderStoresView()" />
          </div>
          <div class="filter-field">
            <label>Primary Niche Keyword</label>
            <select id="store-kw-filter" class="filter-select" onchange="renderStoresView()">
              <option value="ALL">All Keywords</option>
            </select>
          </div>
          <div class="filter-field">
            <label>Store Tier</label>
            <select id="store-tier-filter" class="filter-select" onchange="renderStoresView()">
              <option value="ALL">All Store Tiers</option>
              <option value="Tier 1">Tier 1: Market Leaders</option>
              <option value="Tier 2">Tier 2: Rising Challengers</option>
              <option value="Tier 3">Tier 3: Niche Specialists</option>
            </select>
          </div>
          <div class="filter-field" style="flex:0.7;">
            <label>Star Seller</label>
            <select id="store-star-filter" class="filter-select" onchange="renderStoresView()">
              <option value="ALL">All Stores</option>
              <option value="STAR">⭐ Star Sellers Only</option>
            </select>
          </div>
        </div>

        <div class="chart-grid-equal">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Top 12Filtered Stores by Estimated Gross Revenue ($ USD)</div>
                <div class="card-subtitle">Aggregated across listings ranked in Pages 1–10</div>
              </div>
            </div>
            <div class="chart-box-sm">
              <canvas id="chartTopStoresRevenue"></canvas>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Store Efficiency: Top-10p Listings Count vs. Avg Revenue per Listing</div>
                <div class="card-subtitle">Identifies high-efficiency boutique stores vs. high-volume catalog mills</div>
              </div>
            </div>
            <div class="chart-box-sm">
              <canvas id="chartStoreEfficiency"></canvas>
            </div>
          </div>
        </div>

        <div class="table-container">
          <table class="erank-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Shop Name</th>
                <th>Primary Niche Keyword</th>
                <th class="num">Top-10p Listings</th>
                <th class="num">Best Page</th>
                <th class="num">Avg Price ($)</th>
                <th class="num">Avg Rating</th>
                <th class="num">Captured Reviews</th>
                <th class="num">Est. Unit Sales</th>
                <th class="num">Est. Gross Revenue ($)</th>
                <th class="num">Rev / Listing ($)</th>
                <th>Store Tier</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="store-tbody"></tbody>
          </table>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 6: LISTING OPTIMIZATION, 4,000-LISTING EXPLORER & ML CLUSTERS    -->
      <!-- ===================================================================== -->
      <section id="view-listing-optimization" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">Listing Explorer, Unsupervised ML Clusters & Profit Calculator</h1>
            <p class="page-subtitle">Explore all 4,000 scraped listings across Pages 1–10, inspect K-Means / 2D PCA market segments, and calculate digital unit economics.</p>
          </div>
        </div>

        <div class="chart-grid-2">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">2D PCA Machine Learning Cluster Projection (Standardized Features)</div>
                <div class="card-subtitle" id="ml-cluster-subtitle">K-Means Segmentation optimized via Silhouette Score</div>
              </div>
              <select id="pca-color-mode" class="filter-select" style="width:200px;height:30px;" onchange="renderPCAChart()">
                <option value="cluster_persona">Color by: ML Cluster Persona</option>
                <option value="category">Color by: Product Category</option>
              </select>
            </div>
            <div class="chart-box">
              <canvas id="chartPCAScatter"></canvas>
            </div>
          </div>

          <!-- Digital Listing Profit & Fee Calculator -->
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">🧮 Etsy Digital Product Margin & Share-and-Save Calculator</div>
                <div class="card-subtitle">Simulate Etsy transaction fees, 4% Share & Save rebate, and paid ad ROAS</div>
              </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div class="filter-field">
                <label>Listing Retail Price ($)</label>
                <input type="number" id="calc-price" class="filter-input" value="27.00" step="0.5" oninput="runProfitCalculator()" />
              </div>
              <div class="filter-field">
                <label>Sale Discount (%)</label>
                <input type="number" id="calc-discount" class="filter-input" value="20" step="5" oninput="runProfitCalculator()" />
              </div>
              <div class="filter-field">
                <label>Traffic Source / Fee Mode</label>
                <select id="calc-traffic-mode" class="filter-select" onchange="runProfitCalculator()">
                  <option value="share_save">Pinterest w/ Etsy Share & Save (-4% Fee Rebate)</option>
                  <option value="standard">Standard Etsy Search (~10.5% Total Fees)</option>
                  <option value="offsite_ads">Etsy Offsite Ads (+15% Attributed Fee)</option>
                </select>
              </div>
              <div class="filter-field">
                <label>Est. Monthly Unit Sales</label>
                <input type="number" id="calc-monthly-sales" class="filter-input" value="85" step="5" oninput="runProfitCalculator()" />
              </div>
            </div>
            <div id="calc-results-box" style="margin-top:14px;background:#f4f8f6;border:1px solid #cde3d8;border-radius:8px;padding:14px;"></div>
          </div>
        </div>

        <!-- 4,000-Listing Interactive Filter Bar -->
        <div class="filter-card">
          <div class="filter-field" style="flex:1.4;">
            <label>Search Listing Title or Shop</label>
            <input type="text" id="list-search" class="filter-input" placeholder="🔍 e.g. ADHD, GoodNotes, LLC, Bundle..." oninput="resetAndRenderListings()" />
          </div>
          <div class="filter-field">
            <label>Keyword Niche</label>
            <select id="list-kw-filter" class="filter-select" onchange="resetAndRenderListings()">
              <option value="ALL">All Keywords (4,000)</option>
            </select>
          </div>
          <div class="filter-field" style="flex:0.7;">
            <label>Search Page (1–10)</label>
            <select id="list-page-filter" class="filter-select" onchange="resetAndRenderListings()">
              <option value="ALL">Pages 1–10 (All)</option>
              <option value="1">Page 1 Only</option>
              <option value="2">Page 2 Only</option>
              <option value="3">Page 3 Only</option>
              <option value="1-3">Pages 1–3 (Top Fold)</option>
              <option value="8-10">Pages 8–10 (Long Tail)</option>
            </select>
          </div>
          <div class="filter-field" style="flex:0.8;">
            <label>Badge Filter</label>
            <select id="list-badge-filter" class="filter-select" onchange="resetAndRenderListings()">
              <option value="ALL">All Listings</option>
              <option value="TRENDING">🔥 Bestseller or Popular Now</option>
              <option value="BESTSELLER">🏆 Bestseller Only</option>
              <option value="POPULAR">⚡ Popular Now Only</option>
              <option value="ORGANIC">🌿 Organic Only (No Ads)</option>
            </select>
          </div>
          <div class="filter-field" style="flex:0.9;">
            <label>Sort By</label>
            <select id="list-sort-by" class="filter-select" onchange="resetAndRenderListings()">
              <option value="listing_opportunity_index">Opportunity Index (High → Low)</option>
              <option value="estimated_revenue">Est. Gross Revenue (High → Low)</option>
              <option value="estimated_sales">Est. Unit Sales (High → Low)</option>
              <option value="reviews_count">Review Count (High → Low)</option>
              <option value="price_desc">Price (High → Low)</option>
              <option value="price_asc">Price (Low → High)</option>
            </select>
          </div>
        </div>

        <div class="card" style="padding:12px 18px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;">
          <div id="listings-count-label" style="font-size:13px;font-weight:600;color:var(--text-secondary);">Showing 1–50 of 4,000 listings</div>
          <div style="display:flex;gap:8px;align-items:center;">
            <button class="btn-outline" onclick="changeListingPage(-1)">◀ Prev 50</button>
            <span id="listings-page-indicator" style="font-size:12.5px;font-weight:700;padding:0 8px;">Page 1</span>
            <button class="btn-outline" onclick="changeListingPage(1)">Next 50 ▶</button>
          </div>
        </div>

        <div class="table-container">
          <table class="erank-table">
            <thead>
              <tr>
                <th>Page #</th>
                <th>Listing Title & Archetype</th>
                <th>Keyword</th>
                <th>Shop Name</th>
                <th>Badges & Signals</th>
                <th class="num">Price ($)</th>
                <th class="num">Rating</th>
                <th class="num">Reviews</th>
                <th class="num">Est. Sales</th>
                <th class="num">Est. Revenue ($)</th>
                <th class="num">Opp Index</th>
              </tr>
            </thead>
            <tbody id="listings-tbody"></tbody>
          </table>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 7: PINTEREST AD STUDIO & SHOP INSIGHTS                           -->
      <!-- ===================================================================== -->
      <section id="view-shop-insights" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">📌 Pinterest Marketing & Paid Advertising Studio</h1>
            <p class="page-subtitle">Calibrate bundle pricing, Target CPA, and Max CPC with Etsy's 4% Share & Save rebate, and deploy niche-specific 9:16 Pin playbooks.</p>
          </div>
        </div>

        <!-- Interactive Pinterest Paid Ads & ROAS Simulator -->
        <div class="filter-card" style="background:#f2f8f5;border-color:#b8decb;">
          <div class="filter-field">
            <label>Target ROAS Goal (e.g., 2.8x)</label>
            <input type="number" id="pin-roas-input" class="filter-input" value="2.8" step="0.2" min="1.2" max="6.0" oninput="renderPinterestView()" />
          </div>
          <div class="filter-field">
            <label>Landing Page Conversion Rate (%)</label>
            <input type="number" id="pin-cvr-input" class="filter-input" value="2.4" step="0.2" min="0.5" max="8.0" oninput="renderPinterestView()" />
          </div>
          <div class="filter-field">
            <label>Bundle Price Multiplier vs. Avg Price</label>
            <input type="number" id="pin-bundle-mult" class="filter-input" value="1.45" step="0.05" min="1.0" max="3.0" oninput="renderPinterestView()" />
          </div>
          <div class="filter-field">
            <label>Daily Pinterest Ad Budget ($ USD)</label>
            <input type="number" id="pin-daily-budget" class="filter-input" value="35" step="5" min="5" max="500" oninput="renderPinterestView()" />
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Dynamic Pinterest Paid Ad Unit Economics by Keyword</div>
              <div class="card-subtitle">Adjust the sliders above to recalculate Target CPA, Max Profitable CPC, and Daily Projected Revenue</div>
            </div>
          </div>
          <div class="table-container">
            <table class="erank-table">
              <thead>
                <tr>
                  <th>Keyword</th>
                  <th class="num">Current Etsy Avg ($)</th>
                  <th class="num">Target Bundle AOV ($)</th>
                  <th class="num">Net Margin (93.5%)</th>
                  <th class="num">Target CPA ($)</th>
                  <th class="num">Max Profitable CPC ($)</th>
                  <th class="num">Est. Daily Clicks</th>
                  <th class="num">Est. Daily Revenue ($)</th>
                  <th>Recommended Campaign Priority</th>
                </tr>
              </thead>
              <tbody id="pinterest-econ-tbody"></tbody>
            </table>
          </div>
        </div>

        <h2 style="font-size:18px;font-weight:700;margin:22px 0 12px 0;">Actionable Pinterest Creative, Board & Funnel Playbooks</h2>
        <div class="playbook-grid" id="pinterest-playbook-grid"></div>
      </section>

      <!-- ===================================================================== -->
      <!-- VIEW 8: DESIGN INSPIRATION & METHODOLOGY                              -->
      <!-- ===================================================================== -->
      <section id="view-reference-design" class="view-panel">
        <div class="page-header">
          <div>
            <h1 class="page-title">🎨 Design Alignment & Analytical Methodology</h1>
            <p class="page-subtitle">How this standalone application integrates your eRank visual references with Python Selenium scraping & unsupervised ML.</p>
          </div>
        </div>

        <div class="chart-grid-equal">
          <div class="card">
            <div class="card-header">
              <div class="card-title">1. eRank Reference Integration (Monthly Trends & Trend Buzz)</div>
            </div>
            <p style="font-size:13.5px;line-height:1.65;color:var(--text-secondary);">
              Designed directly from your uploaded <strong>eRank Monthly Trends</strong> and <strong>Trend Buzz</strong> reference interfaces:
            </p>
            <ul style="margin:12px 0 0 18px;font-size:13.5px;line-height:1.75;color:var(--text-primary);">
              <li><strong>Deep Forest Green Navigation Sidebar (<code>#064428</code>):</strong> Mirrors eRank's information hierarchy (<em>Dashboard, Keyword Research, Competitor Research, Listing Optimization, Shop Insights, Trends → Trend Buzz & Monthly Trends</em>).</li>
              <li><strong>Inline 12-Month Trend Graph Sparklines:</strong> Every keyword row renders a 12-bar monthly seasonality histogram with highlighted current-month bar and peak search label underneath.</li>
              <li><strong>Trend Buzz Multi-Metric Columns:</strong> Computes <em>Search Interest, Search Trend, Change %, Avg Searches, Avg Clicks, Avg CTR %, Etsy Competition</em> (color-coded bar), and <em>Keyword Difficulty (KD)</em>.</li>
              <li><strong>Global Top Search & Live Scraper Trigger:</strong> Filter any table instantaneously or launch a 10-page Python scrape for any new digital product keyword.</li>
            </ul>
          </div>

          <div class="card">
            <div class="card-header">
              <div class="card-title">2. Analytical Enhancements Beyond Excel</div>
            </div>
            <ul style="margin:4px 0 0 18px;font-size:13.5px;line-height:1.75;color:var(--text-primary);">
              <li><strong>Page 1 to Page 10 Rank Decay Curves:</strong> Dynamically compare how unit sales, revenue, review density, and paid ad saturation decay from Page 1 to Page 10 across up to 3 keywords simultaneously.</li>
              <li><strong>Unsupervised Machine Learning (K-Means + 2D PCA):</strong> Standardizes 6 listing features (<code>StandardScaler</code>), optimizes cluster count via <strong>Silhouette Score</strong>, and projects all 4,000 listings into an interactive 2D Principal Component scatterplot.</li>
              <li><strong>Interactive Pinterest ROAS & Share-and-Save Simulator:</strong> Real-time unit economics modeling that accounts for Etsy's <code>4%</code> Share & Save fee rebate and calculates maximum profitable CPCs for paid Pinterest traffic.</li>
            </ul>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- ================= MODAL: STORE / KEYWORD DEEP-DIVE OR LIVE SCRAPER ================= -->
  <div class="modal-backdrop" id="app-modal" onclick="if(event.target===this) closeModal()">
    <div class="modal-dialog">
      <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #dce3e0;padding-bottom:12px;margin-bottom:16px;">
        <h3 id="modal-title" style="font-size:18px;font-weight:700;">Details</h3>
        <button class="btn-outline" onclick="closeModal()">✕ Close</button>
      </div>
      <div id="modal-body"></div>
    </div>
  </div>

  <!-- ================= EMBEDDED APPLICATION DATA & INTERACTIVE JS ENGINE ================= -->
  <script>
    const APP_DATA = {json_payload};

    let currentSortKey = 'opportunity_score';
    let currentSortAsc = false;
    let starredKeywords = new Set(['faceless digital marketing guide', 'notion template adhd', 'small business bookkeeping spreadsheet']);
    let selectedSeasonalityKeyword = APP_DATA.keywords[0]?.keyword || 'faceless digital marketing guide';
    let currentListingPage = 1;
    const LISTINGS_PER_PAGE = 50;

    // Chart.js instances registry
    const charts = {{}};

    function fmtNum(n) {{
      return Number(n || 0).toLocaleString('en-US', {{ maximumFractionDigits: 0 }});
    }}

    function fmtUsd(n) {{
      return '$' + Number(n || 0).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function getCompBadge(score, level) {{
      const s = Number(score);
      if (s < 35) return `<span class="badge-pill badge-low">${{s.toFixed(1)}} (${{level || 'Low'}})</span>`;
      if (s < 65) return `<span class="badge-pill badge-mod">${{s.toFixed(1)}} (${{level || 'Moderate'}})</span>`;
      return `<span class="badge-pill badge-high">${{s.toFixed(1)}} (${{level || 'High'}})</span>`;
    }}

    function getOppBadge(score) {{
      const s = Number(score);
      if (s >= 68) return `<span class="badge-pill badge-low" style="font-size:12.5px;">💎 ${{s.toFixed(1)}}</span>`;
      if (s >= 45) return `<span class="badge-pill badge-mod" style="font-size:12.5px;">${{s.toFixed(1)}}</span>`;
      return `<span class="badge-pill badge-high" style="font-size:12.5px;">${{s.toFixed(1)}}</span>`;
    }}

    function buildSparklineHTML(kwObj) {{
      const series = kwObj.monthly_trend_12m || [];
      if (!series.length) return '';
      const maxVal = Math.max(...series.map(d => d.searches), 1);
      const barsHtml = series.map((d, idx) => {{
        const heightPct = Math.max(10, Math.round((d.searches / maxVal) * 100));
        let cls = 'spark-bar';
        if (idx === series.length - 1) cls += ' current';
        else if (d.searches === maxVal) cls += ' peak';
        return `<div class="${{cls}}" style="height:${{heightPct}}%" title="${{d.month}}: ${{fmtNum(d.searches)}} searches"></div>`;
      }}).join('');

      const lastEntry = series[series.length - 1];
      return `
        <div class="sparkline-wrapper">
          <div class="sparkline-bars">${{barsHtml}}</div>
          <div class="sparkline-caption">
            <span>🔍 ${{lastEntry.month}}</span>
            <span>${{fmtNum(lastEntry.searches)}}</span>
          </div>
        </div>
      `;
    }}

    function toggleTrendsMenu() {{
      const sub = document.getElementById('trends-submenu');
      const chev = document.getElementById('trends-chevron');
      if (sub.style.display === 'none') {{
        sub.style.display = 'block';
        chev.textContent = '▴';
      }} else {{
        sub.style.display = 'none';
        chev.textContent = '▾';
      }}
    }}

    function switchView(viewId) {{
      document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
      const target = document.getElementById('view-' + viewId);
      if (target) target.classList.add('active');

      document.querySelectorAll('.nav-item, .nav-subitem').forEach(el => {{
        if (el.getAttribute('data-view') === viewId) el.classList.add('active');
        else el.classList.remove('active');
      }});

      // Trigger chart resize / initialization for active view
      if (viewId === 'dashboard') initDashboardCharts();
      if (viewId === 'monthly-trends') {{
        renderMonthlyTrendsTable();
        renderSeasonalityChart(selectedSeasonalityKeyword);
      }}
      if (viewId === 'trend-buzz') {{
        renderTrendBuzzTable();
        initTrendBuzzCharts();
      }}
      if (viewId === 'keyword-research') updateKeywordComparison();
      if (viewId === 'competitor-research') renderStoresView();
      if (viewId === 'listing-optimization') {{
        renderPCAChart();
        runProfitCalculator();
        renderListingsTable();
      }}
      if (viewId === 'shop-insights') renderPinterestView();
    }}

    // ================= INITIALIZATION =================
    function initApp() {{
      populateDropdowns();
      renderDashboardKPIs();
      renderDashboardTable();
      initDashboardCharts();
      renderMonthlyTrendsTable();
      renderTrendBuzzTable();
      runProfitCalculator();
    }}

    function populateDropdowns() {{
      const kws = APP_DATA.keywords.map(k => k.keyword);
      const cats = [...new Set(APP_DATA.keywords.map(k => k.category))];

      const catSelect = document.getElementById('mt-category-select');
      catSelect.innerHTML = '<option value="ALL">All Categories</option>' +
        cats.map(c => `<option value="${{c}}">${{c}}</option>`).join('');

      const storeKw = document.getElementById('store-kw-filter');
      const listKw = document.getElementById('list-kw-filter');
      const kwOptions = '<option value="ALL">All Keywords</option>' +
        kws.map(k => `<option value="${{k}}">${{k}}</option>`).join('');
      storeKw.innerHTML = kwOptions;
      listKw.innerHTML = kwOptions;

      // Populate comparator dropdowns
      ['comp-kw-1', 'comp-kw-2', 'comp-kw-3'].forEach((id, idx) => {{
        const sel = document.getElementById(id);
        sel.innerHTML = kws.map((k, i) => `<option value="${{k}}" ${{i === idx ? 'selected' : ''}}>${{k}}</option>`).join('');
      }});

      document.getElementById('topbar-kw-count').textContent =
        `${{APP_DATA.kpis.total_keywords}} Keywords (${{fmtNum(APP_DATA.kpis.total_listings_scraped)}} Listings)`;
      document.getElementById('sidebar-corpus-status').textContent =
        `${{fmtNum(APP_DATA.kpis.total_listings_scraped)}} Listings · ${{APP_DATA.kpis.total_unique_stores}} Stores`;
    }}

    // ================= VIEW 1: DASHBOARD =================
    function renderDashboardKPIs() {{
      const k = APP_DATA.kpis;
      const grid = document.getElementById('dashboard-kpi-grid');
      grid.innerHTML = `
        <div class="kpi-card">
          <div class="kpi-label">Scraped Digital Listings</div>
          <div class="kpi-value">${{fmtNum(k.total_listings_scraped)}}</div>
          <div class="kpi-sub">${{k.pages_per_keyword}} Pages × ${{k.total_keywords}} Keywords</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Monthly Search Volume</div>
          <div class="kpi-value">${{fmtNum(k.total_market_monthly_searches)}}</div>
          <div class="kpi-sub">Across Tracked Digital Niches</div>
        </div>
        <div class="kpi-card orange">
          <div class="kpi-label">Top Opportunity Niche</div>
          <div class="kpi-value" style="font-size:17px;line-height:1.3;">${{k.top_opportunity_keyword}}</div>
          <div class="kpi-sub">Opportunity Score: ${{k.top_opportunity_score}}/100</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Blue-Ocean Keywords</div>
          <div class="kpi-value">${{k.blue_ocean_keywords_count}} / ${{k.total_keywords}}</div>
          <div class="kpi-sub">High Demand · Low Competition</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Competitor Stores Ranked</div>
          <div class="kpi-value">${{fmtNum(k.total_unique_stores)}}</div>
          <div class="kpi-sub">Benchmarked Across Pages 1–10</div>
        </div>
      `;
    }}

    function sortKeywords(key) {{
      if (currentSortKey === key) currentSortAsc = !currentSortAsc;
      else {{
        currentSortKey = key;
        currentSortAsc = (key === 'keyword' || key === 'rank');
      }}
      APP_DATA.keywords.sort((a, b) => {{
        const va = a[key], vb = b[key];
        if (typeof va === 'string') return currentSortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
        return currentSortAsc ? (va - vb) : (vb - va);
      }});
      renderDashboardTable();
      renderMonthlyTrendsTable();
      renderTrendBuzzTable();
    }}

    function renderDashboardTable() {{
      const filterTxt = (document.getElementById('dash-kw-filter')?.value || '').toLowerCase();
      const tbody = document.getElementById('dashboard-kw-tbody');
      const rows = APP_DATA.keywords.filter(k => k.keyword.toLowerCase().includes(filterTxt));

      tbody.innerHTML = rows.map(k => `
        <tr onclick="inspectKeywordModal('${{k.keyword}}')" style="cursor:pointer;">
          <td><strong>${{k.rank}}</strong></td>
          <td>
            <span class="kw-cell">
              ${{k.keyword}} ${{k.is_hot ? '<span title="Popular Yesterday">🔥</span>' : ''}}
            </span>
          </td>
          <td>${{buildSparklineHTML(k)}}</td>
          <td class="num"><strong>${{fmtNum(k.est_monthly_search_volume)}}</strong></td>
          <td class="num" style="color:${{k.yoy_search_trend_pct >= 0 ? '#0b6e40' : '#c0392b'}};font-weight:700;">
            ${{k.yoy_search_trend_pct >= 0 ? '+' : ''}}${{k.yoy_search_trend_pct.toFixed(1)}}%
          </td>
          <td class="num">${{fmtNum(k.total_competing_listings)}}</td>
          <td class="num">${{fmtUsd(k.avg_price_usd)}}</td>
          <td class="num"><strong>${{fmtUsd(k.avg_est_revenue_per_listing_usd)}}</strong></td>
          <td class="num">${{k.demand_score.toFixed(1)}}</td>
          <td class="num">${{getCompBadge(k.competition_score, k.competition_level)}}</td>
          <td class="num">${{getOppBadge(k.opportunity_score)}}</td>
          <td style="font-size:12px;font-weight:600;">${{k.niche_classification}}</td>
        </tr>
      `).join('');
    }}

    function initDashboardCharts() {{
      const ctx1 = document.getElementById('chartOpportunityMatrix');
      if (charts.oppMatrix) charts.oppMatrix.destroy();

      const bubblePoints = APP_DATA.keywords.map(k => ({{
        x: k.competition_score,
        y: k.demand_score,
        r: Math.max(8, Math.min(26, Math.sqrt(k.est_monthly_search_volume) / 12)),
        keyword: k.keyword,
        opp: k.opportunity_score,
        vol: k.est_monthly_search_volume,
        compListings: k.total_competing_listings
      }}));

      charts.oppMatrix = new Chart(ctx1, {{
        type: 'bubble',
        data: {{
          datasets: [{{
            label: 'Digital Product Keywords',
            data: bubblePoints,
            backgroundColor: bubblePoints.map(p =>
              p.opp >= 68 ? 'rgba(14, 107, 64, 0.78)' :
              p.opp >= 45 ? 'rgba(229, 124, 35, 0.78)' : 'rgba(192, 57, 43, 0.72)'
            ),
            borderColor: '#064428',
            borderWidth: 1.5
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          onClick: (evt, elements) => {{
            if (elements.length > 0) {{
              const idx = elements[0].index;
              inspectKeywordModal(bubblePoints[idx].keyword);
            }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => {{
                  const raw = ctx.raw;
                  return [
                    `Keyword: ${{raw.keyword}}`,
                    `Opportunity Score: ${{raw.opp}}/100`,
                    `Demand Score: ${{raw.y}} | Competition Score: ${{raw.x}}`,
                    `Monthly Searches: ${{fmtNum(raw.vol)}} | Listings: ${{fmtNum(raw.compListings)}}`
                  ];
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{ display: true, text: 'Competition Score (Lower = Easier Entry)', font: {{ weight: 'bold' }} }},
              min: 0,
              max: 105
            }},
            y: {{
              title: {{ display: true, text: 'Demand Score (Higher = Stronger Velocity & Revenue)', font: {{ weight: 'bold' }} }},
              min: 15,
              max: 90
            }}
          }}
        }}
      }});

      const ctx2 = document.getElementById('chartRevenueVsAds');
      if (charts.revAds) charts.revAds.destroy();

      const labels = APP_DATA.keywords.map(k => k.keyword.length > 22 ? k.keyword.slice(0, 22) + '…' : k.keyword);
      charts.revAds = new Chart(ctx2, {{
        type: 'bar',
        data: {{
          labels,
          datasets: [
            {{
              label: 'Avg Est. Revenue / Listing ($)',
              data: APP_DATA.keywords.map(k => k.avg_est_revenue_per_listing_usd),
              backgroundColor: 'rgba(19, 122, 75, 0.82)',
              yAxisID: 'y'
            }},
            {{
              label: 'Ad Saturation (%)',
              data: APP_DATA.keywords.map(k => k.ad_saturation_pct),
              type: 'line',
              borderColor: '#e57c23',
              backgroundColor: '#e57c23',
              borderWidth: 2.5,
              yAxisID: 'y1'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ position: 'left', title: {{ display: true, text: 'Avg Revenue / Listing ($)' }} }},
            y1: {{ position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Ad Density (%)' }} }}
          }}
        }}
      }});
    }}

    // ================= VIEW 2: MONTHLY TRENDS (Screenshot 1) =================
    function toggleStar(evt, kw) {{
      evt.stopPropagation();
      if (starredKeywords.has(kw)) starredKeywords.delete(kw);
      else starredKeywords.add(kw);
      renderMonthlyTrendsTable();
    }}

    function renderMonthlyTrendsTable() {{
      const txt = (document.getElementById('mt-filter-input')?.value || '').toLowerCase();
      const cat = document.getElementById('mt-category-select')?.value || 'ALL';
      const quick = document.getElementById('mt-hot-select')?.value || 'ALL';

      const rows = APP_DATA.keywords.filter(k => {{
        if (txt && !k.keyword.toLowerCase().includes(txt)) return false;
        if (cat !== 'ALL' && k.category !== cat) return false;
        if (quick === 'HOT' && !k.is_hot) return false;
        if (quick === 'BLUE' && k.competition_score >= 48) return false;
        if (quick === 'STAR' && !starredKeywords.has(k.keyword)) return false;
        return true;
      }});

      const tbody = document.getElementById('mt-tbody');
      tbody.innerHTML = rows.map((k, idx) => {{
        const isStar = starredKeywords.has(k.keyword);
        return `
          <tr onclick="selectMonthlyTrendKeyword('${{k.keyword}}')" style="cursor:pointer;">
            <td>
              <span class="star-btn ${{isStar ? 'starred' : ''}}" onclick="toggleStar(event, '${{k.keyword}}')">${{isStar ? '★' : '☆'}}</span>
              <strong>${{idx + 1}}</strong>
            </td>
            <td>
              <span class="kw-cell">
                ${{k.keyword}} ${{k.is_hot ? '<span title="Popular Yesterday">🔥</span>' : ''}}
              </span>
            </td>
            <td style="color:var(--text-secondary);font-size:12px;">${{k.category}}</td>
            <td style="text-align:center;">${{buildSparklineHTML(k)}}</td>
            <td class="num" style="font-size:14px;font-weight:700;">${{fmtNum(k.est_monthly_search_volume)}}</td>
            <td class="num" style="color:${{k.yoy_search_trend_pct >= 0 ? '#0b6e40' : '#c0392b'}};font-weight:700;">
              ${{k.yoy_search_trend_pct >= 0 ? '+' : ''}}${{k.yoy_search_trend_pct.toFixed(1)}}%
            </td>
            <td class="num">${{fmtNum(k.total_competing_listings)}}</td>
            <td class="num">${{fmtUsd(k.avg_price_usd)}}</td>
            <td class="num"><strong>${{fmtUsd(k.avg_est_revenue_per_listing_usd)}}</strong></td>
            <td class="num">${{getOppBadge(k.opportunity_score)}}</td>
          </tr>
        `;
      }}).join('');
    }}

    function selectMonthlyTrendKeyword(kw) {{
      selectedSeasonalityKeyword = kw;
      renderSeasonalityChart(kw);
    }}

    function renderSeasonalityChart(kw) {{
      const kwObj = APP_DATA.keywords.find(k => k.keyword === kw) || APP_DATA.keywords[0];
      if (!kwObj) return;
      document.getElementById('mt-detail-chart-title').textContent =
        `12-Month Search Volume Trajectory: "${{kwObj.keyword}}" (Peak: ${{kwObj.peak_month}} — ${{fmtNum(kwObj.peak_searches)}} searches)`;

      const ctx = document.getElementById('chartMonthlySeasonality');
      if (charts.seasonality) charts.seasonality.destroy();

      const series = kwObj.monthly_trend_12m || [];
      charts.seasonality = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: series.map(d => d.month),
          datasets: [{{
            label: `Monthly Searches (${{kwObj.keyword}})`,
            data: series.map(d => d.searches),
            backgroundColor: series.map((d, i) => i === series.length - 1 ? '#064428' : '#2e8b57'),
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ beginAtZero: true, title: {{ display: true, text: 'Monthly Searches' }} }}
          }}
        }}
      }});
    }}

    // ================= VIEW 3: TREND BUZZ (Screenshot 2) =================
    function renderTrendBuzzTable() {{
      const txt = (document.getElementById('tb-search')?.value || '').toLowerCase();
      const tf = document.getElementById('tb-timeframe')?.value || 'Yesterday';
      const mult = tf === 'Yesterday' ? 1.0 : (tf === 'Past 7 Days' ? 1.04 : 1.0);

      const rows = APP_DATA.keywords.filter(k => k.keyword.toLowerCase().includes(txt));
      const tbody = document.getElementById('tb-tbody');

      tbody.innerHTML = rows.map((k, idx) => {{
        const compScore = k.competition_score;
        const barColor = compScore < 35 ? '#137a4b' : (compScore < 65 ? '#e57c23' : '#d9381e');
        return `
          <tr onclick="inspectKeywordModal('${{k.keyword}}')" style="cursor:pointer;">
            <td><strong>#${{idx + 1}}</strong></td>
            <td>
              <span class="kw-cell">
                ${{k.keyword}} ${{k.is_hot ? '🔥' : ''}}
              </span>
            </td>
            <td>
              <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:75px;height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden;">
                  <div style="width:${{k.search_interest}}%;height:100%;background:#0e6b40;"></div>
                </div>
                <span style="font-size:12px;font-weight:700;">${{k.search_interest}}</span>
              </div>
            </td>
            <td style="text-align:center;">${{buildSparklineHTML(k)}}</td>
            <td class="num" style="color:${{k.yoy_search_trend_pct >= 0 ? '#0b6e40' : '#c0392b'}};font-weight:700;">
              ${{k.yoy_search_trend_pct >= 0 ? '▲ +' : '▼ '}}${{k.yoy_search_trend_pct.toFixed(1)}}%
            </td>
            <td class="num"><strong>${{fmtNum(Math.round(k.est_monthly_search_volume * mult))}}</strong></td>
            <td class="num">${{fmtNum(Math.round(k.avg_clicks * mult))}}</td>
            <td class="num"><strong>${{k.avg_ctr_pct.toFixed(0)}}%</strong></td>
            <td class="num">
              <div class="comp-bar-wrap">
                <div class="comp-bar-fill" style="width:${{Math.min(100, compScore)}}%;background:${{barColor}};"></div>
                <span class="comp-bar-text">${{fmtNum(k.total_competing_listings)}}</span>
              </div>
            </td>
            <td class="num">${{getCompBadge(k.kd_score, k.competition_level)}}</td>
            <td class="num">${{getOppBadge(k.opportunity_score)}}</td>
          </tr>
        `;
      }}).join('');
    }}

    function initTrendBuzzCharts() {{
      const ctx1 = document.getElementById('chartBuzzSearchesClicks');
      if (charts.buzzSC) charts.buzzSC.destroy();

      const labels = APP_DATA.keywords.map(k => k.keyword.length > 18 ? k.keyword.slice(0, 18) + '…' : k.keyword);
      charts.buzzSC = new Chart(ctx1, {{
        type: 'bar',
        data: {{
          labels,
          datasets: [
            {{
              label: 'Avg Monthly Searches',
              data: APP_DATA.keywords.map(k => k.est_monthly_search_volume),
              backgroundColor: '#064428'
            }},
            {{
              label: 'Estimated Monthly Clicks',
              data: APP_DATA.keywords.map(k => k.avg_clicks),
              backgroundColor: '#4cd98c'
            }}
          ]
        }},
        options: {{ responsive: true, maintainAspectRatio: false }}
      }});

      const ctx2 = document.getElementById('chartBuzzVelocity');
      if (charts.buzzVel) charts.buzzVel.destroy();
      charts.buzzVel = new Chart(ctx2, {{
        type: 'bar',
        data: {{
          labels,
          datasets: [
            {{
              label: 'Popular Now Badge (%)',
              data: APP_DATA.keywords.map(k => k.popular_now_rate_pct),
              backgroundColor: '#e57c23'
            }},
            {{
              label: 'Bestseller Badge (%)',
              data: APP_DATA.keywords.map(k => k.bestseller_rate_pct),
              backgroundColor: '#137a4b'
            }},
            {{
              label: 'Active In-Cart Signal (%)',
              data: APP_DATA.keywords.map(k => k.active_cart_rate_pct),
              backgroundColor: '#2980b9'
            }}
          ]
        }},
        options: {{ responsive: true, maintainAspectRatio: false }}
      }});
    }}

    // ================= VIEW 4: COMPARATIVE KEYWORD STUDIO =================
    function updateKeywordComparison() {{
      const kw1 = document.getElementById('comp-kw-1')?.value;
      const kw2 = document.getElementById('comp-kw-2')?.value;
      const kw3 = document.getElementById('comp-kw-3')?.value;
      const metric = document.getElementById('comp-decay-metric')?.value || 'avg_revenue';

      const selectedKws = [kw1, kw2, kw3]
        .map(name => APP_DATA.keywords.find(k => k.keyword === name))
        .filter(Boolean);

      const colors = ['#064428', '#e57c23', '#2980b9'];

      // 1. Page 1-10 Decay Chart
      const ctxDecay = document.getElementById('chartPageDecay');
      if (charts.pageDecay) charts.pageDecay.destroy();

      charts.pageDecay = new Chart(ctxDecay, {{
        type: 'line',
        data: {{
          labels: ['Page 1', 'Page 2', 'Page 3', 'Page 4', 'Page 5', 'Page 6', 'Page 7', 'Page 8', 'Page 9', 'Page 10'],
          datasets: selectedKws.map((k, idx) => ({{
            label: k.keyword,
            data: (k.page_decay_curve || []).map(p => p[metric]),
            borderColor: colors[idx % colors.length],
            backgroundColor: colors[idx % colors.length],
            borderWidth: 2.5,
            tension: 0.25
          }}))
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ beginAtZero: true }}
          }}
        }}
      }});

      // 2. Radar Comparison Chart
      const ctxRadar = document.getElementById('chartKeywordRadar');
      if (charts.kwRadar) charts.kwRadar.destroy();

      charts.kwRadar = new Chart(ctxRadar, {{
        type: 'radar',
        data: {{
          labels: [
            'Demand Score',
            'Opportunity Score',
            'Ease of Entry (100-Comp)',
            'Price Margin Index',
            'Popular Velocity',
            'Click-Through Rate'
          ],
          datasets: selectedKws.map((k, idx) => ({{
            label: k.keyword,
            data: [
              k.demand_score,
              k.opportunity_score,
              100 - k.competition_score,
              Math.min(100, (k.avg_price_usd / 30) * 100),
              Math.min(100, k.popular_now_rate_pct * 3),
              Math.min(100, k.avg_ctr_pct - 15)
            ],
            borderColor: colors[idx % colors.length],
            backgroundColor: idx === 0 ? 'rgba(6,68,40,0.18)' : (idx === 1 ? 'rgba(229,124,35,0.18)' : 'rgba(41,128,185,0.18)'),
            borderWidth: 2
          }}))
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{ r: {{ min: 0, max: 100 }} }}
        }}
      }});

      // 3. Side-by-Side Comparison Matrix Table
      const thead = document.getElementById('kw-compare-thead');
      const tbody = document.getElementById('kw-compare-tbody');
      thead.innerHTML = `<tr><th>Metric / Dimension</th>` +
        selectedKws.map(k => `<th class="num" style="font-size:13px;color:#064428;">${{k.keyword}}</th>`).join('') + `</tr>`;

      const metricsRows = [
        ['Strategic Classification', k => k.niche_classification],
        ['Opportunity Score (0–100)', k => `<strong>${{k.opportunity_score.toFixed(1)}}</strong>`],
        ['Demand Score (0–100)', k => k.demand_score.toFixed(1)],
        ['Competition Score (0–100)', k => `${{k.competition_score.toFixed(1)}} (${{k.competition_level}})`],
        ['Est. Monthly Search Volume', k => fmtNum(k.est_monthly_search_volume)],
        ['YoY Search Trend (%)', k => `${{k.yoy_search_trend_pct >= 0 ? '+' : ''}}${{k.yoy_search_trend_pct.toFixed(1)}}%`],
        ['Total Competing Listings', k => fmtNum(k.total_competing_listings)],
        ['Average Listing Price ($)', k => fmtUsd(k.avg_price_usd)],
        ['Avg Est. Unit Sales / Listing', k => fmtNum(k.avg_est_sales_per_listing)],
        ['Avg Est. Revenue / Listing ($)', k => `<strong>${{fmtUsd(k.avg_est_revenue_per_listing_usd)}}</strong>`],
        ['Paid Etsy Ad Saturation (%)', k => `${{k.ad_saturation_pct.toFixed(1)}}%`],
        ['Top-5 Store Concentration (%)', k => `${{k.top5_store_sales_share_pct.toFixed(1)}}%`],
        ['Popular Now Badge Rate (%)', k => `${{k.popular_now_rate_pct.toFixed(1)}}%`],
        ['Bestseller Badge Rate (%)', k => `${{k.bestseller_rate_pct.toFixed(1)}}%`]
      ];

      tbody.innerHTML = metricsRows.map(([label, fn]) =>
        `<tr><td><strong>${{label}}</strong></td>` +
        selectedKws.map(k => `<td class="num">${{fn(k)}}</td>`).join('') +
        `</tr>`
      ).join('');
    }}

    // ================= VIEW 5: COMPETITOR STORES =================
    function renderStoresView() {{
      const txt = (document.getElementById('store-search-input')?.value || '').toLowerCase();
      const kw = document.getElementById('store-kw-filter')?.value || 'ALL';
      const tier = document.getElementById('store-tier-filter')?.value || 'ALL';
      const star = document.getElementById('store-star-filter')?.value || 'ALL';

      const filtered = APP_DATA.stores.filter(s => {{
        if (txt && !s.shop_name.toLowerCase().includes(txt)) return false;
        if (kw !== 'ALL' && s.primary_keyword !== kw) return false;
        if (tier !== 'ALL' && !s.store_tier.startsWith(tier)) return false;
        if (star === 'STAR' && !s.is_star_seller) return false;
        return true;
      }});

      const tbody = document.getElementById('store-tbody');
      tbody.innerHTML = filtered.slice(0, 60).map((s, idx) => `
        <tr onclick="inspectStoreModal('${{s.shop_name}}')" style="cursor:pointer;">
          <td><strong>#${{idx + 1}}</strong></td>
          <td>
            <span class="kw-cell">${{s.shop_name}}</span>
            ${{s.is_star_seller ? '<span class="tag-chip tag-starseller" style="margin-left:6px;">★ Star Seller</span>' : ''}}
          </td>
          <td><code>${{s.primary_keyword}}</code></td>
          <td class="num"><strong>${{s.top10p_listings_count}}</strong></td>
          <td class="num">Page ${{s.best_page_rank}}</td>
          <td class="num">${{fmtUsd(s.avg_listing_price_usd)}}</td>
          <td class="num">${{s.avg_star_rating.toFixed(2)}} ★</td>
          <td class="num">${{fmtNum(s.total_reviews_captured)}}</td>
          <td class="num">${{fmtNum(s.total_estimated_sales)}}</td>
          <td class="num"><strong>${{fmtUsd(s.total_estimated_revenue_usd)}}</strong></td>
          <td class="num">${{fmtUsd(s.avg_revenue_per_listing_usd)}}</td>
          <td style="font-size:11.5px;font-weight:600;">${{s.store_tier}}</td>
          <td><button class="btn-outline" style="padding:4px 8px;font-size:11px;">Inspect</button></td>
        </tr>
      `).join('');

      // Update Store Charts
      const top12 = filtered.slice(0, 12);
      const ctx1 = document.getElementById('chartTopStoresRevenue');
      if (charts.topStores) charts.topStores.destroy();
      charts.topStores = new Chart(ctx1, {{
        type: 'bar',
        data: {{
          labels: top12.map(s => s.shop_name),
          datasets: [{{
            label: 'Estimated Gross Revenue ($ USD)',
            data: top12.map(s => s.total_estimated_revenue_usd),
            backgroundColor: '#0e6b40'
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }}
        }}
      }});

      const ctx2 = document.getElementById('chartStoreEfficiency');
      if (charts.storeEff) charts.storeEff.destroy();
      charts.storeEff = new Chart(ctx2, {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: 'Competitor Stores',
            data: filtered.slice(0, 80).map(s => ({{
              x: s.top10p_listings_count,
              y: s.avg_revenue_per_listing_usd,
              shop: s.shop_name
            }})),
            backgroundColor: 'rgba(229, 124, 35, 0.75)',
            pointRadius: 5
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            tooltip: {{
              callbacks: {{
                label: (ctx) => `${{ctx.raw.shop}}: ${{ctx.raw.x}} listings | ${{fmtUsd(ctx.raw.y)}}/listing`
              }}
            }}
          }},
          scales: {{
            x: {{ title: {{ display: true, text: 'Listings Ranked in Top 10 Pages' }} }},
            y: {{ title: {{ display: true, text: 'Avg Revenue per Listing ($ USD)' }} }}
          }}
        }}
      }});
    }}

    // ================= VIEW 6: LISTING EXPLORER, ML CLUSTERS & CALCULATOR =================
    function renderPCAChart() {{
      const colorMode = document.getElementById('pca-color-mode')?.value || 'cluster_persona';
      const diag = APP_DATA.ml_diagnostics || {{}};
      document.getElementById('ml-cluster-subtitle').textContent =
        `Optimal k=${{diag.optimal_k || 6}} Clusters (Silhouette=${{diag.best_silhouette_score || 0.26}}) · Sampled from 4,000 Listings`;

      // Sample every 4th listing (1,000 points) for fast, crisp canvas rendering
      const sample = APP_DATA.listings.filter((_, i) => i % 4 === 0);
      const groups = {{}};
      sample.forEach(item => {{
        const key = item[colorMode] || 'Cluster';
        if (!groups[key]) groups[key] = [];
        groups[key].push({{
          x: item.pca_1,
          y: item.pca_2,
          title: item.title,
          kw: item.keyword,
          price: item.price,
          rev: item.estimated_revenue
        }});
      }});

      const palette = ['#064428', '#e57c23', '#2980b9', '#8e44ad', '#27ae60', '#c0392b', '#16a085', '#d35400'];
      const ctx = document.getElementById('chartPCAScatter');
      if (charts.pca) charts.pca.destroy();

      charts.pca = new Chart(ctx, {{
        type: 'scatter',
        data: {{
          datasets: Object.keys(groups).map((gKey, idx) => ({{
            label: gKey,
            data: groups[gKey],
            backgroundColor: palette[idx % palette.length] + 'BB',
            pointRadius: 4
          }}))
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            tooltip: {{
              callbacks: {{
                label: (ctx) => {{
                  const r = ctx.raw;
                  return `${{r.title.slice(0, 42)}}… (${{fmtUsd(r.price)}} | Rev: ${{fmtUsd(r.rev)}})`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ title: {{ display: true, text: 'Principal Component 1 (Demand & Velocity)' }} }},
            y: {{ title: {{ display: true, text: 'Principal Component 2 (Price Margin & Competition)' }} }}
          }}
        }}
      }});
    }}

    function runProfitCalculator() {{
      const retail = parseFloat(document.getElementById('calc-price')?.value || 27);
      const disc = parseFloat(document.getElementById('calc-discount')?.value || 20);
      const mode = document.getElementById('calc-traffic-mode')?.value || 'share_save';
      const monthlySales = parseInt(document.getElementById('calc-monthly-sales')?.value || 85, 10);

      const salePrice = retail * (1 - disc / 100);
      const listingFee = 0.20;
      const txFeePct = mode === 'share_save' ? 0.025 : (mode === 'offsite_ads' ? 0.215 : 0.065);
      const procFee = salePrice * 0.03 + 0.25;
      const totalFees = listingFee + (salePrice * txFeePct) + procFee;
      const netProfitPerSale = Math.max(0, salePrice - totalFees);
      const netMarginPct = salePrice > 0 ? (netProfitPerSale / salePrice) * 100 : 0;
      const monthlyNetProfit = netProfitPerSale * monthlySales;
      const targetCpa28x = salePrice / 2.8;

      const box = document.getElementById('calc-results-box');
      box.innerHTML = `
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center;">
          <div>
            <div style="font-size:11px;color:var(--text-secondary);font-weight:700;">EFFECTIVE SALE PRICE</div>
            <div style="font-size:18px;font-weight:800;color:var(--text-primary);margin-top:3px;">${{fmtUsd(salePrice)}}</div>
          </div>
          <div>
            <div style="font-size:11px;color:var(--text-secondary);font-weight:700;">NET PROFIT / SALE</div>
            <div style="font-size:18px;font-weight:800;color:#0b6e40;margin-top:3px;">${{fmtUsd(netProfitPerSale)}} (${{netMarginPct.toFixed(1)}}%)</div>
          </div>
          <div>
            <div style="font-size:11px;color:var(--text-secondary);font-weight:700;">ALLOWABLE PINTEREST CPA</div>
            <div style="font-size:18px;font-weight:800;color:var(--erank-orange);margin-top:3px;">${{fmtUsd(targetCpa28x)}}</div>
          </div>
          <div>
            <div style="font-size:11px;color:var(--text-secondary);font-weight:700;">EST. MONTHLY NET PROFIT</div>
            <div style="font-size:18px;font-weight:800;color:#064428;margin-top:3px;">${{fmtUsd(monthlyNetProfit)}}</div>
          </div>
        </div>
      `;
    }}

    function getFilteredListings() {{
      const txt = (document.getElementById('list-search')?.value || '').toLowerCase();
      const kw = document.getElementById('list-kw-filter')?.value || 'ALL';
      const pageFilter = document.getElementById('list-page-filter')?.value || 'ALL';
      const badge = document.getElementById('list-badge-filter')?.value || 'ALL';
      const sortBy = document.getElementById('list-sort-by')?.value || 'listing_opportunity_index';

      let rows = APP_DATA.listings.filter(item => {{
        if (txt && !item.title.toLowerCase().includes(txt) && !item.shop_name.toLowerCase().includes(txt)) return false;
        if (kw !== 'ALL' && item.keyword !== kw) return false;
        if (pageFilter === '1-3' && item.page > 3) return false;
        else if (pageFilter === '8-10' && item.page < 8) return false;
        else if (['1', '2', '3'].includes(pageFilter) && String(item.page) !== pageFilter) return false;

        if (badge === 'TRENDING' && !(item.is_bestseller || item.is_popular_now)) return false;
        if (badge === 'BESTSELLER' && !item.is_bestseller) return false;
        if (badge === 'POPULAR' && !item.is_popular_now) return false;
        if (badge === 'ORGANIC' && item.is_ad) return false;
        return true;
      }});

      rows.sort((a, b) => {{
        if (sortBy === 'price_desc') return b.price - a.price;
        if (sortBy === 'price_asc') return a.price - b.price;
        return (b[sortBy] || 0) - (a[sortBy] || 0);
      }});
      return rows;
    }}

    function resetAndRenderListings() {{
      currentListingPage = 1;
      renderListingsTable();
    }}

    function changeListingPage(delta) {{
      const rows = getFilteredListings();
      const maxPage = Math.max(1, Math.ceil(rows.length / LISTINGS_PER_PAGE));
      currentListingPage = Math.min(maxPage, Math.max(1, currentListingPage + delta));
      renderListingsTable();
    }}

    function renderListingsTable() {{
      const rows = getFilteredListings();
      const total = rows.length;
      const maxPage = Math.max(1, Math.ceil(total / LISTINGS_PER_PAGE));
      const startIdx = (currentListingPage - 1) * LISTINGS_PER_PAGE;
      const slice = rows.slice(startIdx, startIdx + LISTINGS_PER_PAGE);

      document.getElementById('listings-count-label').textContent =
        `Showing ${{total ? startIdx + 1 : 0}}–${{Math.min(total, startIdx + LISTINGS_PER_PAGE)}} of ${{fmtNum(total)}} filtered listings`;
      document.getElementById('listings-page-indicator').textContent =
        `Page ${{currentListingPage}} / ${{maxPage}}`;

      const tbody = document.getElementById('listings-tbody');
      tbody.innerHTML = slice.map(item => `
        <tr>
          <td><strong>P${{item.page}}</strong> <span style="color:var(--text-muted);font-size:11px;">(#${{item.position_on_page}})</span></td>
          <td style="max-width:310px;">
            <div style="font-weight:600;color:var(--text-primary);">${{item.title}}</div>
            <div style="font-size:11px;color:var(--text-muted);">${{item.cluster_persona}}</div>
          </td>
          <td><code>${{item.keyword}}</code></td>
          <td><span class="kw-cell" onclick="inspectStoreModal('${{item.shop_name}}')">${{item.shop_name}}</span></td>
          <td>
            ${{item.is_bestseller ? '<span class="tag-chip tag-bestseller">🏆 Bestseller</span>' : ''}}
            ${{item.is_popular_now ? '<span class="tag-chip tag-popular">🔥 Popular Now</span>' : ''}}
            ${{item.is_star_seller ? '<span class="tag-chip tag-starseller">★ Star Seller</span>' : ''}}
            ${{item.is_ad ? '<span class="tag-chip tag-ad">Ad</span>' : ''}}
            ${{item.in_carts_count > 0 ? `<span class="tag-chip" style="background:#dcfce7;color:#166534;">🛒 ${{item.in_carts_count}}+ carts</span>` : ''}}
          </td>
          <td class="num"><strong>${{fmtUsd(item.price)}}</strong></td>
          <td class="num">${{item.rating > 0 ? item.rating.toFixed(2) + ' ★' : 'New'}}</td>
          <td class="num">${{fmtNum(item.reviews_count)}}</td>
          <td class="num">${{fmtNum(item.estimated_sales)}}</td>
          <td class="num"><strong>${{fmtUsd(item.estimated_revenue)}}</strong></td>
          <td class="num">${{getOppBadge(item.listing_opportunity_index)}}</td>
        </tr>
      `).join('');
    }}

    // ================= VIEW 7: PINTEREST AD STUDIO =================
    function renderPinterestView() {{
      const roas = parseFloat(document.getElementById('pin-roas-input')?.value || 2.8);
      const cvr = parseFloat(document.getElementById('pin-cvr-input')?.value || 2.4) / 100.0;
      const mult = parseFloat(document.getElementById('pin-bundle-mult')?.value || 1.45);
      const budget = parseFloat(document.getElementById('pin-daily-budget')?.value || 35);

      const tbody = document.getElementById('pinterest-econ-tbody');
      tbody.innerHTML = APP_DATA.pinterest_strategies.map(p => {{
        const avgPrice = p.current_avg_etsy_price_usd;
        const bundleAov = Math.max(18.50, avgPrice * mult);
        const netMargin = bundleAov * 0.935;
        const targetCpa = bundleAov / roas;
        const maxCpc = Math.max(0.05, targetCpa * cvr);
        const dailyClicks = Math.round(budget / maxCpc);
        const dailyRev = dailyClicks * cvr * bundleAov;

        return `
          <tr>
            <td><strong>${{p.keyword}}</strong></td>
            <td class="num">${{fmtUsd(avgPrice)}}</td>
            <td class="num" style="color:#0b6e40;font-weight:700;">${{fmtUsd(bundleAov)}}</td>
            <td class="num">${{fmtUsd(netMargin)}}</td>
            <td class="num"><strong>${{fmtUsd(targetCpa)}}</strong></td>
            <td class="num" style="color:var(--erank-orange);font-weight:800;">${{fmtUsd(maxCpc)}}</td>
            <td class="num">${{fmtNum(dailyClicks)}} clicks/day</td>
            <td class="num"><strong>${{fmtUsd(dailyRev)}}/day</strong></td>
            <td style="font-size:12px;font-weight:600;">${{p.pinterest_campaign_priority}}</td>
          </tr>
        `;
      }}).join('');

      const grid = document.getElementById('pinterest-playbook-grid');
      grid.innerHTML = APP_DATA.pinterest_strategies.map(p => {{
        const tierCls = p.pinterest_campaign_priority.includes('Tier 1') ? 'tier1' : 'tier2';
        return `
          <div class="playbook-card ${{tierCls}}">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <h3 style="font-size:15px;font-weight:800;color:#064428;text-transform:capitalize;">📌 ${{p.keyword}}</h3>
              ${{getOppBadge(p.opportunity_score)}}
            </div>
            <div class="playbook-hook">"${{p.high_converting_pin_hook}}"</div>
            <div style="font-size:12.5px;line-height:1.65;color:var(--text-primary);">
              <div><strong>🎨 Creative Format:</strong> ${{p.optimal_pin_creative_format}}</div>
              <div><strong>🗂️ Target Boards:</strong> ${{p.target_pinterest_boards}}</div>
              <div><strong>🎯 Interest Targeting:</strong> ${{p.pinterest_interest_targeting}}</div>
              <div><strong>🚀 Funnel & Upsell:</strong> ${{p.bundle_and_lead_magnet_funnel}}</div>
              <div><strong>📅 Peak Seasonality:</strong> ${{p.peak_seasonal_window}}</div>
            </div>
          </div>
        `;
      }}).join('');
    }}

    // ================= MODALS & GLOBAL ACTIONS =================
    function inspectKeywordModal(kwName) {{
      const k = APP_DATA.keywords.find(x => x.keyword === kwName);
      const p = APP_DATA.pinterest_strategies.find(x => x.keyword === kwName);
      if (!k) return;

      const topListings = APP_DATA.listings
        .filter(l => l.keyword === kwName)
        .sort((a, b) => b.listing_opportunity_index - a.listing_opportunity_index)
        .slice(0, 6);

      document.getElementById('modal-title').textContent = `Keyword Intelligence Deep-Dive: "${{k.keyword}}"`;
      document.getElementById('modal-body').innerHTML = `
        <div class="kpi-grid" style="margin-bottom:16px;">
          <div class="kpi-card">
            <div class="kpi-label">Monthly Search Volume</div>
            <div class="kpi-value">${{fmtNum(k.est_monthly_search_volume)}}</div>
            <div class="kpi-sub">YoY Trend: ${{k.yoy_search_trend_pct >= 0 ? '+' : ''}}${{k.yoy_search_trend_pct}}%</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Competing Listings</div>
            <div class="kpi-value">${{fmtNum(k.total_competing_listings)}}</div>
            <div class="kpi-sub">Competition: ${{k.competition_score}}/100 (${{k.competition_level}})</div>
          </div>
          <div class="kpi-card orange">
            <div class="kpi-label">Opportunity Score</div>
            <div class="kpi-value">${{k.opportunity_score}}/100</div>
            <div class="kpi-sub">${{k.niche_classification}}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Target Pinterest Bundle</div>
            <div class="kpi-value">${{p ? fmtUsd(p.recommended_pinterest_bundle_price_usd) : fmtUsd(k.avg_price_usd * 1.45)}}</div>
            <div class="kpi-sub">Max CPC: ${{p ? fmtUsd(p.max_profitable_cpc_usd) : '$0.22'}}</div>
          </div>
        </div>
        <h4 style="margin:12px 0 8px 0;">Top 6 High-Opportunity Listings for "${{k.keyword}}"</h4>
        <div class="table-container">
          <table class="erank-table">
            <thead>
              <tr>
                <th>Page</th>
                <th>Listing Title</th>
                <th>Shop</th>
                <th class="num">Price</th>
                <th class="num">Reviews</th>
                <th class="num">Est. Sales</th>
                <th class="num">Est. Revenue</th>
              </tr>
            </thead>
            <tbody>
              ${{topListings.map(l => `
                <tr>
                  <td>P${{l.page}}</td>
                  <td><strong>${{l.title}}</strong></td>
                  <td>${{l.shop_name}}</td>
                  <td class="num">${{fmtUsd(l.price)}}</td>
                  <td class="num">${{fmtNum(l.reviews_count)}}</td>
                  <td class="num">${{fmtNum(l.estimated_sales)}}</td>
                  <td class="num"><strong>${{fmtUsd(l.estimated_revenue)}}</strong></td>
                </tr>
              `).join('')}}
            </tbody>
          </table>
        </div>
      `;
      document.getElementById('app-modal').classList.add('open');
    }}

    function inspectStoreModal(shopName) {{
      const s = APP_DATA.stores.find(x => x.shop_name === shopName);
      if (!s) return;
      const storeListings = APP_DATA.listings
        .filter(l => l.shop_name === shopName)
        .sort((a, b) => b.estimated_revenue - a.estimated_revenue);

      document.getElementById('modal-title').textContent = `Competitor Store Benchmark: ${{s.shop_name}}`;
      document.getElementById('modal-body').innerHTML = `
        <div class="kpi-grid" style="margin-bottom:16px;">
          <div class="kpi-card">
            <div class="kpi-label">Top-10p Listings</div>
            <div class="kpi-value">${{s.top10p_listings_count}}</div>
            <div class="kpi-sub">Best Rank: Page ${{s.best_page_rank}}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Captured Reviews</div>
            <div class="kpi-value">${{fmtNum(s.total_reviews_captured)}}</div>
            <div class="kpi-sub">Avg Rating: ${{s.avg_star_rating.toFixed(2)}} ★</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Est. Unit Sales</div>
            <div class="kpi-value">${{fmtNum(s.total_estimated_sales)}}</div>
            <div class="kpi-sub">Primary Niche: ${{s.primary_keyword}}</div>
          </div>
          <div class="kpi-card orange">
            <div class="kpi-label">Est. Gross Revenue</div>
            <div class="kpi-value">${{fmtUsd(s.total_estimated_revenue_usd)}}</div>
            <div class="kpi-sub">${{s.store_tier}}</div>
          </div>
        </div>
        <h4 style="margin:12px 0 8px 0;">Top Ranked Listings by ${{s.shop_name}} (Pages 1–10)</h4>
        <div class="table-container">
          <table class="erank-table">
            <thead>
              <tr>
                <th>Page</th>
                <th>Listing Title</th>
                <th class="num">Price</th>
                <th class="num">Reviews</th>
                <th class="num">Est. Sales</th>
                <th class="num">Est. Revenue</th>
              </tr>
            </thead>
            <tbody>
              ${{storeListings.slice(0, 10).map(l => `
                <tr>
                  <td>P${{l.page}} (#${{l.position_on_page}})</td>
                  <td><strong>${{l.title}}</strong></td>
                  <td class="num">${{fmtUsd(l.price)}}</td>
                  <td class="num">${{fmtNum(l.reviews_count)}}</td>
                  <td class="num">${{fmtNum(l.estimated_sales)}}</td>
                  <td class="num"><strong>${{fmtUsd(l.estimated_revenue)}}</strong></td>
                </tr>
              `).join('')}}
            </tbody>
          </table>
        </div>
      `;
      document.getElementById('app-modal').classList.add('open');
    }}

    function openScrapeModal() {{
      document.getElementById('modal-title').textContent = '⚡ Scrape & Analyze New Digital Product Keyword (10 Pages)';
      document.getElementById('modal-body').innerHTML = `
        <p style="font-size:13.5px;color:var(--text-secondary);margin-bottom:14px;">
          Enter any digital product keyword below. When connected to the local Python server (<code>app.py</code>), this triggers the 10-page scraper, recalculates K-Means/PCA clusters, and adds the new keyword to all charts and tables.
        </p>
        <div style="display:flex;gap:10px;margin-bottom:14px;">
          <input type="text" id="new-scrape-kw" class="filter-input" style="flex:1;" placeholder="e.g. goodnotes digital sticker book, canva media kit template..." value="goodnotes digital sticker book" />
          <select id="new-scrape-mode" class="filter-select" style="width:210px;">
            <option value="auto">Auto (Selenium + Calibrated)</option>
            <option value="benchmark">Instant 10-Page Benchmark</option>
          </select>
          <button class="btn-primary" onclick="executeLiveScrape()">🚀 Run 10-Page Scrape</button>
        </div>
        <div id="scrape-status-msg" style="font-size:13px;font-weight:600;color:#064428;"></div>
      `;
      document.getElementById('app-modal').classList.add('open');
    }}

    async function executeLiveScrape() {{
      const kwInput = document.getElementById('new-scrape-kw');
      const modeInput = document.getElementById('new-scrape-mode');
      const statusEl = document.getElementById('scrape-status-msg');
      const kw = (kwInput?.value || '').trim().toLowerCase();
      if (!kw) return;

      statusEl.textContent = `⏳ Scraping 10 result pages for "${{kw}}" and recomputing ML clusters...`;
      try {{
        const resp = await fetch('/api/scrape', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ keyword: kw, mode: modeInput?.value || 'auto' }})
        }});
        if (!resp.ok) throw new Error('Server endpoint unavailable in static file mode');
        const newData = await resp.json();
        Object.assign(APP_DATA, newData);
        initApp();
        statusEl.textContent = `✅ Successfully scraped 10 pages (400 listings) for "${{kw}}"! Dashboard updated.`;
        setTimeout(() => closeModal(), 1100);
      }} catch (err) {{
        statusEl.innerHTML = `ℹ️ Running in standalone portable HTML mode. Run <code>.\\.venv\\Scripts\\python.exe app.py</code> to enable live backend scraping, or inspect existing 4,000 listings immediately.`;
      }}
    }}

    function handleGlobalSearch() {{
      const q = (document.getElementById('global-search-input')?.value || '').trim().toLowerCase();
      if (!q) return;
      const exact = APP_DATA.keywords.find(k => k.keyword.toLowerCase().includes(q));
      if (exact) {{
        inspectKeywordModal(exact.keyword);
      }} else {{
        openScrapeModal();
        const inp = document.getElementById('new-scrape-kw');
        if (inp) inp.value = q;
      }}
    }}

    function exportCurrentCSV() {{
      const headers = ['keyword','category','est_monthly_search_volume','yoy_search_trend_pct','total_competing_listings','avg_price_usd','avg_est_revenue_per_listing_usd','demand_score','competition_score','opportunity_score','niche_classification'];
      const csvRows = [
        headers.join(','),
        ...APP_DATA.keywords.map(k => headers.map(h => JSON.stringify(k[h] ?? '')).join(','))
      ];
      const blob = new Blob([csvRows.join('\\n')], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'etsy_keyword_intelligence_export.csv';
      a.click();
    }}

    function closeModal() {{
      document.getElementById('app-modal').classList.remove('open');
    }}

    window.addEventListener('DOMContentLoaded', initApp);
  </script>
</body>
</html>
"""
