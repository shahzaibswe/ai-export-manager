from typing import List, Tuple
from app.models.schemas import ProductAttributes, SlotCheckResult

REQUIRED_SLOTS_PER_CATEGORY = {
    "Leather Apparel & Goods": ["material", "sizes", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Home Textiles & Decor": ["material", "sizes", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Watches & Timepieces": ["material", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Toys & Kids Products": ["material", "moq", "unit_price_usd", "lead_time_days"],
    "Sports Goods & Balls": ["material", "sizes", "moq", "unit_price_usd", "lead_time_days"],
    "Consumer Electronics": ["material", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Footwear & Shoes": ["material", "sizes", "colors", "moq", "unit_price_usd", "lead_time_days"],
    "Jewelry & Fashion Accessories": ["material", "moq", "unit_price_usd", "lead_time_days"],
    "Surgical & Dental Instruments": ["material", "moq", "unit_price_usd", "lead_time_days"],
    "General Export Manufacturing": ["material", "moq", "unit_price_usd", "lead_time_days"]
}

def generate_product_aware_questions(product_name: str, category: str, missing_slot: str) -> Tuple[str, str]:
    """
    Dynamically generates natural Urdu and English follow-up questions
    customized specifically to the user's product (e.g. watches, toys, balls, jackets, etc.)
    """
    clean_name = product_name.replace("_", " ").title() if product_name else "Product"

    if missing_slot == "material":
        if "watch" in product_name.lower() or category == "Watches & Timepieces":
            urdu = f"Aap ki {clean_name} kis material ki bani hain? (e.g., Stainless Steel 316L Case, Genuine Leather Strap, Silicone, Ceramic)"
            eng = f"What material are your {clean_name} crafted from? (e.g., Stainless Steel 316L, Leather Strap, Silicone)"
        elif "toy" in product_name.lower() or category == "Toys & Kids Products":
            urdu = f"Aap ke {clean_name} kis material ke banay hain? (e.g., Non-Toxic BPA-Free ABS Plastic, Eco-Friendly Wood, Soft Plush)"
            eng = f"What material are these {clean_name} made of? (e.g., Non-Toxic ABS Plastic, Solid Wood, Soft Plush)"
        elif "ball" in product_name.lower() or category == "Sports Goods & Balls":
            urdu = f"Aap ki {clean_name} kis material ki bani hain? (e.g., Microfiber PU Leather, Hand-Stitched 32 Panels, Composite PVC)"
            eng = f"What material is used for these {clean_name}? (e.g., Microfiber PU Leather, Hand-Stitched Panels, PVC)"
        elif "scissor" in product_name.lower() or category == "Surgical & Dental Instruments":
            urdu = f"Aap ke {clean_name} kis surgical steel ke hain? (e.g., AISI 420 Medical Grade Stainless Steel, German Steel)"
            eng = f"What steel grade is used for {clean_name}? (e.g., Medical Grade Stainless Steel 420)"
        elif "towel" in product_name.lower() or category == "Home Textiles & Decor":
            urdu = f"Aap ke {clean_name} kis kapray ke hain? (e.g., 100% Combed Ring-Spun Cotton, Microfiber, 600 GSM Terry)"
            eng = f"What fabric is used for {clean_name}? (e.g., 100% Combed Cotton, Microfiber)"
        else:
            urdu = f"Aap ka product ({clean_name}) kis material ka bana hai? (e.g., Plastic, Solid Wood, Stainless Steel, Cotton, Leather)"
            eng = f"What material is this {clean_name} made of? (e.g., High-Grade Plastic, Wood, Steel, Leather, Cotton)"

    elif missing_slot == "moq":
        urdu = f"Aap ka {clean_name} ke liye kam az kam order (MOQ / Minimum Order Quantity) kitnay units ka hai?"
        eng = f"What is your Minimum Order Quantity (MOQ) for {clean_name}?"

    elif missing_slot == "unit_price_usd":
        urdu = f"Aap {clean_name} ka per-unit wholesale FOB export rate (USD dollars mein) kya quote karna chahtay hain?"
        eng = f"What is your target wholesale FOB unit price in USD for {clean_name}?"

    elif missing_slot == "lead_time_days":
        urdu = f"Aap ko {clean_name} ki production aur dispatch mein kitnay din darkaar hon gay? (Lead time)"
        eng = f"What is your manufacturing and dispatch lead time in days for {clean_name}?"

    elif missing_slot == "sizes":
        if "ball" in product_name.lower() or category == "Sports Goods & Balls":
            urdu = f"Aap ki {clean_name} ke konsay sizes dastiyab hain? (e.g., Official Size 5, Youth Size 4, Standard Size)"
            eng = f"What sizes are available for {clean_name}? (e.g., Official Size 5, Size 4)"
        elif "watch" in product_name.lower() or category == "Watches & Timepieces":
            urdu = f"Aap ki {clean_name} ka dial size ya case diameter kya hai? (e.g., 40mm, 42mm, Men's Standard, Women's Standard)"
            eng = f"What is the case diameter or target gender for {clean_name}? (e.g., 40mm, 42mm, Men/Women)"
        else:
            urdu = f"Aap ke {clean_name} ke konsay sizes ya dimensions dastiyab hain? (e.g., S se XXL, ya specific measurements)"
            eng = f"What sizes or dimensions are available for {clean_name}?"

    elif missing_slot == "colors":
        urdu = f"Aap ke {clean_name} mein konsay rang (colors) dastiyab hain? (e.g., Kaala, Silver, Gold, Blue, Multi-color)"
        eng = f"What color variations are available for {clean_name}? (e.g., Black, Silver, Gold, Assorted)"

    else:
        urdu = f"Baraye meherbani {clean_name} ke bare mein mazeed maloomat faraham karein."
        eng = f"Please provide additional details for {clean_name}."

    return urdu, eng

def check_required_slots(category: str, attrs: ProductAttributes) -> SlotCheckResult:
    """
    Checks if all required fields are present based on the product category.
    Generates dynamic, product-aware conversational Urdu follow-up questions.
    """
    req_fields = REQUIRED_SLOTS_PER_CATEGORY.get(category, REQUIRED_SLOTS_PER_CATEGORY["General Export Manufacturing"])
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

    # Focus on the first priority missing field
    priority_missing = missing[0]
    prod_name = attrs.product_type or "Product"
    urdu_q, eng_q = generate_product_aware_questions(prod_name, category, priority_missing)

    return SlotCheckResult(
        is_complete=False,
        missing_fields=missing,
        follow_up_question_urdu=urdu_q,
        follow_up_question_en=eng_q
    )
