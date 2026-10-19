import re
from typing import Dict, Any, List, Optional
from app.models.schemas import ProductAttributes

CATEGORY_PATTERNS = {
    "Watches & Timepieces": [
        r"\bwatch\b", r"\bwatches\b", r"\bghari\b", r"\bghariyan\b", r"\bghari\b",
        r"\btimepiece\b", r"\bchronograph\b", r"\bsmartwatch\b", r"\bquartz\b"
    ],
    "Toys & Kids Products": [
        r"\btoy\b", r"\btoys\b", r"\bkhilona\b", r"\bkhilone\b", r"\bplush\b",
        r"\bdoll\b", r"\bdolls\b", r"\baction figure\b", r"\bbuilding blocks\b",
        r"\brc car\b", r"\bpuzzle\b", r"\bkids\b", r"\bbaby\b"
    ],
    "Sports Goods & Balls": [
        r"\bball\b", r"\bballs\b", r"\bgaind\b", r"\bgand\b", r"\bfootball\b",
        r"\bsoccer\b", r"\bcricket\b", r"\bbat\b", r"\btennis\b", r"\bvolleyball\b",
        r"\bbasketball\b", r"\bboxer\b", r"\bbox\b", r"\bgloves\b", r"\bsportswear\b", r"\bgym\b"
    ],
    "Consumer Electronics": [
        r"\bearbuds\b", r"\bheadphone\b", r"\bheadphones\b", r"\bearphone\b",
        r"\bcharger\b", r"\bspeaker\b", r"\bbluetooth\b", r"\bwireless\b",
        r"\bgadget\b", r"\belectronic\b", r"\bpower bank\b", r"\bcable\b"
    ],
    "Footwear & Shoes": [
        r"\bshoe\b", r"\bshoes\b", r"\bjootay\b", r"\bjoota\b", r"\bsneakers\b",
        r"\bboots\b", r"\bsandals\b", r"\bloafers\b", r"\bslippers\b"
    ],
    "Jewelry & Fashion Accessories": [
        r"\bjewelry\b", r"\bring\b", r"\brings\b", r"\bnecklace\b", r"\bbracelet\b",
        r"\bchain\b", r"\bgemstone\b", r"\bpendant\b", r"\bearrings\b"
    ],
    "Leather Apparel & Goods": [
        r"\bjacket\b", r"\bleather\b", r"\bchamra\b", r"\bcoat\b", r"\bvest\b",
        r"\bbiker\b", r"\bbelt\b", r"\bwallet\b", r"\bbriefcase\b"
    ],
    "Surgical & Dental Instruments": [
        r"\bsurgical\b", r"\bscissors\b", r"\bforceps\b", r"\bdental\b",
        r"\bmayo\b", r"\bscalpel\b", r"\btweezers\b", r"\bimplant\b"
    ],
    "Home Textiles & Decor": [
        r"\btowel\b", r"\btowels\b", r"\bbedsheet\b", r"\bbed sheet\b",
        r"\bcurtain\b", r"\blinen\b", r"\bfabric\b", r"\bpillow\b", r"\bbath\b", r"\bquilt\b"
    ]
}

MATERIAL_PATTERNS = [
    # Watch materials
    (r"\b(stainless steel 316l|stainless steel case|alloy case|steel case)\b", "Stainless Steel 316L"),
    (r"\b(leather strap|genuine leather strap|silicone strap|metal chain|mesh strap)\b", "Genuine Leather Strap & Stainless Steel Case"),
    (r"\b(sapphire crystal|mineral glass)\b", "Sapphire Coated Crystal Glass"),
    # Toy materials
    (r"\b(non-toxic abs plastic|abs plastic|eco-friendly plastic|bpa free plastic)\b", "Non-Toxic BPA-Free ABS Plastic"),
    (r"\b(wooden|natural wood|pine wood|beech wood)\b", "Natural Eco-Friendly Solid Wood"),
    (r"\b(soft plush|pp cotton|plush velvet)\b", "Hypoallergenic Soft Plush & PP Cotton"),
    (r"\b(food grade silicone|soft silicone)\b", "Food-Grade Soft Silicone"),
    (r"\b(die-cast|die cast metal|alloy metal)\b", "Die-Cast Zinc Alloy"),
    # Ball materials
    (r"\b(hand stitched pu|pu leather|microfiber pu|fifa grade pu)\b", "Microfiber Textured PU Leather"),
    (r"\b(pvc leather|synthetic pvc)\b", "High-Density Composite PVC"),
    (r"\b(vulcanized rubber|natural rubber)\b", "Vulcanized High-Grip Rubber"),
    # Metals & Surgical
    (r"\b(stainless steel\s*(?:420|440|304|medical grade)?|medical grade steel|german grade steel)\b", "Medical Grade Stainless Steel"),
    # Leather & Apparel
    (r"\b(genuine leather|asli leather|real leather|asli chamra|asli chamray|cowhide|sheepskin|lambskin)\b", "Genuine Leather"),
    (r"\b(100%\s*cotton|pure cotton|sooti|combed cotton|organic cotton)\b", "100% Combed Cotton"),
    (r"\b(polyester|microfiber|poly-cotton|nylon)\b", "Poly-Cotton Blend"),
    (r"\b(denim|twill)\b", "100% Premium Denim"),
    # General materials
    (r"\bplastic\b", "High-Durability Polymer Plastic"),
    (r"\bmetal\b", "High-Grade Engineered Alloy"),
    (r"\bwood\b", "Fine Natural Wood"),
    (r"\brubber\b", "High-Flex Elastic Rubber"),
    (r"\bglass\b", "Reinforced Tempered Glass"),
    (r"\baluminum\b", "Anodized Aerospace Aluminum"),
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
    "gold": ["gold", "golden", "sunehri"],
    "silver": ["silver", "chandi"],
    "pink": ["pink", "gulabi"],
    "orange": ["orange", "narangi"],
    "multi-color": ["multi", "multicolor", "rang barang", "colorful", "assorted"]
}

