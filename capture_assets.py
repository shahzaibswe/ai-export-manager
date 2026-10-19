import os
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "presentation_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def capture_url(url: str, output_name: str, delay: int = 3, window_size: str = "1280,820"):
    output_path = os.path.join(ASSETS_DIR, output_name)
    args = [
        EDGE_PATH,
        "--headless",
        f"--screenshot={output_path}",
        f"--window-size={window_size}",
        "--hide-scrollbars",
        url
    ]
    print(f"Capturing {url} -> {output_name}...")
    try:
        subprocess.run(args, check=True, timeout=25)
        time.sleep(delay)
        if os.path.exists(output_path):
            print(f"Captured: {output_path} ({os.path.getsize(output_path)} bytes)")
            return output_path
    except Exception as e:
        print(f"Error capturing {url}: {e}")
    return None

def generate_architecture_diagram():
    """Draws a clean, professional 5-layer architecture diagram."""
    width, height = 1200, 700
    img = Image.new("RGB", (width, height), color=(15, 23, 42))  # Navy #0F172A
    draw = ImageDraw.Draw(img)

    layers = [
        ("1. CLIENT LAYER", ["Exporter Web Dashboard (Next.js / Responsive UI)", "Urdu & Roman Urdu Text / Voice Input (Whisper / Web Speech)", "Noto Nastaliq Urdu Typography", "Live Score Gauge & Feedback Meters"], (2, 132, 199)),
        ("2. APPLICATION LAYER", ["FastAPI Microservices Orchestrator", "JWT Authentication & Role Management", "Async Background Job Queue (Redis/RQ)", "Draft & Marketplace Version Store"], (99, 102, 241)),
        ("3. AI / NLP LAYER", ["Roman Urdu Text Preprocessor & Normalizer", "Pydantic-Validated NER Attribute Extraction", "Conversational Urdu Dialogue & Slot-Filling Manager", "Top-Seller RAG Vector Knowledge Base", "0-100 Rubric Quality Scorer & Auto-Improve Loop"], (168, 85, 247)),
        ("4. INTEGRATION LAYER", ["Mock Alibaba Trade Publish API (Verified Gold Supplier)", "Mock Amazon Selling Partner API (SP-API) Catalog", "Autonomous Buyer Negotiation Webhooks", "Payoneer vs Wise Gateway Fee Engine"], (245, 158, 11)),
        ("5. DATA LAYER", ["Relational SQLite Database (Users, Shops, Inquiries)", "Curated Top-Seller Sialkot/Faisalabad Vector Store", "Market Intelligence & Competitor Pricing Snapshots", "FBR 0.25% Export Tax Compliance Log"], (16, 185, 129))
    ]

    y_start = 30
    box_height = 115
    spacing = 16

    for idx, (title, points, color) in enumerate(layers):
        y = y_start + idx * (box_height + spacing)
        # Background box
        draw.rounded_rectangle([40, y, width - 40, y + box_height], radius=12, fill=(30, 41, 59), outline=color, width=2)
        # Title pill
        draw.rounded_rectangle([60, y + 12, 320, y + 40], radius=6, fill=color)
        draw.text((75, y + 16), title, fill=(255, 255, 255))
        # Points
        px = 350
        py = y + 12
        for p in points:
            draw.text((px, py), f"• {p}", fill=(226, 232, 240))
            py += 22

        # Connecting downward arrows
        if idx < len(layers) - 1:
            arrow_y = y + box_height
            draw.line([(width // 2, arrow_y), (width // 2, arrow_y + spacing)], fill=(148, 163, 184), width=3)

    out_path = os.path.join(ASSETS_DIR, "diagram_architecture.png")
    img.save(out_path)
    print(f"Generated: {out_path}")
    return out_path

def generate_methodology_diagram():
    """Draws a 7-stage NLP methodology flowchart with decision diamonds and feedback loops."""
    width, height = 1200, 720
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    steps = [
        ("START: Exporter Urdu Voice / Text Input", (56, 189, 248)),
        ("Stage 1: Preprocessing & Roman Urdu Normalization", (99, 102, 241)),
        ("Stage 2: NER Attribute Extraction (Pydantic Schema)", (168, 85, 247)),
        ("Decision: Are All Required Commercial Slots Present?", (245, 158, 11)),
        ("Stage 3: RAG Listing Generator (Title, 5 Bullets, 15 SEO Keywords)", (16, 185, 129)),
        ("Stage 4: Platform Formatter (Alibaba RFQ & Amazon SP-API)", (2, 132, 199)),
        ("Decision: Quality Score >= 80 / 100?", (244, 63, 94)),
        ("Stage 5: Human Review (Urdu Summary) -> One-Click Publish", (34, 197, 94))
    ]

    x = 100
    y_start = 25
    box_h = 55
    spacing = 30

    for idx, (title, color) in enumerate(steps):
        y = y_start + idx * (box_h + spacing)
        is_decision = "Decision" in title

        if is_decision:
            # Diamond shape representation
            draw.rounded_rectangle([x + 100, y, width - x - 100, y + box_h], radius=20, fill=(45, 30, 20) if "80" not in title else (50, 20, 30), outline=color, width=3)
            draw.text((x + 130, y + 16), f"◆ {title}", fill=color)
            # Side feedback loop note
            if "Slots" in title:
                draw.text((width - 320, y + 18), "[NO -> Urdu Follow-up Question]", fill=(251, 191, 36))
            else:
                draw.text((width - 320, y + 18), "[NO -> Auto-Improve Loop (Max 2x)]", fill=(244, 63, 94))
        else:
            draw.rounded_rectangle([x, y, width - x, y + box_h], radius=10, fill=(30, 41, 59), outline=color, width=2)
            draw.text((x + 30, y + 16), title, fill=(255, 255, 255))

        if idx < len(steps) - 1:
            draw.line([(width // 2, y + box_h), (width // 2, y + box_h + spacing)], fill=(148, 163, 184), width=2)

    out_path = os.path.join(ASSETS_DIR, "diagram_methodology.png")
    img.save(out_path)
    print(f"Generated: {out_path}")
    return out_path

if __name__ == "__main__":
    print("Generating diagrams...")
    generate_architecture_diagram()
    generate_methodology_diagram()

    print("Capturing live screenshots...")
    capture_url("http://127.0.0.1:8000/", "ss_dashboard.png")
    capture_url("http://127.0.0.1:8000/?preset=5", "ss_slot_followup.png", delay=3)
    capture_url("http://127.0.0.1:8000/?preset=2", "ss_listing_preview.png", delay=3)
    capture_url("http://127.0.0.1:8000/?preset=2&buyer=1", "ss_buyer_agent.png", delay=4)
    capture_url("http://127.0.0.1:8000/marketplace/alibaba/sample", "ss_alibaba.png")
    capture_url("http://127.0.0.1:8000/marketplace/amazon/sample", "ss_amazon.png")

    print("All presentation assets prepared successfully!")
