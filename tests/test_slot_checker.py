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

def test_slot_checker_missing_watch_material():
    attrs = ProductAttributes(
        product_type="luxury_watches",
        category="Watches & Timepieces",
        material=None,  # Missing material!
        colors=["black"],
        moq=100,
        unit_price_usd=25.0,
        lead_time_days=12
    )

    result = check_required_slots(attrs.category, attrs)
    assert result.is_complete is False
    assert "material" in result.missing_fields
    # Follow-up must be tailored to watches, not jackets/kapray!
    assert "watches" in result.follow_up_question_urdu.lower() or "watch" in result.follow_up_question_urdu.lower()
    assert "Steel" in result.follow_up_question_urdu or "Strap" in result.follow_up_question_urdu

def test_slot_checker_missing_toy_moq():
    attrs = ProductAttributes(
        product_type="educational_toys",
        category="Toys & Kids Products",
        material="Non-Toxic ABS Plastic",
        moq=None,  # Missing MOQ!
        unit_price_usd=6.0,
        lead_time_days=15
    )

    result = check_required_slots(attrs.category, attrs)
    assert result.is_complete is False
    assert "moq" in result.missing_fields
    assert "toy" in result.follow_up_question_urdu.lower()

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