SIZE_RANGE_PATTERNS = [
    # Clothing sizes
    (r"\bm\s*(?:se|to|-)\s*xxl\b", ["M", "L", "XL", "XXL"]),
    (r"\bs\s*(?:se|to|-)\s*xxl\b", ["S", "M", "L", "XL", "XXL"]),
    (r"\bs\s*(?:se|to|-)\s*xl\b", ["S", "M", "L", "XL"]),
    (r"\bm\s*(?:se|to|-)\s*xl\b", ["M", "L", "XL"]),
    (r"\bxs\s*(?:se|to|-)\s*xxl\b", ["XS", "S", "M", "L", "XL", "XXL"]),
    # Ball sizes
    (r"\bsize\s*5\b", ["Official Size 5"]),
    (r"\bsize\s*4\b", ["Youth Size 4"]),
    (r"\bsize\s*3\b", ["Junior Size 3"]),
    # Watch sizes
    (r"\b(40mm|41mm|42mm|44mm|45mm)\b", ["Standard 42mm Casing"]),
    (r"\b(men|mardana)\b", ["Men's Standard"]),
    (r"\b(women|zanana)\b", ["Women's Standard"]),
    (r"\bunisex\b", ["Universal Unisex"]),
    # Toy age groups
    (r"\bage\s*(\d+\s*(?:to|-)\s*\d+\s*(?:years|sal)?)\b", [r"Age \1"]),
    (r"\b(3\+|4\+|6\+|8\+)\b", ["Ages 3+ Safe"]),
    # Boxing glove weights
    (r"\b(10oz|12oz|14oz|16oz)\b", ["10oz", "12oz", "14oz", "16oz"]),
]

STOP_WORDS = {
    "mere", "paas", "hai", "hain", "hy", "ki", "ka", "ke", "wali", "wala", "wale",
    "rate", "price", "qeemat", "cost", "dollar", "usd", "piece", "pieces", "pcs",
    "din", "days", "mein", "me", "delivery", "kam", "az", "se", "order", "moq",
    "export", "bana", "banatay", "aur", "and", "with", "for", "ham", "hum", "aik", "ek"
}

