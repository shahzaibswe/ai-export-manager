from typing import Dict, Any, List
from app.models.schemas import ProductAttributes, MarketplaceListing
from app.nlp.rag_store import retrieve_rag_examples

PLATFORM_LIMITS = {
    "alibaba": {"title_max_len": 128, "bullet_count": 5},
    "amazon": {"title_max_len": 200, "bullet_count": 5}
}

def generate_listing(attrs: ProductAttributes, platform: str = "alibaba", target_country: str = "USA") -> MarketplaceListing:
    """
    Generates marketplace-ready English export listing adhering to platform rules,
    featuring 5 buyer-focused benefit bullets, full SEO markdown description,
    15 targeted keywords, and an Urdu summary for exporter approval.
    """
    category = attrs.category or "Export Goods"
    rag_examples = retrieve_rag_examples(category, attrs.product_type or "")

    # Formatting components
    sizes_str = ", ".join(attrs.sizes) if attrs.sizes else "Standard Export Sizes"
    colors_str = " & ".join([c.capitalize() for c in attrs.colors]) if attrs.colors else "Classic Assorted"
    material_clean = (attrs.material or "Premium Export Grade").title()
    moq_str = f"MOQ {attrs.moq}" if attrs.moq else "Flexible Wholesale MOQ"
    lead_time_str = f"{attrs.lead_time_days} Days" if attrs.lead_time_days else "Fast Turnaround"
    price_str = f"${attrs.unit_price_usd:.2f}" if attrs.unit_price_usd else "Competitive Factory FOB"

    # 1. Title generation
    if attrs.product_type in ["men_jacket", "leather_jacket"]:
        title = f"Men's {material_clean} Jacket, {colors_str}, Sizes {sizes_str}, Wholesale OEM, {moq_str}"
    elif attrs.product_type == "surgical_scissors":
        title = f"Professional Surgical Operating Mayo Scissors, {material_clean}, CE & ISO Certified, {moq_str}"
    elif attrs.product_type == "bath_towels":
        title = f"Luxury {material_clean} Hotel Bath Towel Set, {colors_str}, Highly Absorbent, Wholesale {moq_str}"
    elif attrs.product_type == "match_football":
        title = f"Official Size 5 Pro Match Football, Hand Stitched {material_clean}, FIFA Standard, {moq_str}"
    else:
        prod_title = (attrs.product_type or "Product").replace("_", " ").title()
        title = f"Premium {material_clean} {prod_title}, {colors_str}, Wholesale B2B Exporter, {moq_str}"

    # Platform length cap
    max_len = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS["alibaba"])["title_max_len"]
    if len(title) > max_len:
        title = title[:max_len-3] + "..."

    # 2. Five Buyer-Focused Bullets
    bullets: List[str] = [
        f"PREMIUM {material_clean.upper()} CONSTRUCTION: Engineered for high durability and strict export grade standards, ensuring superior comfort and performance.",
        f"BUYER SPECIFICATIONS & COLORWAYS: Available in {colors_str} across sizing matrix ({sizes_str}) with reinforced stitching and precision finishing.",
        f"DIRECT PAKISTANI FACTORY PRICING: Sourced directly from our industrial manufacturing hub with an accessible MOQ of {attrs.moq or 'flexible'} units at {price_str}/unit FOB.",
        f"OEM & PRIVATE LABEL CAPABILITY: Full customization available including bespoke buyer tags, embroidered logos, laser engraving, and custom barcode packaging.",
        f"RELIABLE EXPORT DISPATCH: Guaranteed lead time of {lead_time_str} with complete pre-shipment quality inspection and worldwide air/ocean logistics support to {target_country}."
    ]

    # 3. Comprehensive SEO Markdown Description
    description = f"""### Product Overview
Welcome to direct manufacturing from Pakistan's premier export cluster. This **{title}** is precision-crafted for international commercial buyers, distributors, and retail brands in {target_country}.

### Key Commercial Specifications
- **Product Type:** {(attrs.product_type or 'Commercial Product').replace('_', ' ').title()}
- **Primary Material:** {material_clean}
- **Available Sizes:** {sizes_str}
- **Available Colors:** {colors_str}
- **Minimum Order Quantity (MOQ):** {attrs.moq or 'Contact Factory'} pieces
- **FOB Export Unit Price:** {price_str}
- **Production Lead Time:** {lead_time_str}
- **Quality Certifications:** ISO 9001 / CE Export Standards Compliant

### Customization & OEM Support
We support comprehensive OEM and private label requirements:
1. **Custom Branding:** Screen printing, silicone heat transfer, debossing, or woven neck labels.
2. **Packaging:** Individual polybag, retail display box, or custom carton with buyer shipping marks.
3. **Samples:** Pre-production samples dispatched within 5-7 working days.

### Why Partner With Us?
Located in Pakistan's world-renowned export manufacturing hub, we provide high-grade craftsmanship, rapid turnaround, and competitive tariff advantages for North American and European importers.
"""

    # 4. 15 High-Intent SEO Keywords
    keywords = [
        f"{attrs.material or 'export'} {(attrs.product_type or 'goods').replace('_', ' ')}",
        f"wholesale {attrs.product_type or 'goods'}",
        f"pakistan {attrs.category or 'export'} manufacturer",
        f"oem {(attrs.product_type or 'goods').replace('_', ' ')} supplier",
        f"bulk {colors_str.lower()} {attrs.product_type or 'items'}",
        f"factory price {attrs.product_type or 'products'}",
        f"b2b export to {target_country}",
        f"custom {material_clean.lower()} supplier",
        "iso certified manufacturing",
        "private label export",
        "sialkot faisalabad trade",
        f"direct manufacturer {target_country}",
        f"high quality {attrs.product_type or 'goods'}",
        "fast shipping worldwide",
        "verified wholesale supplier"
    ]

    # 5. Urdu Summary for Exporter Approval (Human-in-the-loop)
    urdu_summary = (
        f"Aap ka listing tayyar hai! Title: \"{title}\". "
        f"Material: {material_clean}, MOQ: {attrs.moq or 'N/A'} pieces, "
        f"Rate: {price_str}, Delivery: {lead_time_str}. "
        f"Is listing mein 5 buyer-focused bullet points, mukammal description, "
        f"aur 15 high-ranking SEO keywords shamil kiye gaye hain. "
        f"Neechay review karein aur Approve kar ke publish karein."
    )

    platform_formatted = {
        "platform": platform,
        "title": title,
        "bullets": bullets,
        "description": description,
        "keywords": keywords,
        "target_country": target_country,
        "unit_price_usd": attrs.unit_price_usd,
        "moq": attrs.moq
    }

    return MarketplaceListing(
        title=title,
        bullets=bullets,
        description=description,
        keywords=keywords,
        urdu_summary=urdu_summary,
        platform_formatted=platform_formatted
    )
