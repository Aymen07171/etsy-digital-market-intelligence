"""
Pinterest Marketing & Paid Advertising Strategy Generator for Etsy Digital Products.

Generates data-driven, keyword-specific Pinterest organic SEO and paid ad recommendations,
calibrating Target CPC, Target CPA, Bundle AOV targets, creative formats, and Etsy
'Share & Save' funnel mechanics from the scraped marketplace metrics.
"""

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


PINTEREST_NICHE_PLAYBOOKS: Dict[str, Dict[str, Any]] = {
    "notion template adhd": {
        "ad_format": "9:16 Vertical Video Pin (15s Screen Recording of Gamified Dopamine Menu)",
        "pin_hook": "Stop Fighting Your Brain: The All-in-One ADHD Notion Second Brain That Actually Sticks",
        "pinterest_boards": "ADHD Organization Hacks | Notion Templates Aesthetic | Neurodivergent Productivity",
        "interest_targeting": "Productivity, Time Management, Bullet Journaling, ADHD Support, Studyblr",
        "lead_magnet_funnel": "Free 'ADHD Daily Brain Dump' 1-Page Notion Mini-Template -> $27 Full Life OS Upsell",
        "peak_seasonality": "Back-to-School (Aug-Sep) & New Year Reset (Dec 26 - Feb 15)",
    },
    "small business bookkeeping spreadsheet": {
        "ad_format": "2:3 Split-Screen Carousel Pin (Messy Receipts vs. Automated 1-Click Tax Dashboard)",
        "pin_hook": "Ditch Monthly Accounting Fees: Automated Google Sheets Bookkeeping for Small Business & Etsy Sellers",
        "pinterest_boards": "Small Business Bookkeeping | LLC Tax Prep | Side Hustle Finances | Etsy Seller Tips",
        "interest_targeting": "Small Business Ownership, Entrepreneurship, Accounting, Personal Finance, Freelancing",
        "lead_magnet_funnel": "Free 'LLC Tax Write-Off Checklist PDF' -> $29 Master Automated P&L Spreadsheet Bundle",
        "peak_seasonality": "Q1 Tax Season (Jan-Apr) & Q4 Year-End Close (Nov-Dec)",
    },
    "faceless digital marketing guide": {
        "ad_format": "9:16 Idea/Video Pin with Text Overlay + Revenue Proof Mockup",
        "pin_hook": "How to Launch a Passive Digital Product Shop Using Only Pinterest & Faceless Pins (Step-by-Step)",
        "pinterest_boards": "Faceless Digital Marketing | Passive Income Ideas | Digital Products Etsy | Pinterest Traffic",
        "interest_targeting": "Digital Marketing, Social Media Marketing, Passive Income, Work From Home, E-commerce",
        "lead_magnet_funnel": "Free '50 Viral Pinterest Hooks + Niche List' -> $37 Complete Faceless Launch Vault (PLR/MRR)",
        "peak_seasonality": "Year-Round Evergreen (Spikes in Jan, May, and Sep)",
    },
    "airbnb welcome book template": {
        "ad_format": "Carousel Pin (Flip-Through of Editable Canva Pages + QR Code WiFi Sign Mockup)",
        "pin_hook": "Turn 4-Star Stays into 5-Star Superhost Reviews: Editable Airbnb Welcome Book + QR GuideBundle",
        "pinterest_boards": "Airbnb Host Tips | Vacation Rental Decor | Short Term Rental Management | Superhost Ideas",
        "interest_targeting": "Real Estate Investing, Interior Design, Travel & Hospitality, Home Staging, VRBO Hosting",
        "lead_magnet_funnel": "Free 'Airbnb Cleaning & Turnover Checklist' -> $29 Ultimate Superhost Canva Bundle (Welcome Book + 12 Signs)",
        "peak_seasonality": "Pre-Summer Travel Prep (Mar-Jun) & Fall Foliage/Ski Prep (Sep-Nov)",
    },
    "procreate brushes bundle": {
        "ad_format": "9:16 Time-Lapse Video Pin (Live iPad Stroke Demo & Texture Zoom-In)",
        "pin_hook": "Transform Flat Digital Art into Rich Watercolor & Ink Illustrations in 1 Brush Stroke",
        "pinterest_boards": "Procreate Brushes & Tutorials | iPad Digital Art | Tattoo Flash Design | Illustration Tips",
        "interest_targeting": "Digital Illustration, Drawing Tutorials, Graphic Design, Procreate App, Concept Art",
        "lead_magnet_funnel": "Free '5 Sample Liner & Shader Brushes' -> $24 Master 150+ Brush Studio + Color Palettes",
        "peak_seasonality": "Holiday iPad Gifting Surge (Nov 20 - Jan 31) & Back-to-School",
    },
    "digital planner goodnotes": {
        "ad_format": "9:16 Aesthetic iPad + Apple Pencil Tap-Through Video Pin",
        "pin_hook": "Your Entire 2026-2027 Life Organized on Your iPad: Hyperlinked GoodNotes Planner + 1,000 Stickers",
        "pinterest_boards": "GoodNotes Digital Planner | iPad Aesthetic Setup | Paperless Planning | Student Organization",
        "interest_targeting": "Journaling, iPad Accessories, Study Motivation, Digital Planning, Goal Setting",
        "lead_magnet_funnel": "Free 'Aesthetic Digital Sticker Sheet + Weekly Layout' -> $22 Undated All-in-One Planner Bundle",
        "peak_seasonality": "Q4/Q1 Planner Rush (Nov-Feb) & Academic Year Start (Jul-Sep)",
    },
    "canva instagram templates": {
        "ad_format": "2:3 Grid Mockup Pin Showing 60 Cohesive Posts + Reels Covers",
        "pin_hook": "30 Days of High-Converting Instagram Content in 15 Minutes: Editable Canva Aesthetic Bundle",
        "pinterest_boards": "Instagram Feed Aesthetic | Canva Templates for Business | Social Media Branding | Realtor Marketing",
        "interest_targeting": "Social Media Strategy, Branding Design, Small Business Marketing, Content Creation",
        "lead_magnet_funnel": "Free '5 Viral Carousel Templates' -> $27 Complete 150-Template Brand Kit (Posts + Stories + E-Book)",
        "peak_seasonality": "Q1 New Business Launches (Jan-Mar) & Q3 Fall Marketing Push (Aug-Oct)",
    },
    "wedding invitation template download": {
        "ad_format": "9:16 Flat-Lay Video/Static Pin with 'Old Money / Venue Sketch' Aesthetic",
        "pin_hook": "Luxury Custom Wedding Stationery Look for Under $20: Instant Edit & Print Canva Wedding Suite",
        "pinterest_boards": "2026 Wedding Invitation Trends | Budget Wedding Ideas | DIY Wedding Stationery | Bridal Shower",
        "interest_targeting": "Wedding Planning, Bridal Inspiration, Wedding Invitations, Event Design",
        "lead_magnet_funnel": "Free 'Wedding Timeline & Budget Tracker' -> $34 Full Matching Suite (Invite + RSVP + Menu + Seating Chart)",
        "peak_seasonality": "Engagement Season Peak (Dec 15 - Apr 30)",
    },
    "printable wall art boho": {
        "ad_format": "2:3 Interior Mockup Pin (Framed 3-Piece Gallery Wall in Sunlit Living Room)",
        "pin_hook": "Refresh Your Living Room for $15: Instant Download Gallery Wall Sets in 5 Standard Frame Sizes",
        "pinterest_boards": "Boho Living Room Decor | Printable Wall Art | Apartment Therapy Ideas | Gallery Wall Layout",
        "interest_targeting": "Home Decor, Interior Styling, DIY Home Improvement, Minimalist Decor, Wall Art",
        "lead_magnet_funnel": "Avoid single $5 prints on Paid Ads; bundle into $18-$24 '6-Piece Whole Room Gallery Wall Set'",
        "peak_seasonality": "Spring Refresh (Mar-May) & Moving Season (Jun-Sep)",
    },
    "svg cut files bundle": {
        "ad_format": "2:3 Physical Product Mockup Pin (Finished T-Shirt, Tumbler, and Tote Bag using the SVGs)",
        "pin_hook": "500+ Commercial-Use Cricut & Laser SVG Designs: Ready-to-Cut Bestseller Bundle for Makers",
        "pinterest_boards": "Cricut Projects to Sell | SVG Cut Files | Sublimation Shirt Ideas | Laser Cut Craft Ideas",
        "interest_targeting": "Cricut Crafting, Silhouette Cameo, DIY Crafts, Woodworking/Laser Cutting, Handmade Business",
        "lead_magnet_funnel": "Free '10 Seasonal SVG Files' -> $19 Whole-Shop Lifetime Commercial SVG Vault Pass",
        "peak_seasonality": "Q4 Craft Fair & Holiday Gift Making Season (Sep-Dec)",
    },
}


