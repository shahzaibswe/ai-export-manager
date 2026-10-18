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

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Export Manager is running. Dashboard loading...</h1>"

@app.get("/marketplace/alibaba/{listing_id}", response_class=HTMLResponse)
async def serve_alibaba_mock(listing_id: str):
    record = db.get_listing(listing_id)
    # Check if id matched directly or in published_platforms
    if not record:
        for r in db.list_all_listings():
            if r.get("published_platforms", {}).get("alibaba", {}).get("listing_id") == listing_id:
                record = r
                break

    if not record:
        raise HTTPException(status_code=404, detail="Alibaba listing not found")

    ali_template = os.path.join(static_dir, "alibaba_preview.html")
    if os.path.exists(ali_template):
        with open(ali_template, "r", encoding="utf-8") as f:
            content = f.read()
            # Dynamic replacements
            listing = record.get("listing", {})
            attrs = record.get("attributes", {})
            content = content.replace("{{TITLE}}", listing.get("title", "Export Product"))
            content = content.replace("{{PRICE}}", f"${attrs.get('unit_price_usd', 40.0):.2f}")
            content = content.replace("{{MOQ}}", f"{attrs.get('moq', 500)} Pieces")
            content = content.replace("{{LEAD_TIME}}", f"{attrs.get('lead_time_days', 15)} Days")
            content = content.replace("{{MATERIAL}}", attrs.get("material", "Genuine Leather").title())
            content = content.replace("{{CATEGORY}}", attrs.get("category", "Leather Apparel"))
            content = content.replace("{{LISTING_ID}}", listing_id)
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

    if not record:
        raise HTTPException(status_code=404, detail="Amazon listing not found")

    amz_template = os.path.join(static_dir, "amazon_preview.html")
    if os.path.exists(amz_template):
        with open(amz_template, "r", encoding="utf-8") as f:
            content = f.read()
            listing = record.get("listing", {})
            attrs = record.get("attributes", {})
            content = content.replace("{{TITLE}}", listing.get("title", "Export Product"))
            content = content.replace("{{PRICE}}", f"${attrs.get('unit_price_usd', 40.0):.2f}")
            content = content.replace("{{MATERIAL}}", attrs.get("material", "Genuine Leather").title())
            content = content.replace("{{LISTING_ID}}", listing_id)
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
