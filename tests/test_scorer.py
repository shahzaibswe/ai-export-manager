from app.models.schemas import ProductAttributes
from app.nlp.generator import generate_listing
from app.nlp.scorer import evaluate_quality_score, auto_improve_listing

def test_rubric_scoring_and_auto_improve():
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

    listing = generate_listing(attrs, platform="alibaba", target_country="USA")
    score = evaluate_quality_score(attrs, listing)

    # Initial score should be solid
    assert score.attributes_score == 30
    assert score.title_score >= 15
    assert score.bullets_score >= 15
    assert score.keywords_score >= 12
    assert score.compliance_score == 15
    assert score.total_score >= 80

    # Test auto-improve on lower score
    enhanced_listing, improved_score = auto_improve_listing(attrs, listing)
    assert improved_score.total_score >= 80
