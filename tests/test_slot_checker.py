from app.models.schemas import ProductAttributes
from app.nlp.slot_checker import check_required_slots

def test_slot_checker_missing_moq():
    attrs = ProductAttributes(
        product_type="men_jacket",
        category="Leather Apparel & Goods",
        material="genuine leather",
        sizes=["M", "L", "XL"],
        colors=["black"],
        moq=None,  # Missing!
        unit_price_usd=40.0,
        lead_time_days=15
    )

    result = check_required_slots(attrs.category, attrs)
    assert result.is_complete is False
    assert "moq" in result.missing_fields
    assert "MOQ" in result.follow_up_question_urdu or "order" in result.follow_up_question_urdu

def test_slot_checker_complete():
    attrs = ProductAttributes(
        product_type="men_jacket",
        category="Leather Apparel & Goods",
        material="genuine leather",
        sizes=["M", "L", "XL"],
        colors=["black"],
        moq=500,
        unit_price_usd=40.0,
        lead_time_days=15
    )

    result = check_required_slots(attrs.category, attrs)
    assert result.is_complete is True
    assert len(result.missing_fields) == 0
