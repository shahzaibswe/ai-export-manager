from typing import Dict, Any
from app.models.schemas import ProductAttributes, MarketInsight

MARKET_BENCHMARKS = {
    "Watches & Timepieces": {
        "typical_min": 15.0,
        "typical_max": 65.0,
        "suggested_multiplier": 1.25,
        "demand": "Very High (E-Commerce & Private Label Watch Brands)",
        "top_countries": ["United States", "United Kingdom", "United Arab Emirates", "Germany", "Canada"],
        "margin": 38.0
    },
    "Toys & Kids Products": {
        "typical_min": 3.5,
        "typical_max": 22.0,
        "suggested_multiplier": 1.20,
        "demand": "Very High (STEM Learning & Holiday Gift Sourcing)",
        "top_countries": ["United States", "United Kingdom", "Germany", "Australia", "France"],
        "margin": 35.0
    },
    "Sports Goods & Balls": {
        "typical_min": 8.0,
        "typical_max": 28.0,
        "suggested_multiplier": 1.22,
        "demand": "High (Youth Leagues & Tournament Clubs)",
        "top_countries": ["United States", "Germany", "United Kingdom", "Brazil", "South Africa"],
        "margin": 34.0
    },
    "Consumer Electronics": {
        "typical_min": 10.0,
        "typical_max": 45.0,
        "suggested_multiplier": 1.25,
        "demand": "Very High (Mobile Accessories & Audio Brands)",
        "top_countries": ["United States", "United Kingdom", "Canada", "UAE", "Germany"],
        "margin": 40.0
    },
    "Footwear & Shoes": {
        "typical_min": 16.0,
        "typical_max": 55.0,
        "suggested_multiplier": 1.20,
        "demand": "High (Direct-to-Consumer Fashion Brands)",
        "top_countries": ["United States", "United Kingdom", "Italy", "Spain", "Germany"],
        "margin": 30.0
    },
    "Jewelry & Fashion Accessories": {
        "typical_min": 5.0,
        "typical_max": 40.0,
        "suggested_multiplier": 1.30,
        "demand": "Very High (Boutique & Online Retailers)",
        "top_countries": ["United States", "United Kingdom", "France", "UAE", "Australia"],
        "margin": 45.0
    },
    "Leather Apparel & Goods": {
        "typical_min": 35.0,
        "typical_max": 80.0,
        "suggested_multiplier": 1.20,
        "demand": "Very High (Peak Autumn/Winter Buying Season)",
        "top_countries": ["United States", "United Kingdom", "Germany", "France", "Canada"],
        "margin": 32.5
    },
    "Surgical & Dental Instruments": {
        "typical_min": 3.5,
        "typical_max": 12.0,
        "suggested_multiplier": 1.15,
        "demand": "High (Year-Round Recurring Hospital Tenders)",
        "top_countries": ["United States", "Germany", "Japan", "United Arab Emirates", "Saudi Arabia"],
        "margin": 45.0
    },
    "Home Textiles & Decor": {
        "typical_min": 4.0,
        "typical_max": 16.0,
        "suggested_multiplier": 1.18,
        "demand": "Very High (Hospitality & Home Retail Chains)",
        "top_countries": ["United States", "United Kingdom", "Netherlands", "Australia", "Spain"],
        "margin": 28.0
    }
}

DEFAULT_BENCHMARK = {
    "typical_min": 10.0,
    "typical_max": 40.0,
    "suggested_multiplier": 1.20,
    "demand": "Moderate to High Global Trade",
    "top_countries": ["United States", "United Kingdom", "Germany", "UAE"],
    "margin": 30.0
}

def analyze_market_pricing(attrs: ProductAttributes, target_country: str = "USA") -> MarketInsight:
    category = attrs.category or "General Export Manufacturing"
    bench = MARKET_BENCHMARKS.get(category, DEFAULT_BENCHMARK)

    base_price = attrs.unit_price_usd if attrs.unit_price_usd and attrs.unit_price_usd > 0 else (bench["typical_min"] + bench["typical_max"]) / 2.0
    suggested_price = round(base_price * bench["suggested_multiplier"], 2)

    min_price = min(bench["typical_min"], round(base_price * 0.85, 2))
    max_price = max(bench["typical_max"], round(suggested_price * 1.30, 2))
    avg_price = round((min_price + max_price) / 2.0, 2)

    prod_name = (attrs.product_type or "export product").replace("_", " ").title()
    mat_name = attrs.material or "verified export grade"

    recs = [
        f"International commercial buyers in {target_country} currently pay an average of ${avg_price:.2f} for verified {mat_name} {prod_name}.",
        f"Your base factory quote of ${base_price:.2f} leaves room to negotiate up to ${suggested_price:.2f} for customized OEM orders.",
        f"Offering tiered wholesale discounts (e.g., 200+ units at ${suggested_price:.2f}, 1000+ units at ${base_price:.2f}) boosts RFQ conversion significantly.",
        f"Buyers in {target_country} prioritize strict quality inspection & timely dispatch over rock-bottom pricing."
    ]

    return MarketInsight(
        product_category=category,
        suggested_price_usd=suggested_price,
        market_price_min=min_price,
        market_price_max=max_price,
        market_price_avg=avg_price,
        demand_level=bench["demand"],
        top_buyer_countries=bench["top_countries"],
        margin_estimate_pct=bench["margin"],
        recommendations=recs
    )
