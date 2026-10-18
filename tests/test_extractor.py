from app.nlp.extractor import extract_attributes
from app.nlp.preprocessor import normalize_urdu_text

def test_extract_leather_jacket_benchmark():
    raw = "Mere paas asli chamray ki mardana jacket hai, size M se XXL, kaala aur brown rang, kam az kam 500 pieces, rate 40 dollar per piece, 15 din mein delivery."
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert attrs.product_type == "men_jacket"
    assert attrs.material == "genuine leather"
    assert "M" in attrs.sizes and "XXL" in attrs.sizes
    assert "black" in attrs.colors and "brown" in attrs.colors
    assert attrs.moq == 500
    assert attrs.unit_price_usd == 40.0
    assert attrs.lead_time_days == 15

def test_extract_surgical_scissors():
    raw = "Sialkot mayo scissors medical grade stainless steel 500 pcs rate 4 dollar 10 din delivery"
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert "scissors" in attrs.product_type
    assert "stainless steel" in attrs.material
    assert attrs.moq == 500
    assert attrs.unit_price_usd == 4.0
    assert attrs.lead_time_days == 10
