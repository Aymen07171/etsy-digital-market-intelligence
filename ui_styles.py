"""
CSS Stylesheet for the Etsy Market Intelligence Standalone Application.
Inspired by the eRank visual language (deep forest emerald sidebar, clean top search bar,
inline 12-month bar sparklines, color-coded competition & difficulty badges, and responsive
analytics cards).
"""

APP_CSS = r"""
:root {
  --erank-sidebar-bg: #064428;
  --erank-sidebar-hover: #0b5835;
  --erank-sidebar-active: #0e6b40;
  --erank-emerald: #137a4b;
  --erank-emerald-light: #e6f4ed;
  --erank-orange: #e57c23;
  --erank-orange-hover: #cf6a15;
  --bg-main: #f4f6f5;
  --bg-card: #ffffff;
  --bg-row-alt: #f8f5ec;
  --text-primary: #1c2826;
  --text-secondary: #5a6b65;
  --text-muted: #84948e;
  --border-color: #dce3e0;
  --badge-low-bg: #d1f2df;
  --badge-low-text: #0b5e36;
  --badge-mod-bg: #fef0c7;
  --badge-mod-text: #93560d;
  --badge-high-bg: #fde2dd;
  --badge-high-text: #9e2315;
  --shadow-sm: 0 1px 3px rgba(10, 40, 25, 0.06);
  --shadow-md: 0 4px 14px rgba(10, 40, 25, 0.08);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-primary);
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ================= LEFT SIDEBAR (eRank Deep Forest Green) ================= */
.sidebar {
  width: 245px;
  min-width: 245px;
  background-color: var(--erank-sidebar-bg);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  height: 100vh;
  user-select: none;
  z-index: 20;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.12);
}

.sidebar-brand {
  padding: 18px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.09);
}

.brand-logo {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-logo span.e-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: #ffffff;
  color: var(--erank-sidebar-bg);
  font-weight: 900;
  font-size: 20px;
}

.brand-badge {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  background: var(--erank-orange);
  color: #fff;
  padding: 3px 7px;
  border-radius: 10px;
  font-weight: 700;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 20px;
  color: rgba(255, 255, 255, 0.86);
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  border-left: 4px solid transparent;
}

.nav-item:hover {
  background-color: var(--erank-sidebar-hover);
  color: #ffffff;
}

.nav-item.active {
  background-color: var(--erank-sidebar-active);
  color: #ffffff;
  font-weight: 600;
  border-left-color: #4cd98c;
}

.nav-item-left {
  display: flex;
  align-items: center;
  gap: 11px;
}

.nav-icon {
  width: 18px;
  text-align: center;
  font-size: 15px;
}

.nav-submenu {
  background: rgba(0, 0, 0, 0.18);
  padding: 4px 0;
}

.nav-subitem {
  padding: 9px 20px 9px 48px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.78);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.15s ease;
  border-left: 4px solid transparent;
}

.nav-subitem:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}

.nav-subitem.active {
  color: #ffffff;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.11);
  border-left-color: var(--erank-orange);
}

.sidebar-footer {
  padding: 14px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-upgrade {
  width: 100%;
  background: var(--erank-orange);
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.15s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.btn-upgrade:hover {
  background: var(--erank-orange-hover);
}

.sidebar-status {
  margin-top: 10px;
  font-size: 11.5px;
  color: rgba(255, 255, 255, 0.72);
  display: flex;
  align-items: center;
  gap: 7px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4cd98c;
  box-shadow: 0 0 6px #4cd98c;
}

/* ================= MAIN VIEWPORT & TOP UTILITY BAR ================= */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.topbar {
  height: 60px;
  min-height: 60px;
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 26px;
  gap: 16px;
  z-index: 10;
}

.search-group {
  display: flex;
  align-items: center;
  border: 1px solid #cbd5d0;
  border-radius: 6px;
  overflow: hidden;
  background: #f9fbfa;
  height: 38px;
  max-width: 580px;
  flex: 1;
}

.search-select {
  border: none;
  background: transparent;
  padding: 0 12px;
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
  border-right: 1px solid #dce3e0;
  height: 100%;
  cursor: pointer;
  outline: none;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 0 14px;
  font-size: 13.5px;
  color: var(--text-primary);
  outline: none;
}

.country-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 12px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-secondary);
  border-left: 1px solid #dce3e0;
  height: 100%;
  background: #ffffff;
}

.search-btn {
  background: #3d7a62;
  color: #ffffff;
  border: none;
  width: 42px;
  height: 100%;
  cursor: pointer;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.search-btn:hover {
  background: var(--erank-sidebar-bg);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.quota-pill {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f3f7f5;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.quota-pill strong {
  color: var(--erank-sidebar-bg);
}

.btn-outline {
  background: #ffffff;
  border: 1px solid #cbd5d0;
  color: var(--text-primary);
  padding: 7px 14px;
  border-radius: 6px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s;
}

.btn-outline:hover {
  border-color: var(--erank-emerald);
  color: var(--erank-emerald);
  background: var(--erank-emerald-light);
}

.btn-primary {
  background: var(--erank-emerald);
  color: #ffffff;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: background 0.15s;
}

.btn-primary:hover {
  background: var(--erank-sidebar-bg);
}

/* ================= CONTENT SCROLL AREA ================= */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px 30px 48px 30px;
}

.view-panel {
  display: none;
  animation: fadeIn 0.18s ease-in-out;
}

.view-panel.active {
  display: block;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
  gap: 16px;
}

.page-title {
  font-size: 23px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-subtitle {
  font-size: 13.5px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* ================= FILTER BAR CARD (eRank Style) ================= */
.filter-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 16px;
  box-shadow: var(--shadow-sm);
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 170px;
  flex: 1;
}

.filter-field label {
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
}

.filter-input, .filter-select {
  height: 36px;
  border: 1px solid #cbd5d0;
  border-radius: 6px;
  padding: 0 11px;
  font-size: 13px;
  color: var(--text-primary);
  background: #ffffff;
  outline: none;
}

.filter-input:focus, .filter-select:focus {
  border-color: var(--erank-emerald);
  box-shadow: 0 0 0 2px rgba(19, 122, 75, 0.12);
}

/* ================= KPI GRID ================= */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 15px 18px;
  box-shadow: var(--shadow-sm);
  border-top: 3px solid var(--erank-emerald);
}

.kpi-card.orange {
  border-top-color: var(--erank-orange);
}

.kpi-label {
  font-size: 11.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--text-secondary);
}

.kpi-value {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 6px 0 4px 0;
}

.kpi-sub {
  font-size: 12px;
  color: var(--erank-emerald);
  font-weight: 600;
}

/* ================= CHART CARDS & GRIDS ================= */
.chart-grid-2 {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 18px;
  margin-bottom: 20px;
}

.chart-grid-equal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 20px;
}

@media (max-width: 1180px) {
  .chart-grid-2, .chart-grid-equal {
    grid-template-columns: 1fr;
  }
}

.card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 18px 20px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 18px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eef2f0;
}

.card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.card-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
}

.chart-box {
  position: relative;
  height: 330px;
  width: 100%;
}

.chart-box-sm {
  position: relative;
  height: 250px;
  width: 100%;
}

/* ================= eRank DATA TABLES & SPARKLINES ================= */
.table-container {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow-x: auto;
  box-shadow: var(--shadow-sm);
}

table.erank-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

table.erank-table thead th {
  background: #eef3f0;
  color: #3b4d47;
  font-weight: 700;
  font-size: 11.5px;
  text-transform: none;
  padding: 11px 14px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  white-space: nowrap;
  user-select: none;
}

table.erank-table thead th:hover {
  background: #e1ebe6;
  color: var(--erank-sidebar-bg);
}

table.erank-table thead th.num,
table.erank-table tbody td.num {
  text-align: right;
}

table.erank-table tbody tr {
  border-bottom: 1px solid #ecefe9;
  transition: background 0.12s;
}

table.erank-table tbody tr:nth-child(even) {
  background-color: var(--bg-row-alt);
}

table.erank-table tbody tr:hover {
  background-color: #e9f4ee;
}

table.erank-table tbody td {
  padding: 10px 14px;
  vertical-align: middle;
  color: var(--text-primary);
}

.kw-cell {
  font-weight: 700;
  color: #0b5835;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.kw-cell:hover {
  text-decoration: underline;
}

.star-btn {
  cursor: pointer;
  color: #b0bdb7;
  font-size: 15px;
  margin-right: 6px;
  transition: color 0.15s;
}

.star-btn.starred {
  color: var(--erank-orange);
}

/* Inline 12-Month Trend Graph Sparkline (Matches Screenshot 1 & 2) */
.sparkline-wrapper {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 128px;
}

.sparkline-bars {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 26px;
  width: 100%;
  padding-bottom: 2px;
  border-bottom: 1px solid #cbd5d0;
}

.spark-bar {
  flex: 1;
  background: #b5c4be;
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  transition: background 0.15s;
}

.spark-bar.peak {
  background: #6c8c80;
}

.spark-bar.current {
  background: #064428;
}

.sparkline-caption {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 10px;
  font-weight: 700;
  color: #064428;
  margin-top: 2px;
}

/* Competition & Score Badges */
.badge-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11.5px;
  font-weight: 700;
  white-space: nowrap;
}

.badge-low {
  background: var(--badge-low-bg);
  color: var(--badge-low-text);
}

.badge-mod {
  background: var(--badge-mod-bg);
  color: var(--badge-mod-text);
}

.badge-high {
  background: var(--badge-high-bg);
  color: var(--badge-high-text);
}

. badge-blue-ocean {
  background: #d1f2df;
  color: #064428;
  border: 1px solid #86d9ab;
}

.comp-bar-wrap {
  width: 115px;
  background: #eaepe9;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #dce3e0;
  position: relative;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 6px;
  font-size: 11px;
  font-weight: 700;
}

.comp-bar-fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 0;
  opacity: 0.32;
}

.comp-bar-text {
  position: relative;
  z-index: 1;
}

/* Pinterest Playbook Cards */
.playbook-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}

.playbook-card {
  background: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px 18px;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--erank-emerald);
}

.playbook-card.tier1 {
  border-left-color: #0b6e40;
}

.playbook-card.tier2 {
  border-left-color: var(--erank-orange);
}

.playbook-hook {
  background: #f4f8f6;
  border-left: 3px solid var(--erank-emerald);
  padding: 8px 12px;
  font-size: 12.5px;
  font-style: italic;
  color: #064428;
  margin: 10px 0;
  border-radius: 0 4px 4px 0;
}

/* Modal / Drawer */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(6, 35, 20, 0.55);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-backdrop.open {
  display: flex;
}

.modal-dialog {
  background: #ffffff;
  border-radius: 10px;
  width: 92%;
  max-width: 940px;
  max-height: 88vh;
  overflow-y: auto;
  padding: 24px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.25);
}

.tag-chip {
  display: inline-block;
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 700;
  margin-right: 4px;
}

.tag-bestseller { background: #fde68a; color: #92400e; }
.tag-popular { background: #fed7aa; color: #9a3412; }
.tag-starseller { background: #e9d5ff; color: #5b21b6; }
.tag-ad { background: #e2e8f0; color: #475569; }
"""
