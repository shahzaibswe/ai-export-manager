from app.models.schemas import ProductAttributes
from app.nlp.generator import generate_listing
from app.agents.buyer_agent import process_buyer_inquiry, generate_english_reply_from_urdu

def test_buyer_inquiry_intent_and_reply():
    attrs = ProductAttributes(
        product_type="men_jacket",
        category="Leather Apparel & Goods",
        material="genuine leather",
        sizes=["M", "L", "XL", "XXL"],
        colors=["black", "brown"],
        moq=500,
        unit_price_usd=40.0,
        lead_time_days=15
    )
    listing = generate_listing(attrs)

    # 1. Custom quote inquiry (should escalate in Urdu)
    inq = process_buyer_inquiry(
        listing_id="list-test-01",
        buyer_name="John Doe",
        buyer_country="USA",
        message="Can you do 300 pieces with custom logo?",
        attrs=attrs,
        listing=listing
    )

    assert inq.requires_exporter is True
    assert inq.status == "waiting_exporter"
    assert "John Doe" in inq.exporter_question_urdu

    # 2. Exporter replies in Urdu
    reply_en = generate_english_reply_from_urdu(
        inq,
        urdu_reply="iska rate 45 dollar hai aur 20 din lagain gay",
        attrs=attrs
    )

    assert "$45.00" in reply_en
    assert "20" in reply_en
    assert "Dear John Doe" in reply_en
