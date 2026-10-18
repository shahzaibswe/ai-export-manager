from fastapi import APIRouter, HTTPException, Query
from app.models.database import db
from app.models.schemas import ProductAttributes
from app.agents.market_intelligence import analyze_market_pricing

router = APIRouter(prefix="/api/v1/market", tags=["Market Intelligence"])

@router.get("/insights")
def get_market_insights(listing_id: str = Query(..., description="ID of the listing")):
    record = db.get_listing(listing_id)
    if not record:
        raise HTTPException(status_code=404, detail="Listing not found")

    if record.get("market_insight"):
        return record["market_insight"]

    attrs = ProductAttributes(**record.get("attributes", {}))
    return analyze_market_pricing(attrs, target_country=record.get("target_country", "USA"))
