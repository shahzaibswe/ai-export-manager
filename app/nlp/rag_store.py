from typing import List, Dict, Any

TOP_SELLER_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "rag-leather-01",
        "category": "Leather Apparel & Goods",
        "keywords": ["leather", "jacket", "biker", "genuine leather", "cowhide", "oem"],
        "title": "Custom Men's Genuine Leather Biker Jacket Vintage Distressed Motorcycle Coat Wholesale OEM",
        "bullets": [
            "PREMIUM 100% GENUINE COWHIDE LEATHER: Handcrafted from full-grain supple leather offering rugged durability and exceptional wind resistance.",
            "PRECISION EXPORT FIT & FINISH: Heavy-duty YKK brass zippers, reinforced quilted shoulders, and breathable polyester satin thermal lining.",
            "COMPREHENSIVE SIZING MATRIX: Available in standard US/EU sizes M through XXL with custom tailored dimensional options for private label brands.",
            "DIRECT SIALKOT FACTORY OEM: Low MOQ of 500 units with full custom logo embossing, laser engraving, bespoke hangtags, and custom woven neck labels.",
            "RELIABLE EXPORT TIMELINES: 15-20 days production turnaround with strict pre-shipment ISO quality inspection and door-to-door air/sea freight support."
        ],
        "keywords_list": [
            "genuine leather jacket", "men motorcycle jacket", "sialkot leather exporter",
            "wholesale leather coat", "oem biker jacket", "custom leather apparel",
            "distressed leather coat", "vintage biker apparel", "heavy duty ykk zipper",
            "private label leather", "pakistan export garment", "full grain cowhide",
            "outerwear manufacturer", "factory price jacket", "leather goods supplier"
        ]
    },
    {
        "id": "rag-surgical-01",
        "category": "Surgical & Dental Instruments",
        "keywords": ["surgical", "scissors", "mayo", "stainless steel", "medical", "operating"],
        "title": "Professional Operating Mayo Scissors Straight 14cm Medical Grade Stainless Steel CE ISO Certified",
        "bullets": [
            "GERMAN-GRADE STAINLESS STEEL: Forged from AISI 420 hardened surgical steel for maximum corrosion resistance and enduring edge sharpness.",
            "ERGONOMIC ULTRASONIC FINISH: Satin anti-glare finish reduces operating room glare; precision ground beveled cutting blades for effortless tissue dissection.",
            "INTERNATIONAL ACCREDITATION: Fully compliant with CE Mark, ISO 13485 medical device manufacturing standards, and FDA cGMP compliance.",
            "AUTOCLAVABLE & REUSABLE: High-temperature steam sterilization proof up to 134°C without discoloration or blade dulling over hundreds of autoclave cycles.",
            "WHOLESALE OEM CAPABILITY: Custom laser-marking of hospital/distributor logos, barcode etching, and sterile blister packaging support."
        ],
        "keywords_list": [
            "mayo dissecting scissors", "surgical scissors 14cm", "medical grade stainless steel",
            "sialkot surgical instruments", "ce iso certified tools", "hospital operating instruments",
            "straight dissecting shears", "reusable surgical tools", "autoclavable scissors",
            "oem medical devices", "dental and surgical export", "precision medical shears",
            "aisi 420 steel", "operating room supplies", "pakistan surgical hub"
        ]
    },
    {
        "id": "rag-textile-01",
        "category": "Home Textiles",
        "keywords": ["towel", "cotton", "bath", "hotel", "faisalabad", "luxury"],
        "title": "Luxury 100% Combed Cotton Hotel Bath Towel Set 600 GSM Ultra Absorbent Quick Dry",
        "bullets": [
            "100% COMBED RING-SPUN COTTON: Woven from premium Pakistani long-staple cotton for cloud-soft hand feel, zero lint shedding, and ultimate plushness.",
            "SUPERIOR 600 GSM ABSORBENCY: High-density double-loop terry weave absorbs up to 4x its weight in moisture while retaining quick-dry performance.",
            "COMMERCIAL LAUNDRY GRADE: Double-needle reinforced stitched side hems resist fraying across 200+ commercial hotel wash cycles at high temperatures.",
            "OEKO-TEX STANDARD 100 CERTIFIED: Completely free from harmful chemicals, azo dyes, and skin irritants; eco-friendly reactive dyeing.",
            "DIRECT FAISALABAD TEXTILE MILL: Low bulk wholesale MOQ, customized jacquard borders, bespoke GSM weights, and private carton packaging."
        ],
        "keywords_list": [
            "hotel bath towels", "100 combed cotton towels", "600 gsm luxury towel",
            "faisalabad textile export", "wholesale bath sheet", "ultra absorbent terry towel",
            "oeko tex certified cotton", "commercial hotel linen", "pakistan cotton exporter",
            "quick dry bath towel", "plush bathroom towels", "bulk hospitality supplies",
            "double loop terry", "custom jacquard towel", "soft combed cotton"
        ]
    },
    {
        "id": "rag-sports-01",
        "category": "Sports Goods & Fitness",
        "keywords": ["football", "soccer", "match ball", "pu leather", "fifa", "hand stitched"],
        "title": "Official Size 5 Pro Match Football Hand-Stitched PU Leather Thermal Bonded FIFA Standard",
        "bullets": [
            "FIFA QUALITY PRO SPECIFICATIONS: Engineered with high-rebound multi-layer micro-textured PU leather for optimal aerodynamic flight and touch precision.",
            "32-PANEL HAND-STITCHED INTEGRITY: High-tensile bonded polyester thread with reinforced Taiwanese butyl bladder prevents pressure loss and water absorption.",
            "ALL-WEATHER DURABILITY: Suitable for natural turf and modern 3G/4G artificial grass pitches with scuff-resistant cross-laminated carcass.",
            "CUSTOM BRANDING & FEDERATION LOGOS: Custom silkscreen printing of league, club, or sponsor logos with official tournament color schemes.",
            "SIALKOT SPORTS HUB ADVANTAGE: Direct factory pricing, ISO 9001 certified production, and seamless container loading for international importers."
        ],
        "keywords_list": [
            "official match football", "fifa quality pro soccer ball", "size 5 football",
            "sialkot sports manufacturer", "hand stitched soccer ball", "pu leather football",
            "wholesale sports balls", "custom printed soccer ball", "tournament match ball",
            "aerodynamic soccer ball", "butyl bladder football", "pakistan sports export",
            "club football supplier", "training match ball", "outdoor soccer ball"
        ]
    }
]

def retrieve_rag_examples(category: str, query_text: str) -> List[Dict[str, Any]]:
    """
    RAG retriever: fetches top-performing listing style templates matching product category and query terms.
    """
    query_lower = query_text.lower()
    matches = []

    for item in TOP_SELLER_KNOWLEDGE_BASE:
        score = 0
        if item["category"] == category:
            score += 50
        for kw in item["keywords"]:
            if kw in query_lower:
                score += 15
        matches.append((score, item))

    matches.sort(key=lambda x: x[0], reverse=True)
    # Return top 2 matching examples
    return [m[1] for m in matches[:2]]
