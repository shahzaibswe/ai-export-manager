import uuid
from datetime import datetime
from typing import Dict, Any

def publish_to_mock_alibaba(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates Alibaba Open Platform API (alibaba.trade.product.publish).
    Returns verified listing token, live URL, and RFQ status.
    """
    listing_id = f"ali-{uuid.uuid4().hex[:10]}"
    return {
        "marketplace": "Alibaba.com",
        "api_status": "SUCCESS",
        "listing_id": listing_id,
        "alibaba_item_code": f"ALB-{uuid.uuid4().hex[:6].upper()}",
        "live_url": f"/marketplace/alibaba/{listing_id}",
        "verification_status": "APPROVED_GOLD_SUPPLIER",
        "status": "LIVE",
        "published_at": datetime.now().isoformat(),
        "mock_message": "Listing published successfully to Alibaba Trade Showcase (Verified Pakistan Export Pavilion)."
    }