class PinterestStrategyGenerator:
    """Builds actionable Pinterest organic & paid ad recommendations per keyword niche."""

    @staticmethod
    def generate_strategy_table(kw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriches the keyword intelligence table with concrete Pinterest unit economics,
        creative formats, targeting, and funnel recommendations.
        """
        rows: List[Dict[str, Any]] = []

        for _, row in kw_df.iterrows():
            kw = str(row["keyword"]).lower()
            playbook = PINTEREST_NICHE_PLAYBOOKS.get(
                kw,
                {
                    "ad_format": "9:16 Vertical Video Walkthrough + 2:3 Infographics",
                    "pin_hook": f"Save 10+ Hours a Week with This All-in-One {row['keyword'].title()} System",
                    "pinterest_boards": f"{row['keyword'].title()} Ideas | Digital Templates | Productivity Hacks",
                    "interest_targeting": "Productivity, DIY & Crafts, Small Business, Digital Downloads",
                    "lead_magnet_funnel": f"Free Mini-Sample -> $25 Complete {row['keyword'].title()} Mega Bundle",
                    "peak_seasonality": "Q1 Reset (Jan-Feb) & Q3 Back-to-Business (Aug-Sep)",
                },
            )

            current_avg_price = float(row["avg_price_usd"])
            # For paid Pinterest Ads to achieve >= 2.5x ROAS, single low-ticket digital items ($4-$9)
            # must be bundled to lift Average Order Value (AOV) to at least $18-$32.
            recommended_bundle_price = round(max(18.50, current_avg_price * 1.45), 2)

            # With Etsy 'Share & Save' (4% fee rebate on external traffic from Pinterest),
            # net Etsy fee drops from ~10.5% to ~6.5%. Zero COGS on digital downloads -> ~93.5% net margin.
            net_margin_after_share_and_save = round(recommended_bundle_price * 0.935, 2)

            # Target ROAS = 2.8x -> Target CPA = Recommended Bundle Price / 2.8
            target_cpa_usd = round(recommended_bundle_price / 2.8, 2)

            # Assuming a 2.4% Pinterest-to-Etsy landing page conversion rate on high-intent digital bundles
            assumed_cvr = 0.024
            max_profitable_cpc_usd = round(target_cpa_usd * assumed_cvr, 2)

            # Priority level based on Opportunity Score and Price/AOV viability
            opp_score = float(row["opportunity_score"])
            if opp_score >= 68 and current_avg_price >= 12.0:
                ad_priority = "Tier 1: Scale Paid Conversion & Consideration Ads Immediately"
                budget_split = "70% Paid Conversion/Traffic Ads / 30% Organic SEO Pins (5-8 Pins/day)"
            elif opp_score >= 55:
                ad_priority = "Tier 2: Retargeting Ads + High-Volume Organic Video Pins"
                budget_split = "40% Paid Retargeting & Warm Traffic / 60% Organic SEO Carousels"
            else:
                ad_priority = "Tier 3: Organic Pinterest SEO Only (Avoid Cold Paid Ads unless Bundled >= $22)"
                budget_split = "10% Promote Best-Selling Pin Only / 90% Automated Organic Keyword Pins"

            rows.append(
                {
                    "keyword": row["keyword"],
                    "niche_classification": row["niche_classification"],
                    "opportunity_score": opp_score,
                    "current_avg_etsy_price_usd": current_avg_price,
                    "recommended_pinterest_bundle_price_usd": recommended_bundle_price,
                    "net_margin_with_etsy_share_and_save_usd": net_margin_after_share_and_save,
                    "target_cpa_at_2_8x_roas_usd": target_cpa_usd,
                    "max_profitable_cpc_usd": max_profitable_cpc_usd,
                    "pinterest_campaign_priority": ad_priority,
                    "recommended_budget_allocation": budget_split,
                    "optimal_pin_creative_format": playbook["ad_format"],
                    "high_converting_pin_hook": playbook["pin_hook"],
                    "target_pinterest_boards": playbook["pinterest_boards"],
                    "pinterest_interest_targeting": playbook["interest_targeting"],
                    "bundle_and_lead_magnet_funnel": playbook["lead_magnet_funnel"],
                    "peak_seasonal_window": playbook["peak_seasonality"],
                }
            )

        return pd.DataFrame(rows)
