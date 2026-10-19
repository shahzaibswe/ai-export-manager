from app.nlp.extractor import extract_attributes
from app.nlp.preprocessor import normalize_urdu_text

def test_extract_leather_jacket_benchmark():
    raw = "Mere paas asli chamray ki mardana jacket hai, size M se XXL, kaala aur brown rang, kam az kam 500 pieces, rate 40 dollar per piece, 15 din mein delivery."
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert attrs.product_type == "men_jacket"
    assert "Leather" in attrs.material or "leather" in attrs.material.lower()
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
    assert "steel" in attrs.material.lower()
    assert attrs.moq == 500
    assert attrs.unit_price_usd == 4.0
    assert attrs.lead_time_days == 10

def test_extract_watches():
    raw = "Mere paas luxury quartz watches hain stainless steel case aur leather strap ke sath, black dial, rate 25 dollar, kam az kam 100 pieces, 12 din delivery."
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert "watch" in attrs.product_type
    assert attrs.category == "Watches & Timepieces"
    assert "Steel" in attrs.material or "Leather" in attrs.material
    assert "black" in attrs.colors
    assert attrs.moq == 100
    assert attrs.unit_price_usd == 25.0
    assert attrs.lead_time_days == 12

def test_extract_toys():
    raw = "Ham bachon ke educational STEM learning toys banatay hain non-toxic ABS plastic ke, multi-color, rate 6 dollar per unit, MOQ 500 toys, 15 din mein delivery."
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert "toy" in attrs.product_type
    assert attrs.category == "Toys & Kids Products"
    assert "Plastic" in attrs.material or "ABS" in attrs.material
    assert attrs.moq == 500
    assert attrs.unit_price_usd == 6.0
    assert attrs.lead_time_days == 15

def test_extract_balls():
    raw = "Sialkot FIFA quality pro match football hand stitched PU leather size 5 MOQ 200 balls rate 12 dollar 20 days delivery."
    normalized = normalize_urdu_text(raw)
    attrs = extract_attributes(normalized, raw)

    assert "football" in attrs.product_type or "ball" in attrs.product_type
    assert attrs.category == "Sports Goods & Balls"
    assert "PU" in attrs.material or "Leather" in attrs.material
    assert attrs.moq == 200
    assert attrs.unit_price_usd == 12.0
    assert attrs.lead_time_days == 20
