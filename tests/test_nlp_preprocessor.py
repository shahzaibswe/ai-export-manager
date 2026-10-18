from app.nlp.preprocessor import normalize_urdu_text

def test_normalize_urdu_numbers_and_units():
    raw = "Mere paas asli chamray ki mardana jacket hai, size M se XXL, kaala aur brown rang, kam az kam paanch sau pieces, rate challis dollar per piece, 15 din mein delivery."
    normalized = normalize_urdu_text(raw)
    
    assert "500" in normalized
    assert "$40" in normalized or "40" in normalized
    assert "MOQ" in normalized or "500" in normalized
    assert "leather" in normalized
    assert "black" in normalized

def test_normalize_surgical_text():
    raw = "Sialkot mayo scissors medical grade stainless steel 500 pcs rate chaar dollar 10 din delivery"
    normalized = normalize_urdu_text(raw)
    assert "scissors" in normalized
    assert "stainless steel" in normalized