def extract_attributes(normalized_text: str, raw_text: str = "") -> ProductAttributes:
    """
    Extracts structured product attributes for ANY arbitrary product type
    (Watches, Toys, Balls, Jackets, Electronics, Footwear, etc.)
    """
    text = f"{normalized_text} {raw_text}".lower()

    # 1. Detect Category dynamically
    category = "General Export Manufacturing"
    for cat_name, patterns in CATEGORY_PATTERNS.items():
        matched = False
        for pat in patterns:
            if re.search(pat, text):
                category = cat_name
                matched = True
                break
        if matched:
            break

    # 2. Extract Specific Product Type
    product_type = None

    # Common explicit products
    if re.search(r"\b(watch|watches|ghari|ghariyan|chronograph|smartwatch)\b", text):
        product_type = "luxury_watches" if "luxury" in text else "quartz_watches"
    elif re.search(r"\b(toy|toys|khilone|khilona|plush|doll|rc car|building blocks)\b", text):
        product_type = "educational_toys" if ("educational" in text or "stem" in text) else "kids_toys"
    elif re.search(r"\b(football|soccer|match ball|gaind|gand)\b", text):
        product_type = "match_football"
    elif re.search(r"\b(cricket ball|leather ball)\b", text):
        product_type = "cricket_balls"
    elif re.search(r"\b(ball|balls)\b", text):
        product_type = "sports_balls"
    elif re.search(r"\b(jacket|jackets)\b", text):
        product_type = "men_jacket" if ("men" in text or "mardana" in text) else "leather_jacket"
    elif re.search(r"\b(scissor|scissors|mayo)\b", text):
        product_type = "surgical_scissors"
    elif re.search(r"\b(towel|towels)\b", text):
        product_type = "bath_towels"
    elif re.search(r"\b(earbuds|earphones|headphones)\b", text):
        product_type = "wireless_earbuds"
    elif re.search(r"\b(shoe|shoes|sneakers|boots)\b", text):
        product_type = "export_footwear"
    elif re.search(r"\b(boxing gloves|gloves)\b", text):
        product_type = "boxing_gloves" if "boxing" in text else "export_gloves"
    elif re.search(r"\b(bedsheet|bed sheet)\b", text):
        product_type = "luxury_bedsheets"
    else:
        # Dynamic extraction from user's sentence: find noun keywords
        cleaned_words = [w for w in re.findall(r"\b[a-zA-Z]{3,}\b", text) if w not in STOP_WORDS]
        if cleaned_words:
            product_type = "_".join(cleaned_words[:2])
        else:
            product_type = "custom_export_goods"

    # 3. Material extraction (universal)
    material = None
    for pattern, mat_name in MATERIAL_PATTERNS:
        if re.search(pattern, text):
            material = mat_name
            break

    # Contextual fallback for material if explicitly mentioned
    if not material:
        # Look for phrases like "plastic ke", "wood ke", "leather ka", "cotton ki", "steel ka"
        mat_match = re.search(r"\b([a-zA-Z]+)\s*(?:ka|ki|ke|made\s*of|material)\b", text)
        if mat_match:
            candidate = mat_match.group(1)
            if candidate not in STOP_WORDS and len(candidate) > 3:
                material = candidate.capitalize()

    # 4. Sizes / Dimensions / Specifications
    sizes: List[str] = []
    for pat, size_list in SIZE_RANGE_PATTERNS:
        match = re.search(pat, text)
        if match:
            sizes = size_list
            break

    if not sizes:
        # Check standard garment sizes
        found_sizes = []
        for s in ["xs", "s", "m", "l", "xl", "xxl", "3xl"]:
            if re.search(r"\b" + s + r"\b", text):
                found_sizes.append(s.upper())
        if found_sizes:
            sizes = found_sizes

    # 5. Colors
    colors: List[str] = []
    for std_color, aliases in COLOR_KEYWORDS.items():
        for alias in aliases:
            if re.search(r"\b" + alias + r"\b", text):
                if std_color not in colors:
                    colors.append(std_color)
                break

    # 6. MOQ (Minimum Order Quantity)
    moq: Optional[int] = None
    if "moq" in text:
        m = re.search(r"moq\s*[:=-]?\s*(\d+)", text)
        if m:
            moq = int(m.group(1))

    if moq is None:
        # Check patterns like "kam az kam 500", "500 pieces", "500 pcs", "500 balls", "100 watches", "200 toys"
        moq_patterns = [
            r"(?:kam\s*az\s*kam|kam\s*se\s*kam|minimum\s*order)\s*(\d{1,6})",
            r"(\d{2,6})\s*(?:piece|pieces|pcs|balls|units|watches|toys|pairs|sets|boxes|items)\b",
            r"(?:moq|quantity|qty)\s*(\d+)"
        ]
        for pat in moq_patterns:
            m = re.search(pat, text)
            if m:
                moq = int(m.group(1))
                break

    # 7. Unit Price USD
    unit_price_usd: Optional[float] = None
    price_patterns = [
        r"\$\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*\$",
        r"(?:rate|price|qeemat|cost)\s*(?:is|hai|hy)?\s*(\d+(?:\.\d+)?)\s*(?:dollar|usd)?",
        r"(\d+(?:\.\d+)?)\s*(?:dollar|usd)\s*(?:per\s*piece|each|rate|ka|per\s*unit)?"
    ]
    for p in price_patterns:
        m = re.search(p, text)
        if m:
            unit_price_usd = float(m.group(1))
            break

    # 8. Lead Time Days
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

    # 9. Custom features & certifications
    custom_features: List[str] = []
    if "water resistant" in text or "3atm" in text:
        custom_features.append("3ATM / 5ATM Water Resistant")
    if "oem" in text or "custom" in text:
        custom_features.append("OEM / Custom Branding Available")
    if "iso" in text or "ce" in text:
        custom_features.append("CE & ISO Certified")
    if "en71" in text or "astm" in text:
        custom_features.append("ASTM & EN71 Child Safety Approved")
    if "hand stitched" in text:
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
