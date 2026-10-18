import re
from typing import Dict, Any, List, Optional
from app.models.schemas import ProductAttributes

CATEGORY_PATTERNS = {
    "Leather Apparel & Goods": [r"jacket", r"leather", r"chamra", r"coat", r"vest", r"biker", r"gloves", r"belt", r"wallet"],
    "Surgical & Dental Instruments": [r"surgical", r"scissors", r"forceps", r"dental", r"mayo", r"scalpel", r"tweezers", r"implant"],
    "Home Textiles": [r"towel", r"bedsheet", r"cotton", r"linen", r"curtain", r"fabric", r"pillow", r"bath"],
    "Sports Goods & Fitness": [r"football", r"soccer", r"boxing", r"gloves", r"cricket", r"bat", r"ball", r"sportswear", r"gym"]
}

MATERIAL_PATTERNS = [
    (r"\b(genuine leather|real leather|asli chamra|cowhide|sheepskin|lambskin)\b", "genuine leather"),
    (r"\b(pu leather|synthetic leather|faux leather)\b", "PU leather"),
    (r"\b(stainless steel\s*(?:420|440|304|medical grade)?|medical grade steel|german grade steel)\b", "medical grade stainless steel"),
    (r"\b(100%\s*cotton|pure cotton|sooti|combed cotton|organic cotton)\b", "100% combed cotton"),
    (r"\b(polyester|microfiber|poly-cotton|nylon)\b", "poly-cotton blend"),
    (r"\b(denim|twill)\b", "100% premium denim"),
]

COLOR_KEYWORDS = {
    "black": ["black", "kaala", "kala", "siah"],
    "brown": ["brown", "bhoora", "khaki"],
    "white": ["white", "sufaid", "safaid", "chitta"],
    "blue": ["blue", "neela", "navy"],
    "red": ["red", "laal", "lal", "surkh"],
    "green": ["green", "hara", "sabz"],
    "grey": ["grey", "gray", "silver"],
    "yellow": ["yellow", "peela"],
    "tan": ["tan", "camel"],
}

SIZE_RANGE_PATTERNS = [
    (r"\bm\s*(?:se|to|-)\s*xxl\b", ["M", "L", "XL", "XXL"]),
    (r"\bs\s*(?:se|to|-)\s*xxl\b", ["S", "M", "L", "XL", "XXL"]),
    (r"\bs\s*(?:se|to|-)\s*xl\b", ["S", "M", "L", "XL"]),
    (r"\bm\s*(?:se|to|-)\s*xl\b", ["M", "L", "XL"]),
    (r"\bxs\s*(?:se|to|-)\s*xxl\b", ["XS", "S", "M", "L", "XL", "XXL"]),
    (r"\bsize\s*5\b", ["Size 5"]),
    (r"\bsize\s*4\b", ["Size 4"]),
    (r"\b(10oz|12oz|14oz|16oz)\b", ["10oz", "12oz", "14oz", "16oz"]),
    (r"\b(\d{2,3}\s*[xX*]\s*\d{2,3}\s*(?:cm|inch)?)\b", None),  # custom dimension
]

