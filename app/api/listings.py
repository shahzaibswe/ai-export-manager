import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import (
    ListingDraftInput, FollowUpAnswerInput, PublishRequest,
    PublishResponse, ListingRecord
)
from app.models.database import db
from app.nlp.preprocessor import normalize_urdu_text
from app.nlp.extractor import extract_attributes
from app.nlp.slot_checker import check_required_slots
from app.nlp.generator import generate_listing
from app.nlp.scorer import auto_improve_listing
from app.nlp.formatter import format_listing_by_platform
from app.agents.market_intelligence import analyze_market_pricing
from app.marketplaces.mock_alibaba import publish_to_mock_alibaba
from app.marketplaces.mock_amazon import publish_to_mock_amazon

router = APIRouter(prefix="/api/v1/listings", tags=["Listings"])

@router.post("/draft")
def create_draft(input_data: ListingDraftInput):
    """
    Submits Urdu or Roman Urdu product description.
    Runs full NLP pipeline: normalization -> attribute extraction -> slot checking.
    If fields are missing, returns follow-up question in Urdu.
    If fields are complete, generates listing, scores it, and runs market analysis.
    """
    raw_text = input_data.urdu_text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Urdu product description cannot be empty")

    listing_id = f"list-{uuid.uuid4().hex[:8]}"
    now = datetime.now().isoformat()

    # 1. Preprocess & Normalize
    normalized = normalize_urdu_text(raw_text)

    # 2. Extract structured attributes
    attrs = extract_attributes(normalized, raw_text)

    # 3. Slot check
    slot_res = check_required_slots(attrs.category or "Export Goods", attrs)

    listing_obj = None
    score_obj = None
    market_obj = None
    status = "needs_info"

    if slot_res.is_complete:
        # 4. Generate listing
        generated = generate_listing(attrs, platform=input_data.platform, target_country=input_data.target_country)
        # Format platform payload
        generated.platform_formatted = format_listing_by_platform(input_data.platform, attrs, generated)
        # 5. Quality scoring & auto-improve loop
        enhanced_listing, score_detail = auto_improve_listing(attrs, generated)
        listing_obj = enhanced_listing
        score_obj = score_detail
        # 6. Market intelligence
        market_obj = analyze_market_pricing(attrs, target_country=input_data.target_country)
        status = "ready"

    record_data = {
        "id": listing_id,
        "created_at": now,
        "updated_at": now,
        "raw_input": raw_text,
        "normalized_text": normalized,
        "target_platform": input_data.platform,
        "target_country": input_data.target_country,
        "attributes": attrs.model_dump(),
        "slots_status": slot_res.model_dump(),
        "listing": listing_obj.model_dump() if listing_obj else None,
        "quality_score": score_obj.model_dump() if score_obj else None,
        "market_insight": market_obj.model_dump() if market_obj else None,
        "status": status,
        "published_platforms": {}
    }

    db.save_listing(record_data)
    return db.get_listing(listing_id)

@router.post("/{listing_id}/answer")
def answer_follow_up(listing_id: str, answer: FollowUpAnswerInput):
    """
    Supplies missing information in response to the Urdu follow-up question.
    Updates attributes and proceeds with listing generation once all slots are filled.
    """
    record = db.get_listing(listing_id)
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")

    combined_raw = f"{record['raw_input']}. {answer.answer_text.strip()}"
    normalized_answer = normalize_urdu_text(answer.answer_text.strip())
    combined_normalized = f"{record['normalized_text']} {normalized_answer}"

    # Re-extract with updated text
    attrs = extract_attributes(combined_normalized, combined_raw)
    slot_res = check_required_slots(attrs.category or "Export Goods", attrs)

    listing_obj = None
    score_obj = None
    market_obj = None
    status = "needs_info"

    if slot_res.is_complete:
        generated = generate_listing(attrs, platform=record["target_platform"], target_country=record["target_country"])
        generated.platform_formatted = format_listing_by_platform(record["target_platform"], attrs, generated)
        enhanced_listing, score_detail = auto_improve_listing(attrs, generated)
        listing_obj = enhanced_listing
        score_obj = score_detail
        market_obj = analyze_market_pricing(attrs, target_country=record["target_country"])
        status = "ready"

    now = datetime.now().isoformat()
    record_data = {
        "id": listing_id,
        "created_at": record["created_at"],
        "updated_at": now,
        "raw_input": combined_raw,
        "normalized_text": combined_normalized,
        "target_platform": record["target_platform"],
        "target_country": record["target_country"],
        "attributes": attrs.model_dump(),
        "slots_status": slot_res.model_dump(),
        "listing": listing_obj.model_dump() if listing_obj else None,
        "quality_score": score_obj.model_dump() if score_obj else None,
        "market_insight": market_obj.model_dump() if market_obj else None,
        "status": status,
        "published_platforms": record.get("published_platforms", {})
    }

    db.save_listing(record_data)
    return db.get_listing(listing_id)

@router.get("/{listing_id}")
def get_listing_detail(listing_id: str):
    record = db.get_listing(listing_id)
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")
    return record

@router.get("")
def list_all():
    return db.list_all_listings()

@router.post("/{listing_id}/publish", response_model=PublishResponse)
def publish_listing(listing_id: str, req: PublishRequest):
    """
    One-click publish to mock Alibaba and/or Amazon marketplace APIs with live URL generation.
    """
    record = db.get_listing(listing_id)
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")

    if not record.get("listing"):
        raise HTTPException(status_code=400, detail="Cannot publish: listing has missing required attributes")

    now = datetime.now().isoformat()
    platform = req.platform.lower()
    published_platforms = record.get("published_platforms", {})

    target_url = ""
    summary_urdu = ""
    published_id = ""

    if platform in ["alibaba", "both"]:
        ali_res = publish_to_mock_alibaba(record)
        published_platforms["alibaba"] = ali_res
        target_url = ali_res["live_url"]
        published_id = ali_res["listing_id"]
        summary_urdu = f"Mubarak ho! Aap ka product Alibaba.com verified Pakistani Export Showcase par live ho chuka hai (Listing ID: {published_id})."

    if platform in ["amazon", "both"]:
        amz_res = publish_to_mock_amazon(record)
        published_platforms["amazon"] = amz_res
        if not target_url:
            target_url = amz_res["live_url"]
            published_id = amz_res["listing_id"]
        summary_urdu += f" Amazon SP-API ke zariye ASIN {amz_res['asin']} allocate ho chuki hai."

    record["published_platforms"] = published_platforms
    record["status"] = "published"
    record["updated_at"] = now
    db.save_listing(record)

    return PublishResponse(
        success=True,
        platform=platform,
        listing_id=published_id,
        status="LIVE",
        live_url=target_url,
        published_at=now,
        summary_urdu=summary_urdu
    )
