from typing import List, Tuple
from app.models.schemas import ProductAttributes, SlotCheckResult

REQUIRED_SLOTS_PER_CATEGORY = {
    "Leather Apparel & Goods": ["material", "sizes", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Surgical & Dental Instruments": ["material", "moq", "unit_price_usd", "lead_time_days"],
    "Home Textiles": ["material", "sizes", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Sports Goods & Fitness": ["material", "sizes", "moq", "unit_price_usd", "lead_time_days"],
    "Export Goods": ["material", "moq", "unit_price_usd", "lead_time_days"]
}

URDU_FOLLOW_UPS = {
    "material": "Aap ka product kis material ya kapray/chamray ka bana hai? (e.g., Asli Cowhide Leather, 100% Cotton, Stainless Steel)",
    "sizes": "Konsay sizes dastiyab hain? (e.g., M se XXL, ya custom dimensions)",
    "colors": "Konsay rang (colors) dastiyab hain? (e.g., Kaala, Brown, Navy Blue)",
    "moq": "Aap ka kam az kam order (MOQ / Minimum Order Quantity) kitnay pieces ka hai?",
    "unit_price_usd": "Filhaal per-piece rate (USD dollars mein) kya quote karna chahtay hain?",
    "lead_time_days": "Production aur delivery mein kitnay din darkaar hon gay? (Lead time)"
}

ENGLISH_FOLLOW_UPS = {
    "material": "What material is this product made of? (e.g., Genuine Cowhide Leather, 100% Combed Cotton)",
    "sizes": "What sizes or dimensions are available? (e.g., Sizes M to XXL)",
    "colors": "What colors are available? (e.g., Black, Brown, Navy Blue)",
    "moq": "What is the Minimum Order Quantity (MOQ)?",
    "unit_price_usd": "What is the target wholesale unit price in USD?",
    "lead_time_days": "What is your production and dispatch lead time in days?"
}

def check_required_slots(category: str, attrs: ProductAttributes) -> SlotCheckResult:
    """
    Checks if all required export fields are populated.
    If missing, returns the first high-priority missing slot and a conversational Urdu prompt.
    """
    req_fields = REQUIRED_SLOTS_PER_CATEGORY.get(category, REQUIRED_SLOTS_PER_CATEGORY["Export Goods"])
    missing: List[str] = []

    if "material" in req_fields and not attrs.material:
        missing.append("material")
    if "sizes" in req_fields and (not attrs.sizes or len(attrs.sizes) == 0):
        missing.append("sizes")
    if "colors" in req_fields and (not attrs.colors or len(attrs.colors) == 0):
        missing.append("colors")
    if "moq" in req_fields and (attrs.moq is None or attrs.moq <= 0):
        missing.append("moq")
    if "unit_price_usd" in req_fields and (attrs.unit_price_usd is None or attrs.unit_price_usd <= 0):
        missing.append("unit_price_usd")
    if "lead_time_days" in req_fields and (attrs.lead_time_days is None or attrs.lead_time_days <= 0):
        missing.append("lead_time_days")

    if not missing:
        return SlotCheckResult(
            is_complete=True,
            missing_fields=[],
            follow_up_question_urdu=None,
            follow_up_question_en=None
        )

    # Focus on the first missing field
    priority_missing = missing[0]
    return SlotCheckResult(
        is_complete=False,
        missing_fields=missing,
        follow_up_question_urdu=URDU_FOLLOW_UPS.get(priority_missing, "Baraye meherbani mazeed maloomat faraham karein."),
        follow_up_question_en=ENGLISH_FOLLOW_UPS.get(priority_missing, "Please provide more details.")
    )
