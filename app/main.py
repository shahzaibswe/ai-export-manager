import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import auth, listings, market, inquiries, payment_tax
from app.models.database import db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="NLP-Powered Urdu-to-Global Export Listing Assistant for Pakistani Exporters (CoreTech Innovation)"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(market.router)
app.include_router(inquiries.router)
app.include_router(payment_tax.router)

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_product_icon(product_type: str, category: str) -> str:
    p = (product_type or "").lower()
    c = (category or "").lower()
    if "watch" in p or "timepiece" in c:
        return "fa-solid fa-clock"
    elif "toy" in p or "kids" in c:
        return "fa-solid fa-shapes"
    elif "football" in p or "soccer" in p or "ball" in p:
        return "fa-solid fa-futbol"
    elif "scissor" in p or "surgical" in c:
        return "fa-solid fa-scissors"
    elif "towel" in p or "textile" in c:
        return "fa-solid fa-scroll"
    elif "earbud" in p or "electronic" in c:
        return "fa-solid fa-headphones"
    elif "shoe" in p or "footwear" in c:
        return "fa-solid fa-shoe-prints"
    elif "jacket" in p or "leather" in c:
        return "fa-solid fa-vest"
    return "fa-solid fa-boxes-packing"

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Export Manager is running. Dashboard loading...</h1>"

@app.get("/presentation", response_class=HTMLResponse)
async def serve_presentation():
    deck_path = os.path.join(static_dir, "presentation_deck.html")
    if os.path.exists(deck_path):
        with open(deck_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Presentation Deck Loading...</h1>"

@app.get("/marketplace/alibaba/{listing_id}", response_class=HTMLResponse)
async def serve_alibaba_mock(listing_id: str):
    record = db.get_listing(listing_id)
    if not record:
        for r in db.list_all_listings():
            if r.get("published_platforms", {}).get("alibaba", {}).get("listing_id") == listing_id:
                record = r
                break

    if not record and listing_id == "sample":
        record = {
            "listing": {
                "title": "Luxury Quartz Chronograph Watch, Stainless Steel 316L, Water Resistant, Custom OEM Dial, MOQ 100",
                "bullets": [
                    "PRECISION QUARTZ TIMEKEEPING: Engineered with high-accuracy Japanese quartz movement and long-life battery.",
                    "PREMIUM STAINLESS STEEL CASING: Scratch-resistant hardened mineral crystal glass and 3ATM/5ATM water resistance.",
                    "BESPOKE PRIVATE LABEL OEM: Custom dial logo printing, engraved case-back, and luxury leatherette gift boxes.",
                    "DIRECT FACTORY EXPORT PRICING: Accessible wholesale MOQ of 100 pieces at $25.00/unit FOB with high retail margin.",
                    "WORLDWIDE EXPORT LOGISTICS: Rigorous pre-shipment quality inspection and rapid dispatch within 12 days to USA."
                ]
            },
            "attributes": {
                "product_type": "luxury_watches",
                "category": "Watches & Timepieces",
                "material": "Stainless Steel 316L",
                "unit_price_usd": 25.0,
                "moq": 100,
                "lead_time_days": 12
            }
        }
    elif not record:
        raise HTTPException(status_code=404, detail="Alibaba listing not found")

    ali_template = os.path.join(static_dir, "alibaba_preview.html")
    if os.path.exists(ali_template):
        with open(ali_template, "r", encoding="utf-8") as f:
            content = f.read()
            listing = record.get("listing", {})
            attrs = record.get("attributes", {})
            prod_type = attrs.get("product_type", "export_product")
            category = attrs.get("category", "General Export")
            mat = (attrs.get("material") or "High-Grade Export Material").title()
            icon_cls = get_product_icon(prod_type, category)

            content = content.replace("{{TITLE}}", listing.get("title", "Export Product"))
            content = content.replace("{{PRICE}}", f"${attrs.get('unit_price_usd', 40.0):.2f}")
            content = content.replace("{{MOQ}}", f"{attrs.get('moq', 500)} Units")
            content = content.replace("{{LEAD_TIME}}", f"{attrs.get('lead_time_days', 15)} Days")
            content = content.replace("{{MATERIAL}}", mat)
            content = content.replace("{{CATEGORY}}", category)
            content = content.replace("{{LISTING_ID}}", listing_id)
            content = content.replace("{{ICON_CLASS}}", icon_cls)
            bullets_html = "".join([f"<li>{b}</li>" for b in listing.get("bullets", [])])
            content = content.replace("{{BULLETS_HTML}}", bullets_html)
            return content
    return f"<h1>Alibaba Listing: {listing_id}</h1>"

@app.get("/marketplace/amazon/{listing_id}", response_class=HTMLResponse)
async def serve_amazon_mock(listing_id: str):
    record = db.get_listing(listing_id)
    if not record:
        for r in db.list_all_listings():
            if r.get("published_platforms", {}).get("amazon", {}).get("listing_id") == listing_id:
                record = r
                break

    if not record and listing_id == "sample":
        record = {
            "listing": {
                "title": "Luxury Quartz Chronograph Watch, Stainless Steel 316L, Water Resistant, Custom OEM Dial, MOQ 100",
                "bullets": [
                    "PRECISION QUARTZ TIMEKEEPING: Engineered with high-accuracy Japanese quartz movement and long-life battery.",
                    "PREMIUM STAINLESS STEEL CASING: Scratch-resistant hardened mineral crystal glass and 3ATM/5ATM water resistance.",
                    "BESPOKE PRIVATE LABEL OEM: Custom dial logo printing, engraved case-back, and luxury leatherette gift boxes.",
                    "DIRECT FACTORY EXPORT PRICING: Accessible wholesale MOQ of 100 pieces at $25.00/unit FOB with high retail margin.",
                    "WORLDWIDE EXPORT LOGISTICS: Rigorous pre-shipment quality inspection and rapid dispatch within 12 days to USA."
                ]
            },
            "attributes": {
                "product_type": "luxury_watches",
                "category": "Watches & Timepieces",
                "material": "Stainless Steel 316L",
                "unit_price_usd": 25.0,
                "moq": 100,
                "lead_time_days": 12
            }
        }
    elif not record:
        raise HTTPException(status_code=404, detail="Amazon listing not found")

    amz_template = os.path.join(static_dir, "amazon_preview.html")
    if os.path.exists(amz_template):
        with open(amz_template, "r", encoding="utf-8") as f:
            content = f.read()
            listing = record.get("listing", {})
            attrs = record.get("attributes", {})
            prod_type = attrs.get("product_type", "export_product")
            category = attrs.get("category", "General Export")
            mat = (attrs.get("material") or "High-Grade Export Material").title()
            icon_cls = get_product_icon(prod_type, category)

            content = content.replace("{{TITLE}}", listing.get("title", "Export Product"))
            content = content.replace("{{PRICE}}", f"${attrs.get('unit_price_usd', 40.0):.2f}")
            content = content.replace("{{MATERIAL}}", mat)
            content = content.replace("{{LISTING_ID}}", listing_id)
            content = content.replace("{{ICON_CLASS}}", icon_cls)
            bullets_html = "".join([f"<li>{b}</li>" for b in listing.get("bullets", [])])
            content = content.replace("{{BULLETS_HTML}}", bullets_html)
            return content
    return f"<h1>Amazon Listing: {listing_id}</h1>"

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "team": settings.TEAM_NAME,
        "version": settings.VERSION,
        "mode": "Hackathon MVP"
    }
