from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.schemas import (
    BuyerInquiryInput, ExporterReplyInput, BuyerInquiryRecord,
    ProductAttributes, MarketplaceListing
)
from app.models.database import db
from app.agents.buyer_agent import process_buyer_inquiry, generate_english_reply_from_urdu

router = APIRouter(prefix="/api/v1/buyer", tags=["Buyer Communication Agent"])

@router.post("/inquiries")
def create_buyer_inquiry(input_data: BuyerInquiryInput):
    """
    Receives incoming inquiry from an international buyer.
    Classifies intent, auto-answers catalog queries, or escalates in Urdu to the exporter.
    """
    record = db.get_listing(input_data.listing_id)
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")

    attrs = ProductAttributes(**record.get("attributes", {}))
    listing = MarketplaceListing(**record.get("listing", {})) if record.get("listing") else None

    if not listing:
        raise HTTPException(status_code=400, detail="Cannot process inquiry: listing incomplete")

    inquiry_record = process_buyer_inquiry(
        listing_id=input_data.listing_id,
        buyer_name=input_data.buyer_name,
        buyer_country=input_data.buyer_country,
        message=input_data.inquiry_message,
        attrs=attrs,
        listing=listing
    )

    db.save_inquiry(inquiry_record.model_dump())
    return inquiry_record

@router.get("/inquiries")
def get_inquiries(listing_id: str = Query(..., description="Listing ID")):
    return db.get_inquiries_for_listing(listing_id)

@router.post("/inquiries/{inquiry_id}/reply")
def reply_to_inquiry(inquiry_id: str, reply_input: ExporterReplyInput):
    """
    Exporter submits reply in conversational Urdu.
    Agent turns it into professional, tone-checked export English for the buyer.
    """
    inq = db.get_inquiry(inquiry_id)
    if not inq:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    record = db.get_listing(inq["listing_id"])
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")

    attrs = ProductAttributes(**record.get("attributes", {}))
    inquiry_record = BuyerInquiryRecord(**inq)

    english_reply = generate_english_reply_from_urdu(
        inquiry_record,
        reply_input.urdu_response,
        attrs
    )

    inq["exporter_reply_urdu"] = reply_input.urdu_response
    inq["generated_reply_en"] = english_reply
    inq["status"] = "replied"

    db.save_inquiry(inq)
    return db.get_inquiry(inquiry_id)
