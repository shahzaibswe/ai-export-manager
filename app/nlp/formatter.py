from typing import Dict, Any
from app.models.schemas import ProductAttributes, MarketplaceListing

def format_for_alibaba(attrs: ProductAttributes, listing: MarketplaceListing) -> Dict[str, Any]:
    """
    Formats product listing payload to Alibaba B2B Supplier / RFQ API format.
    """
    return {
        "marketplace": "Alibaba.com",
        "product_name": listing.title[:128],
        "category": attrs.category or "Apparel & Accessories",
        "model_number": f"PK-{attrs.product_type[:3].upper() if attrs.product_type else 'EXP'}-{attrs.moq or 500}",
        "place_of_origin": "Pakistan",
        "port_of_dispatch": "Karachi Sea Port / Sialkot Dry Port",
        "min_order_quantity": attrs.moq or 500,
        "fob_price_usd": attrs.unit_price_usd or 40.0,
        "fob_price_range": f"${(attrs.unit_price_usd or 40.0)*0.9:.2f} - ${(attrs.unit_price_usd or 40.0)*1.15:.2f}",
        "supply_ability": f"{(attrs.moq or 500) * 10} Pieces per Month",
        "payment_terms": "T/T, L/C, Western Union, Payoneer",
        "lead_time_days": attrs.lead_time_days or 15,
        "material": attrs.material or "Genuine Export Grade",
        "customization": ["Customized Logo (Min. Order: 500 Pieces)", "Customized Packaging", "Graphic Customization"],
        "detailed_description": listing.description,
        "key_attributes": {
            "Material": attrs.material,
            "Colors": ", ".join(attrs.colors) if attrs.colors else "Assorted",
            "Sizes": ", ".join(attrs.sizes) if attrs.sizes else "Custom"
        }
    }

def format_for_amazon(attrs: ProductAttributes, listing: MarketplaceListing) -> Dict[str, Any]:
    """
    Formats product listing payload to Amazon Selling Partner API (SP-API) JSON schema.
    """
    return {
        "marketplace": "Amazon Seller Central (SP-API)",
        "item_name": listing.title[:200],
        "brand_name": "CoreTech Private Label",
        "country_of_origin": "PK",
        "bullet_points": listing.bullets[:5],
        "standard_price": {
            "amount": attrs.unit_price_usd or 40.0,
            "currency_code": "USD"
        },
        "item_type_keyword": (attrs.product_type or "export-product").replace("_", "-"),
        "generic_keywords": ", ".join(listing.keywords[:15]),
        "material_type": attrs.material or "Leather",
        "color_name": attrs.colors[0].capitalize() if attrs.colors else "Multicolor",
        "size_name": attrs.sizes[0] if attrs.sizes else "Standard",
        "fulfillment_availability": {
            "lead_time_to_ship": attrs.lead_time_days or 15,
            "quantity": attrs.moq or 500
        },
        "product_description": listing.description
    }

def format_listing_by_platform(platform: str, attrs: ProductAttributes, listing: MarketplaceListing) -> Dict[str, Any]:
    if platform.lower() == "amazon":
        return format_for_amazon(attrs, listing)
    elif platform.lower() == "both":
        return {
            "alibaba": format_for_alibaba(attrs, listing),
            "amazon": format_for_amazon(attrs, listing)
        }
    else:
        return format_for_alibaba(attrs, listing)
