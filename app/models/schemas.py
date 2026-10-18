from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class ListingDraftInput(BaseModel):
    urdu_text: str = Field(..., description="Product description in Urdu or Roman Urdu")
    audio_base64: Optional[str] = Field(None, description="Optional audio base64")
    platform: str = Field("alibaba", description="Target platform: alibaba, amazon, or both")
    target_country: str = Field("USA", description="Target buyer market country")

class FollowUpAnswerInput(BaseModel):
    answer_text: str = Field(..., description="Answer to missing slot question in Urdu or English")

class ProductAttributes(BaseModel):
    product_type: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    sizes: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    moq: Optional[int] = None
    unit_price_usd: Optional[float] = None
    lead_time_days: Optional[int] = None
    custom_features: List[str] = Field(default_factory=list)

class SlotCheckResult(BaseModel):
    is_complete: bool
    missing_fields: List[str] = Field(default_factory=list)
    follow_up_question_urdu: Optional[str] = None
    follow_up_question_en: Optional[str] = None

class QualityScoreDetail(BaseModel):
    attributes_score: int = Field(..., ge=0, le=30, description="Completeness (Max 30)")
    title_score: int = Field(..., ge=0, le=20, description="Title quality (Max 20)")
    bullets_score: int = Field(..., ge=0, le=20, description="Bullet benefits (Max 20)")
    keywords_score: int = Field(..., ge=0, le=15, description="SEO keywords (Max 15)")
    compliance_score: int = Field(..., ge=0, le=15, description="Policy check (Max 15)")
    total_score: int = Field(..., ge=0, le=100)
    suggestions: List[str] = Field(default_factory=list)
    auto_improved: bool = False
    iterations: int = 1

class MarketplaceListing(BaseModel):
    title: str
    bullets: List[str]
    description: str
    keywords: List[str]
    urdu_summary: str
    platform_formatted: Dict[str, Any] = Field(default_factory=dict)

class MarketInsight(BaseModel):
    product_category: str
    suggested_price_usd: float
    market_price_min: float
    market_price_max: float
    market_price_avg: float
    demand_level: str
    top_buyer_countries: List[str]
    margin_estimate_pct: float
    recommendations: List[str]

class PublishRequest(BaseModel):
    platform: str = Field("alibaba", description="'alibaba', 'amazon', or 'both'")
    custom_title: Optional[str] = None
    custom_price: Optional[float] = None
    custom_moq: Optional[int] = None

class PublishResponse(BaseModel):
    success: bool
    platform: str
    listing_id: str
    status: str
    live_url: str
    published_at: str
    summary_urdu: str

class ListingRecord(BaseModel):
    id: str
    created_at: str
    updated_at: str
    raw_input: str
    normalized_text: str
    target_platform: str
    target_country: str
    attributes: ProductAttributes
    slots_status: SlotCheckResult
    listing: Optional[MarketplaceListing] = None
    quality_score: Optional[QualityScoreDetail] = None
    market_insight: Optional[MarketInsight] = None
    status: str = "draft"  # 'draft', 'needs_info', 'ready', 'published'
    published_platforms: Dict[str, Any] = Field(default_factory=dict)

class BuyerInquiryInput(BaseModel):
    listing_id: str
    buyer_name: str
    buyer_country: str
    inquiry_message: str

class ExporterReplyInput(BaseModel):
    urdu_response: str

class BuyerInquiryRecord(BaseModel):
    id: str
    listing_id: str
    buyer_name: str
    buyer_country: str
    inquiry_message: str
    intent: str
    catalog_answerable: bool
    requires_exporter: bool
    exporter_question_urdu: Optional[str] = None
    exporter_reply_urdu: Optional[str] = None
    generated_reply_en: Optional[str] = None
    status: str = "pending"  # pending, waiting_exporter, replied
    created_at: str
