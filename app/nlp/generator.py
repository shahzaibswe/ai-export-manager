from typing import Dict, Any, List
from app.models.schemas import ProductAttributes, MarketplaceListing
from app.nlp.rag_store import retrieve_rag_examples

PLATFORM_LIMITS = {
    "alibaba": {"title_max_len": 128, "bullet_count": 5},
    "amazon": {"title_max_len": 200, "bullet_count": 5}
}

def generate_listing(attrs: ProductAttributes, platform: str = "alibaba", target_country: str = "USA") -> MarketplaceListing:
    """
    Generates marketplace-ready English export listing dynamically tailored
    to ANY product (Watches, Toys, Balls, Leather, Electronics, Textiles, etc.)
    """
    category = attrs.category or "General Export Manufacturing"
    prod_type = (attrs.product_type or "export_product").lower()

    # Formatted components
    sizes_str = ", ".join(attrs.sizes) if attrs.sizes else "Standard Export Specs"
    colors_str = " & ".join([c.capitalize() for c in attrs.colors]) if attrs.colors else "Classic Colorways"
    material_clean = (attrs.material or "High-Grade Export Material").title()
    moq_str = f"MOQ {attrs.moq}" if attrs.moq else "Flexible Wholesale MOQ"
    lead_time_str = f"{attrs.lead_time_days} Days" if attrs.lead_time_days else "Fast Turnaround"
    price_str = f"${attrs.unit_price_usd:.2f}" if attrs.unit_price_usd else "Competitive Factory FOB"

    # 1. Dynamic Title Generation
    if "watch" in prod_type or category == "Watches & Timepieces":
        title = f"Luxury Quartz Chronograph Watch, {material_clean}, Water Resistant, Custom OEM Dial, {moq_str}"
    elif "toy" in prod_type or category == "Toys & Kids Products":
        title = f"Educational STEM Learning Toys for Kids, {material_clean}, Certified Safe, Wholesale OEM, {moq_str}"
    elif "football" in prod_type or "soccer" in prod_type:
        title = f"Official Size 5 Pro Match Football, Hand Stitched {material_clean}, FIFA Standard, {moq_str}"
    elif "ball" in prod_type or category == "Sports Goods & Balls":
        title = f"Professional Tournament Grade Match Balls, {material_clean}, High Rebound, Wholesale OEM, {moq_str}"
    elif "jacket" in prod_type:
        title = f"Men's {material_clean} Jacket, {colors_str}, Sizes {sizes_str}, Wholesale OEM, {moq_str}"
    elif "scissor" in prod_type or category == "Surgical & Dental Instruments":
        title = f"Professional Surgical Operating Mayo Scissors, {material_clean}, CE & ISO Certified, {moq_str}"
    elif "towel" in prod_type or category == "Home Textiles & Decor":
        title = f"Luxury {material_clean} Hotel Bath Towel Set, {colors_str}, Highly Absorbent, Wholesale {moq_str}"
    elif "earbud" in prod_type or category == "Consumer Electronics":
        title = f"Wireless Bluetooth TWS Earbuds, HiFi Stereo Sound, Noise Cancelling, Wholesale OEM, {moq_str}"
    elif "shoe" in prod_type or category == "Footwear & Shoes":
        title = f"Comfort Men's {material_clean} Casual Shoes, Breathable Lightweight Sneaker, Wholesale OEM, {moq_str}"
    else:
        prod_title = prod_type.replace("_", " ").title()
        title = f"Premium {material_clean} {prod_title}, {colors_str}, Factory Wholesale OEM, {moq_str}"

    max_len = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS["alibaba"])["title_max_len"]
    if len(title) > max_len:
        title = title[:max_len-3] + "..."

    # 2. Category-Specific 5 Buyer-Focused Bullets
    if "watch" in prod_type or category == "Watches & Timepieces":
        bullets = [
            f"PRECISION QUARTZ TIMEKEEPING: Engineered with high-accuracy Japanese quartz movement and long-life battery delivering reliable performance.",
            f"PREMIUM {material_clean.upper()} CASING: Scratch-resistant hardened mineral crystal glass and surgical stainless steel back with 3ATM/5ATM water resistance.",
            f"BESPOKE PRIVATE LABEL OEM: Custom dial logo printing, engraved case-back, bespoke hands, and luxury leatherette gift presentation boxes.",
            f"DIRECT FACTORY EXPORT PRICING: Accessible wholesale MOQ of {attrs.moq or 'flexible'} pieces at {price_str}/unit FOB with high retail margin potential.",
            f"WORLDWIDE EXPORT LOGISTICS: Rigorous pre-shipment quality inspection and rapid dispatch within {lead_time_str} to commercial distributors in {target_country}."
        ]
    elif "toy" in prod_type or category == "Toys & Kids Products":
        bullets = [
            f"CERTIFIED CHILD-SAFE MATERIALS: Manufactured from 100% {material_clean.upper()}, completely free from BPA, phthalates, and harmful heavy metals.",
            f"INTERNATIONAL TOY ACCREDITATION: Fully compliant with international child safety standards including ASTM F963, CE Mark, and EN71 testing.",
            f"COGNITIVE & SENSORY DEVELOPMENT: Designed to inspire interactive STEM problem solving, motor coordination, and imaginative play for children.",
            f"OEM RETAIL PACKAGING: Full private brand customization including vibrant multi-color window boxes, barcode labeling, and custom blister packs.",
            f"DEPENDABLE EXPORT MANUFACTURING: Competitive factory pricing at {price_str}/unit with reliable {lead_time_str} lead time to {target_country}."
        ]
    elif "ball" in prod_type or category == "Sports Goods & Balls":
        bullets = [
            f"OFFICIAL TOURNAMENT INTEGRITY: Engineered with multi-layer textured {material_clean.upper()} for optimal aerodynamic flight and touch response.",
            f"SUPERIOR SHAPE RETENTION: High-tensile bonded stitching with reinforced Taiwanese butyl bladder preventing pressure loss and water uptake.",
            f"ALL-WEATHER DURABILITY: Tested for intense gameplay across natural grass, turf, and all-weather indoor pitches without scuffing or seam splitting.",
            f"CUSTOM FEDERATION & LEAGUE OEM: Full silkscreen club logo printing, tournament colorways, and custom retail polybag/mesh packaging.",
            f"DIRECT SIALKOT SPORTS HUB ADVANTAGE: Direct export pricing at {price_str}/ball, MOQ of {attrs.moq or 'flexible'} balls, and dispatch within {lead_time_str}."
        ]
    elif "scissor" in prod_type or category == "Surgical & Dental Instruments":
        bullets = [
            f"GERMAN-GRADE SURGICAL STEEL: Forged from AISI 420 hardened stainless steel for enduring edge sharpness and anti-corrosion protection.",
            f"SATIN ANTI-GLARE FINISH: Ultrasonic cleaning with matte satin finish reducing operating theater glare and optimizing tactile surgeon control.",
            f"CE & ISO 13485 CERTIFIED: Manufactured in strict compliance with medical device directives and FDA registration requirements.",
            f"AUTOCLAVABLE & REUSABLE: High-temperature steam sterilization resistant up to 134°C without discoloration or blade dulling over hundreds of cycles.",
            f"WHOLESALE OEM CAPABILITY: Custom laser-marking of distributor/hospital logos, barcode etching, and sterile blister packaging support."
        ]
    elif "towel" in prod_type or category == "Home Textiles & Decor":
        bullets = [
            f"100% COMBED RING-SPUN COTTON: Woven from premium Pakistani long-staple cotton for cloud-soft hand feel and zero lint shedding.",
            f"SUPERIOR COMMERCIAL ABSORBENCY: High-density double-loop terry weave absorbs up to 4x its weight in moisture with rapid quick-dry action.",
            f"COMMERCIAL LAUNDRY GRADE: Double-needle reinforced stitched side hems resist fraying across 200+ commercial hotel wash cycles.",
            f"OEKO-TEX STANDARD 100 CERTIFIED: Completely free from harmful chemicals, azo dyes, and skin irritants with eco-friendly reactive dyeing.",
            f"DIRECT FAISALABAD TEXTILE MILL: Low bulk wholesale MOQ of {attrs.moq or 1000} units, customized jacquard borders, and private carton packaging."
        ]
    else:
        bullets = [
            f"PREMIUM {material_clean.upper()} CONSTRUCTION: Engineered for high durability and strict export grade standards, ensuring superior performance.",
            f"BUYER SPECIFICATIONS & COLORWAYS: Available in {colors_str} across sizing matrix ({sizes_str}) with reinforced finishing and quality control.",
            f"DIRECT FACTORY EXPORT PRICING: Direct manufacturing pricing with an accessible MOQ of {attrs.moq or 'flexible'} units at {price_str}/unit FOB.",
            f"OEM & PRIVATE LABEL CAPABILITY: Full customization available including bespoke buyer tags, laser engraving, and custom barcode packaging.",
            f"RELIABLE EXPORT DISPATCH: Guaranteed turnaround of {lead_time_str} with pre-shipment quality inspection and freight support to {target_country}."
        ]

    # 3. Dynamic SEO Markdown Description
    clean_prod_title = prod_type.replace("_", " ").title()
    description = f"""### Product Overview
Welcome to direct manufacturing from Pakistan's premier export cluster. This **{title}** is precision-crafted for international commercial buyers, distributors, and retail brands in {target_country}.

### Key Commercial Specifications
- **Product Category:** {category}
- **Product Model:** {clean_prod_title}
- **Primary Material:** {material_clean}
- **Available Sizes / Specs:** {sizes_str}
- **Available Colors:** {colors_str}
- **Minimum Order Quantity (MOQ):** {attrs.moq or 'Flexible'} units
- **FOB Export Unit Price:** {price_str}
- **Production Lead Time:** {lead_time_str}
- **Quality Certifications:** ISO 9001 / CE Export Standards Compliant

### Customization & OEM Support
We support comprehensive OEM and private label requirements:
1. **Custom Branding:** Bespoke brand logo application (printing, debossing, engraving, or woven tags).
2. **Packaging:** Individual retail gift box, custom blister cards, or master export carton with buyer shipping marks.
3. **Evaluation Samples:** Fast pre-production sample dispatch via DHL/FedEx Express within 5-7 working days.

### Why Partner With Us?
Located in Pakistan's world-renowned export manufacturing hub, we provide high-grade craftsmanship, rapid turnaround, and competitive tariff advantages for North American and European importers.
"""

    # 4. 15 High-Intent SEO Keywords (Product Specific)
    base_kws = [
        f"{material_clean.lower()} {clean_prod_title.lower()}",
        f"wholesale {clean_prod_title.lower()}",
        f"pakistan {clean_prod_title.lower()} manufacturer",
        f"oem {clean_prod_title.lower()} supplier",
        f"bulk {clean_prod_title.lower()} export",
        f"factory price {clean_prod_title.lower()}",
        f"b2b export to {target_country}",
        f"custom {material_clean.lower()} products",
        f"private label {clean_prod_title.lower()}",
        f"direct manufacturer {target_country}",
        "verified wholesale supplier",
        "iso certified manufacturing",
        "export grade products pakistan",
        f"{colors_str.lower()} {clean_prod_title.lower()}",
        "fast shipping worldwide"
    ]

    # 5. Urdu Summary for Exporter Approval
    urdu_summary = (
        f"Aap ka {clean_prod_title} listing tayyar hai! Title: \"{title}\". "
        f"Material: {material_clean}, MOQ: {attrs.moq or 'N/A'} units, "
        f"Rate: {price_str}, Delivery: {lead_time_str}. "
        f"Is listing mein 5 buyer-focused bullet points, mukammal export description, "
        f"aur 15 high-ranking SEO keywords shamil kiye gaye hain. "
        f"Neechay review karein aur Approve kar ke publish karein."
    )

    platform_formatted = {
        "platform": platform,
        "title": title,
        "bullets": bullets,
        "description": description,
        "keywords": base_kws,
        "target_country": target_country,
        "unit_price_usd": attrs.unit_price_usd,
        "moq": attrs.moq
    }

    return MarketplaceListing(
        title=title,
        bullets=bullets,
        description=description,
        keywords=base_kws,
        urdu_summary=urdu_summary,
        platform_formatted=platform_formatted
    )