def extract_attributes(normalized_text: str, raw_text: str = "") -> ProductAttributes:
    """
    Extracts structured product attributes from normalized Urdu/English text.
    Implements rule-based NER matching with fallback slot filling.
    """
    text = f"{normalized_text} {raw_text}".lower()

    # 1. Product type & Category
    category = "Export Goods"
    product_type = "export_product"

    for cat_name, patterns in CATEGORY_PATTERNS.items():
        for pat in patterns:
            if re.search(r"\b" + pat + r"\b", text):
                category = cat_name
                break
        if category != "Export Goods":
            break

    # Determine specific product_type
    if "jacket" in text:
        product_type = "men_jacket" if ("men" in text or "mardana" in text) else "leather_jacket"
    elif "scissor" in text or "mayo" in text:
        product_type = "surgical_scissors"
    elif "towel" in text:
        product_type = "bath_towels"
    elif "football" in text or "soccer" in text:
        product_type = "match_football"
    elif "boxing" in text:
        product_type = "boxing_gloves"
    elif "bedsheet" in text or "bed sheet" in text:
        product_type = "luxury_bedsheets"
    elif "denim" in text or "jean" in text:
        product_type = "denim_jeans"
    else:
        # Default fallback extraction from first noun phrases
        words = [w for w in text.split() if len(w) > 3 and w not in ["mere", "paas", "hain", "wali", "wala", "rate", "piece", "delivery", "dollar"]]
        if words:
            product_type = "_".join(words[:2])

    # 2. Material
    material = None
    for pattern, mat_name in MATERIAL_PATTERNS:
        if re.search(pattern, text):
            material = mat_name
            break
    if not material and "leather" in text:
        material = "genuine leather"
    elif not material and "cotton" in text:
        material = "100% cotton"
    elif not material and "steel" in text:
        material = "stainless steel"

    # 3. Sizes
    sizes: List[str] = []
    for pat, size_list in SIZE_RANGE_PATTERNS:
        match = re.search(pat, text)
        if match:
            if size_list:
                sizes = size_list
                break
            else:
                sizes = [match.group(1)]
                break

    if not sizes:
        # check individual sizes
        found_sizes = []
        for s in ["xs", "s", "m", "l", "xl", "xxl", "3xl"]:
            if re.search(r"\b" + s + r"\b", text):
                found_sizes.append(s.upper())
        if found_sizes:
            sizes = found_sizes

    # 4. Colors
    colors: List[str] = []
    for std_color, aliases in COLOR_KEYWORDS.items():
        for alias in aliases:
            if re.search(r"\b" + alias + r"\b", text):
                if std_color not in colors:
                    colors.append(std_color)
                break

    # 5. MOQ (Minimum Order Quantity)
    moq: Optional[int] = None
    # Look for "moq 500", "500 pieces", "500 pcs", "kam az kam 500"
    moq_match = re.search(r"(?:moq|kam\s*az\s*kam|minimum\s*order|kam\s*se\s*kam)?\s*(\d{2,6})\s*(?:piece|pieces|pcs|balls|pairs|sets|units)?", text)
    if "moq" in text:
        m = re.search(r"moq\s*[:=-]?\s*(\d+)", text)
        if m:
            moq = int(m.group(1))
    if moq is None:
        m = re.search(r"(\d+)\s*(?:piece|pieces|pcs|units|balls|pairs)\b", text)
        if m:
            moq = int(m.group(1))

    # 6. Unit Price USD
    unit_price_usd: Optional[float] = None
    # e.g. "rate 40 dollar", "$40", "40$", "price 40", "40 usd"
    price_patterns = [
        r"\$\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*\$",
        r"(?:rate|price|qeemat|cost)\s*(?:is|hai|hy)?\s*(\d+(?:\.\d+)?)\s*(?:dollar|usd)?",
        r"(\d+(?:\.\d+)?)\s*(?:dollar|usd)\s*(?:per\s*piece|each|rate|ka)?"
    ]
    for p in price_patterns:
        m = re.search(p, text)
        if m:
            unit_price_usd = float(m.group(1))
            break

    # 7. Lead time days
    lead_time_days: Optional[int] = None
    lead_patterns = [
        r"(\d+)\s*(?:din|days)\s*(?:mein\s*delivery|lead\s*time|delivery|production)?",
        r"(?:delivery|lead\s*time|dispatch)\s*(?:in|mein)?\s*(\d+)\s*(?:din|days)"
    ]
    for p in lead_patterns:
        m = re.search(p, text)
        if m:
            lead_time_days = int(m.group(1))
            break

    # 8. Custom features / tags
    custom_features: List[str] = []
    if "oem" in text or "custom" in text:
        custom_features.append("OEM / Custom Branding Available")
    if "iso" in text or "ce" in text:
        custom_features.append("CE & ISO Certified")
    if "hand stitched" in text or "dastkari" in text:
        custom_features.append("Hand Stitched Craftsmanship")
    if "sample" in text:
        custom_features.append("Sample Available on Request")

    return ProductAttributes(
        product_type=product_type,
        category=category,
        material=material,
        sizes=sizes,
        colors=colors,
        moq=moq,
        unit_price_usd=unit_price_usd,
        lead_time_days=lead_time_days,
        custom_features=custom_features
    )
