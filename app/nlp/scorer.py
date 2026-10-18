import re
from typing import Tuple, List
from app.models.schemas import ProductAttributes, MarketplaceListing, QualityScoreDetail

BANNED_POLICY_WORDS = [
    r"\bwhatsapp\b", r"\bwechat\b", r"\bcall\s*me\b", r"\bphone\b",
    r"\+92\d{10}", r"\b\d{11}\b", r"cheap(?:est)?\s*in\s*the\s*world",
    r"100%\s*guaranteed\s*cure", r"free\s*gift\s*money"
]

def evaluate_quality_score(attrs: ProductAttributes, listing: MarketplaceListing) -> QualityScoreDetail:
    """
    Computes quality score according to official 0-100 rubric:
    1. Required attributes complete: 30 pts
    2. Title quality: 20 pts
    3. Bullet clarity & buyer benefits: 20 pts
    4. SEO keywords: 15 pts
    5. Policy compliance: 15 pts
    """
    suggestions: List[str] = []

    # 1. Required Attributes (30 Points)
    attr_pts = 0
    checks = [
        (bool(attrs.material), 5, "Missing material specification"),
        (bool(attrs.sizes and len(attrs.sizes) > 0), 5, "Missing size matrix"),
        (bool(attrs.colors and len(attrs.colors) > 0), 5, "Missing color variations"),
        (bool(attrs.moq and attrs.moq > 0), 5, "Missing minimum order quantity (MOQ)"),
        (bool(attrs.unit_price_usd and attrs.unit_price_usd > 0), 5, "Missing unit FOB price"),
        (bool(attrs.lead_time_days and attrs.lead_time_days > 0), 5, "Missing production lead time")
    ]
    for condition, pts, warning in checks:
        if condition:
            attr_pts += pts
        else:
            suggestions.append(warning)

    # 2. Title Quality (20 Points)
    title_pts = 0
    title = listing.title.strip()
    if 30 <= len(title) <= 150:
        title_pts += 10
    elif len(title) > 15:
        title_pts += 6
    else:
        suggestions.append("Title is too brief; should include product type, material and MOQ")

    # Check capitalization and keyword presence
    if attrs.material and attrs.material.lower() in title.lower():
        title_pts += 5
    if attrs.moq and str(attrs.moq) in title:
        title_pts += 5
    else:
        title_pts += 2

    # 3. Bullet Clarity and Buyer Benefits (20 Points)
    bullet_pts = 0
    if len(listing.bullets) >= 5:
        bullet_pts += 10
    else:
        suggestions.append("Marketplaces expect 5 distinct benefit-focused bullets")
        bullet_pts += max(2, len(listing.bullets) * 2)

    # Check buyer benefit keywords
    benefit_words = ["durability", "oem", "quality", "standard", "certified", "direct", "inspection", "pricing", "custom"]
    matches = sum(1 for w in benefit_words if any(w in b.lower() for b in listing.bullets))
    bullet_pts += min(10, matches * 2)

    # 4. SEO Keywords (15 Points)
    keyword_pts = 0
    if len(listing.keywords) >= 15:
        keyword_pts += 10
    else:
        keyword_pts += min(8, len(listing.keywords))

    if any(attrs.category.lower().split()[0] in kw.lower() for kw in listing.keywords if attrs.category):
        keyword_pts += 5
    else:
        keyword_pts += 3

    # 5. Policy Compliance (15 Points)
    compliance_pts = 15
    full_content = f"{listing.title} {' '.join(listing.bullets)} {listing.description}".lower()
    for banned in BANNED_POLICY_WORDS:
        if re.search(banned, full_content):
            compliance_pts -= 5
            suggestions.append(f"Policy violation detected: prohibited contact info or banned claim matching '{banned}'")

    compliance_pts = max(0, compliance_pts)

    total = attr_pts + title_pts + bullet_pts + keyword_pts + compliance_pts
    total = max(0, min(100, total))

    return QualityScoreDetail(
        attributes_score=attr_pts,
        title_score=title_pts,
        bullets_score=bullet_pts,
        keywords_score=keyword_pts,
        compliance_score=compliance_pts,
        total_score=total,
        suggestions=suggestions,
        auto_improved=False,
        iterations=1
    )

def auto_improve_listing(attrs: ProductAttributes, listing: MarketplaceListing, max_iterations: int = 2) -> Tuple[MarketplaceListing, QualityScoreDetail]:
    """
    Auto-improve feedback loop: If score < 80, automatically enhances listing details,
    refines bullets and keywords, and re-scores up to max_iterations.
    """
    current_listing = listing
    score = evaluate_quality_score(attrs, current_listing)

    iteration = 1
    while score.total_score < 80 and iteration <= max_iterations:
        # Auto-improve adjustments
        # 1. If title was too short or missing MOQ, enhance it
        if "Missing" in " ".join(score.suggestions) or score.title_score < 18:
            mat = (attrs.material or "High-Grade").title()
            moq = f"MOQ {attrs.moq}" if attrs.moq else "Wholesale MOQ"
            prod = (attrs.product_type or "Export Product").replace("_", " ").title()
            current_listing.title = f"Professional {mat} {prod}, Export Quality Wholesale OEM, {moq}"

        # 2. Ensure 5 robust bullets
        if len(current_listing.bullets) < 5 or score.bullets_score < 18:
            current_listing.bullets = [
                f"CERTIFIED EXPORT CRAFTSMANSHIP: High-grade {(attrs.material or 'durable material')} manufactured under strict ISO quality inspection standards.",
                f"COMMERCIAL BUYER ADVANTAGE: Direct manufacturing export pricing from Pakistan cluster with tailored MOQ of {attrs.moq or 500} units.",
                f"COMPREHENSIVE COLOR & SIZING: Tailored options including {', '.join(attrs.colors) if attrs.colors else 'standard export colors'} and precision dimensions.",
                f"OEM & PRIVATE LABEL READY: Custom branding, embossed logos, custom packaging boxes, and buyer barcoding support available.",
                f"RELIABLE DISPATCH & TRANSIT: Scheduled delivery turnaround of {attrs.lead_time_days or 15} days with full international freight forwarding documentation."
            ]

        # 3. Ensure 15 keywords
        if len(current_listing.keywords) < 15:
            current_listing.keywords.extend([
                "pakistan direct manufacturer",
                "global export supplier",
                "custom wholesale order",
                "verified export grade"
            ])
            current_listing.keywords = current_listing.keywords[:15]

        # Re-score
        score = evaluate_quality_score(attrs, current_listing)
        score.auto_improved = True
        score.iterations = iteration + 1
        iteration += 1

    return current_listing, score
