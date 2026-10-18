import uuid
from datetime import datetime
from typing import Dict, Any

def publish_to_mock_amazon(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates Amazon Selling Partner API (SP-API) Product Type Definitions & Feeds API.
    Returns generated ASIN, SKU, live product URL, and active status.
    """
    asin = f"B0{uuid.uuid4().hex[:8].upper()}"
    listing_id = f"amz-{uuid.uuid4().hex[:10]}"
    return {
        "marketplace": "Amazon Seller Central (SP-API)",
        "api_status": "ACCEPTED",
        "listing_id": listing_id,
        "asin": asin,
        "sku": f"CORE-{uuid.uuid4().hex[:6].upper()}",
        "live_url": f"/marketplace/amazon/{listing_id}",
        "status": "ACTIVE_BUYABLE",
        "feed_submission_id": f"feed-{uuid.uuid4().hex[:8]}",
        "published_at": datetime.now().isoformat(),
        "mock_message": f"Listing synchronized via Amazon SP-API. ASIN assigned: {asin}."
    }
