from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "CoreTech" in data["team"]

def test_create_draft_full_flow():
    payload = {
        "urdu_text": "Mere paas asli chamray ki mardana jacket hai, size M se XXL, kaala aur brown rang, kam az kam 500 pieces, rate 40 dollar per piece, 15 din mein delivery.",
        "platform": "alibaba",
        "target_country": "USA"
    }
    res = client.post("/api/v1/listings/draft", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ready"
    assert data["quality_score"]["total_score"] >= 80
    assert "Genuine Leather" in data["listing"]["title"]

    listing_id = data["id"]

    # Test publish
    pub_res = client.post(f"/api/v1/listings/{listing_id}/publish", json={"platform": "alibaba"})
    assert pub_res.status_code == 200
    pub_data = pub_res.json()
    assert pub_data["status"] == "LIVE"
    assert "/marketplace/alibaba/" in pub_data["live_url"]

def test_create_draft_missing_slot_and_answer():
    # Missing MOQ
    payload = {
        "urdu_text": "Sialkot medical surgical mayo scissors stainless steel CE mark rate 4 dollar delivery 10 din",
        "platform": "alibaba",
        "target_country": "USA"
    }
    res = client.post("/api/v1/listings/draft", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "needs_info"
    assert "moq" in data["slots_status"]["missing_fields"]
    listing_id = data["id"]

    # Answer follow-up
    ans_res = client.post(f"/api/v1/listings/{listing_id}/answer", json={"answer_text": "MOQ 500 pieces hai"})
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["status"] == "ready"
    assert ans_data["attributes"]["moq"] == 500
