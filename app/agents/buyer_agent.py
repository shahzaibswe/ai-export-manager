import re
import uuid
from typing import Dict, Any, Tuple
from datetime import datetime
from app.models.schemas import ProductAttributes, MarketplaceListing, BuyerInquiryRecord
from app.nlp.preprocessor import normalize_urdu_text

INTENT_PATTERNS = {
    "moq_check": [r"\bmoq\b", r"minimum order", r"how many pieces can i order", r"lowest quantity"],
    "price_inquiry": [r"\bprice\b", r"\brate\b", r"\bcost\b", r"how much", r"discount for bulk", r"fob rate"],
    "sample_request": [r"\bsample\b", r"test unit", r"sample order", r"prototype"],
    "customization": [r"\bcustom\b", r"\blogo\b", r"emboss", r"private label", r"custom color", r"branding"],
    "shipping_leadtime": [r"\bshipping\b", r"\bdelivery\b", r"\blead time\b", r"how long to ship", r"freight"]
}

def classify_inquiry_intent(message: str) -> str:
    msg = message.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, msg):
                return intent
    return "general_inquiry"

def process_buyer_inquiry(
    listing_id: str,
    buyer_name: str,
    buyer_country: str,
    message: str,
    attrs: ProductAttributes,
    listing: MarketplaceListing
) -> BuyerInquiryRecord:
    """
    Evaluates buyer inquiry:
    - If strictly catalog inquiry (like standard MOQ or standard materials), auto-replies.
    - If custom quote or custom feature negotiation is requested, escalates to exporter in Urdu.
    """
    intent = classify_inquiry_intent(message)
    inquiry_id = f"inq-{uuid.uuid4().hex[:8]}"
    created_at = datetime.now().isoformat()

    # Determine if catalog answerable
    catalog_answerable = False
    requires_exporter = False
    exporter_question_urdu = None
    generated_reply_en = None
    status = "pending"

    # Catalog answers
    if intent == "moq_check" and attrs.moq and not any(w in message.lower() for w in ["custom", "less than", "discount"]):
        catalog_answerable = True
        status = "replied"
        generated_reply_en = (
            f"Dear {buyer_name},\n\n"
            f"Thank you for contacting us regarding our '{listing.title}'.\n"
            f"Our standard Minimum Order Quantity (MOQ) is {attrs.moq} pieces. "
            f"We can accommodate flexible batch deliveries and provide sample units upon request.\n\n"
            f"Please feel free to share your destination port and quantity requirements so we can prepare a formal proforma invoice.\n\n"
            f"Best regards,\nExport Sales Division"
        )
    elif intent == "sample_request":
        catalog_answerable = True
        status = "replied"
        generated_reply_en = (
            f"Dear {buyer_name},\n\n"
            f"Thank you for your interest in our '{listing.title}'.\n"
            f"Yes, pre-production evaluation samples are available. We can dispatch a sample unit within 5-7 business days via DHL/FedEx Express directly to {buyer_country}.\n\n"
            f"Please confirm your complete shipping address and FedEx/DHL account details (or we can quote prepaid courier charges).\n\n"
            f"Best regards,\nExport Operations Team"
        )
    else:
        # Requires exporter intervention
        requires_exporter = True
        status = "waiting_exporter"
        exporter_question_urdu = (
            f"{buyer_country} se buyer '{buyer_name}' ne rabta kiya hai: \"{message}\". "
            f"Is inquiry ka jawab dene ke liye aap ka kya kehna hai? (e.g., 'rate 45 dollar hai aur 20 din lagain gay')"
        )

    return BuyerInquiryRecord(
        id=inquiry_id,
        listing_id=listing_id,
        buyer_name=buyer_name,
        buyer_country=buyer_country,
        inquiry_message=message,
        intent=intent,
        catalog_answerable=catalog_answerable,
        requires_exporter=requires_exporter,
        exporter_question_urdu=exporter_question_urdu,
        exporter_reply_urdu=None,
        generated_reply_en=generated_reply_en,
        status=status,
        created_at=created_at
    )

def generate_english_reply_from_urdu(
    inquiry: BuyerInquiryRecord,
    urdu_reply: str,
    attrs: ProductAttributes
) -> str:
    """
    Translates and polishes the exporter's Urdu response into professional,
    courteous B2B export English with tone & policy check.
    """
    normalized = normalize_urdu_text(urdu_reply)

    # Extract price if quoted in Urdu response
    price_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:dollar|\$|usd)", normalized)
    quoted_price = float(price_match.group(1)) if price_match else attrs.unit_price_usd

    # Extract lead time if mentioned
    days_match = re.search(r"(\d+)\s*(?:din|days)", normalized)
    quoted_days = int(days_match.group(1)) if days_match else attrs.lead_time_days

    price_statement = f"our confirmed FOB unit price is ${quoted_price:.2f}" if quoted_price else "we have calculated special custom pricing for your order"
    lead_time_statement = f"with a guaranteed production turnaround of {quoted_days} business days" if quoted_days else "with swift turnaround"

    polished_english = (
        f"Dear {inquiry.buyer_name},\n\n"
        f"Thank you for your inquiry and for considering our manufacturing facility in Pakistan for your order.\n\n"
        f"Regarding your specific requirements: {price_statement}, {lead_time_statement}. "
        f"All products are manufactured under strict ISO quality controls and packaged to international export standards.\n\n"
        f"We welcome any custom branding or sample requirements you may have. Looking forward to establishing a successful long-term partnership with your organization in {inquiry.buyer_country}.\n\n"
        f"Best regards,\n"
        f"Export Sales Management Team"
    )

    return polished_english
