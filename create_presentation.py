import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "presentation_assets")

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    C_NAVY = RGBColor(15, 23, 42)        # #0F172A
    C_BLUE = RGBColor(2, 132, 199)       # #0284C7
    C_EMERALD = RGBColor(16, 185, 129)   # #10B981
    C_AMBER = RGBColor(245, 158, 11)     # #F59E0B
    C_WHITE = RGBColor(255, 255, 255)
    C_GRAY = RGBColor(100, 116, 139)     # #64748B
    C_DARK_CARD = RGBColor(30, 41, 59)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="CORETECH INNOVATION | NLP HACKATHON 2026"):
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = C_NAVY
        header_shape.line.color.rgb = C_NAVY

        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(8), Inches(0.3))
        p_cat = cat_box.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE

        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(10), Inches(0.55))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        tag_box = slide.shapes.add_textbox(Inches(10.2), Inches(0.35), Inches(2.6), Inches(0.4))
        p_tag = tag_box.text_frame.paragraphs[0]
        p_tag.text = "DEMO: http://127.0.0.1:8000"
        p_tag.font.size = Pt(9)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_EMERALD

    def add_card(slide, left, top, width, height, title, items, badge_text=None, border_color=C_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_WHITE
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.18)
        tf.margin_right = Inches(0.2)
        tf.margin_bottom = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = C_NAVY

        if badge_text:
            p_b = tf.add_paragraph()
            p_b.text = f"[{badge_text}]"
            p_b.font.size = Pt(9)
            p_b.font.bold = True
            p_b.font.color.rgb = C_EMERALD
            p_b.space_after = Pt(3)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(10)
            p.font.color.rgb = C_GRAY
            p.space_after = Pt(2)

    def add_image_if_exists(slide, img_name, left, top, width, height, caption=None):
        img_path = os.path.join(ASSETS_DIR, img_name)
        if os.path.exists(img_path):
            pic = slide.shapes.add_picture(img_path, left, top, width, height)
            if caption:
                cap_box = slide.shapes.add_textbox(left, top + height + Inches(0.05), width, Inches(0.35))
                p = cap_box.text_frame.paragraphs[0]
                p.text = caption
                p.font.size = Pt(9)
                p.font.bold = True
                p.font.color.rgb = C_GRAY
            return pic
        return None

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.color.rgb = C_NAVY

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11), Inches(4.8))
    tf1 = tb.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CORETECH INNOVATION | OFFICIAL NLP HACKATHON 2026 SUBMISSION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "AI Export Manager"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf1.add_paragraph()
    p.text = "From Urdu description to a live global listing on Alibaba and Amazon"
    p.font.size = Pt(21)
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Team Lead: Sufyan Arain | Shahzaib Sheikh | Sehar | Nimra | Zammad"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf1.add_paragraph()
    p.text = "Working Product URL: http://127.0.0.1:8000 • Sialkot & Faisalabad Export Clusters"
    p.font.size = Pt(12)
    p.font.color.rgb = C_EMERALD

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement: The Exporter Language & Know-How Barrier")

    add_card(s2, Inches(0.8), Inches(1.4), Inches(3.6), Inches(5.4),
             "1. Language Barrier",
             [
                 "Pakistani manufacturers in Sialkot (leather, surgical, sports) and Faisalabad (textiles) think, sell, and negotiate in Urdu or Roman Urdu.",
                 "Global buyers on Alibaba and Amazon search strictly in commercial, keyword-rich English.",
                 "Traditional translators lack export trade terminology, resulting in lost ranking and buyer confusion."
             ], "CRITICAL BARRIER", C_AMBER)

    add_card(s2, Inches(4.8), Inches(1.4), Inches(3.6), Inches(5.4),
             "2. Marketplace Complexity",
             [
                 "Alibaba & Amazon enforce strict character limits, mandatory 5-bullet benefit structures, and backend SEO tags.",
                 "Exporters struggle to format titles, attributes, and search keywords for algorithmic visibility.",
                 "Manual copy-pasting between external tools is slow, confusing, and prone to costly compliance errors."
             ], "COMPLIANCE & SEO", C_BLUE)

    add_card(s2, Inches(8.8), Inches(1.4), Inches(3.6), Inches(5.4),
             "3. Pricing & Compliance Blindspots",
             [
                 "Exporters rarely know US and EU market willingness-to-pay and consistently under-price by 20% to 30%.",
                 "Choosing between Payoneer and Wise for international payouts is confusing.",
                 "FBR 0.25% export tax regime and bank e-PRC requirements are hard to navigate."
             ], "REVENUE LOSS", C_EMERALD)

    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION OVERVIEW
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Proposed Solution: End-to-End AI Export Assistant")

    add_card(s3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(2.6),
             "Urdu-First Product Capture",
             [
                 "Speak or type in conversational Urdu or Roman Urdu.",
                 "Preprocesses unicode and normalizes verbal numbers ('paanch sau' -> 500, 'challis dollar' -> $40, 'chamra' -> leather).",
                 "Speech-to-Text integration via Web Audio / Speech API."
             ], "VOICE & TEXT", C_BLUE)

    add_card(s3, Inches(6.8), Inches(1.4), Inches(5.6), Inches(2.6),
             "Smart Urdu Slot-Filling Dialogue",
             [
                 "Category-specific schema validation.",
                 "If key commercial attributes (MOQ, material, dimensions) are missing, the AI prompts the exporter in natural conversational Urdu.",
                 "Dynamically adapts to ANY product (Watches, Toys, Balls, Apparel, Surgical)."
             ], "ACTIVE DIALOGUE", C_AMBER)

    add_card(s3, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6),
             "RAG Generation & 0-100 Quality Scorer",
             [
                 "Curated top-seller style retrieval creates marketplace-ready titles, 5 benefit-driven bullets, and 15 SEO keywords.",
                 "Official 5-dimension rubric judges completeness (0-100).",
                 "Auto-improve feedback loop refines listing until score >= 80."
             ], "HIGH CONVERSION", C_EMERALD)

    add_card(s3, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.6),
             "1-Click Publish & Negotiation Agent",
             [
                 "One-click publish to simulated Alibaba Trade Showcase & Amazon SP-API.",
                 "Autonomous Buyer Communication Agent translates exporter's casual Urdu replies into tone-checked, professional B2B export English quotes."
             ], "HUMAN-IN-THE-LOOP", C_NAVY)

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (WITH VISUAL DIAGRAM)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture: 5-Layer Engineering Flow")

    # Embed visual diagram
    add_image_if_exists(s4, "diagram_architecture.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Figure: Five-Layer Production System Architecture (CoreTech Innovation)")

    add_card(s4, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "Architectural Highlights",
             [
                 "1. Client Layer: Responsive web dashboard supporting Urdu/Roman Urdu text, voice recording, live chips, and preview tabs.",
                 "2. Application Layer: FastAPI microservice orchestrator handling async NLP execution, JWT auth, and draft persistence.",
                 "3. AI/NLP Layer: Preprocessor, Pydantic NER extractor, slot dialogue manager, RAG vector store, and rubric judge.",
                 "4. Integration Layer: Mock Alibaba Publish API and Amazon SP-API with realistic ASIN and listing ID allocation.",
                 "5. Data Layer: SQLite database storing users, shops, listings, market benchmarks, and buyer inquiry logs."
             ], "5-LAYER DESIGN", C_BLUE)

    # =========================================================================
    # SLIDE 5: NLP METHODOLOGY (WITH VISUAL FLOWCHART)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Methodology: 7-Stage NLP Pipeline & Quality Feedback Loops")

    add_image_if_exists(s5, "diagram_methodology.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Figure: 7-Stage NLP Methodology Flowchart with Slot-Filling & Auto-Improve Feedback Loops")

    add_card(s5, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "Pipeline Stages & Quality Rubric",
             [
                 "Stage 0-1: Capture & Preprocess (Unicode normalization, verbal numbers, unit mapping).",
                 "Stage 2: Structured NER extraction validated with Pydantic JSON schema.",
                 "Stage 3: Slot checking against category schema; generates conversational Urdu follow-up if missing.",
                 "Stage 4: Prompted LLM / RAG listing generator (title, 5 bullets, 15 SEO tags).",
                 "Stage 5: Platform formatter (Alibaba 128-char limit & Amazon SP-API schema).",
                 "Stage 6: 0-100 Rubric Scorer. If score < 80, auto-improves (up to 2 iterations).",
                 "Stage 7: Exporter reviews Urdu summary and clicks Approve to publish live."
             ], "7-STAGE PIPELINE", C_EMERALD)

    # =========================================================================
    # SLIDE 6: UNIVERSAL PRODUCT INTELLIGENCE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Universal Product Intelligence: Dynamic for ANY Industry")

    prods = [
        ("⌚ Watches & Timepieces", ["Detects Quartz, Chronograph, Smartwatches", "Follow-up: Stainless Steel 316L, Leather Strap, Water Resistance", "Generates dial logo OEM & luxury presentation packaging"]),
        ("🧸 Toys & Kids Products", ["Detects STEM toys, plush, dolls, RC models", "Follow-up: Non-toxic ABS plastic, solid wood, child age group", "Generates ASTM F963 & EN71 child safety compliance bullets"]),
        ("⚽ Sports Goods & Balls", ["Detects Match Footballs, Soccer, Cricket, Boxing", "Follow-up: PU leather, 32 panels, official Size 5", "Generates tournament aerodynamic flight & federation branding"]),
        ("🧥 Leather & Textiles", ["Detects Leather jackets, coats, hotel towels", "Follow-up: Genuine cowhide, cotton GSM, M-XXL sizing", "Generates Sialkot/Faisalabad export advantage bullets"])
    ]

    for idx, (title, items) in enumerate(prods):
        left_pos = Inches(0.8 + (idx % 2) * 6.0)
        top_pos = Inches(1.4 + (idx // 2) * 2.7)
        add_card(s6, left_pos, top_pos, Inches(5.6), Inches(2.4),
                 title, items, "CATEGORY ADAPTIVE", C_EMERALD if idx % 2 == 1 else C_BLUE)

    # =========================================================================
    # SLIDE 7: LIVE SCREENSHOT: DASHBOARD & PRESETS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Live UI Screenshot: Exporter Dashboard & Presets")

    add_image_if_exists(s7, "ss_dashboard.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Screenshot 1: Live Web Dashboard with One-Click Exporter Presets & Urdu Input (localhost:8000)")

    add_card(s7, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "Dashboard Features",
             [
                 "1. Bilingual Header: CoreTech Innovation branding, Sialkot/Faisalabad cluster badge, and PPT Deck link.",
                 "2. One-Click Exporter Presets: Pre-configured test benchmarks for Leather Jackets, Watches, Toys, Footballs, Surgical Scissors, and Towels.",
                 "3. Voice / Text Input Box: Exporter enters natural Urdu or Roman Urdu with microphone capture simulation.",
                 "4. Target Marketplace Selector: One-click selection for Alibaba (B2B), Amazon (B2C), or Both.",
                 "5. Target Country Selector: USA, UK, Germany, UAE."
             ], "LIVE DASHBOARD", C_BLUE)

    # =========================================================================
    # SLIDE 8: LIVE SCREENSHOT: SMART URDU FOLLOW-UP (SLOT LOOP)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Live UI Screenshot: Smart Urdu Slot-Filling Loop")

    add_image_if_exists(s8, "ss_slot_followup.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Screenshot 2: AI Dialog Manager detecting missing MOQ on Surgical Scissors and prompting in Urdu")

    add_card(s8, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "Conversational Slot Filling",
             [
                 "• Missing Attribute Detection: The Pydantic schema checks if required commercial slots are present.",
                 "• Natural Urdu Prompting: When missing MOQ, the system renders a prominent conversational alert card in Urdu font (Noto Nastaliq Urdu).",
                 "• Zero Middleman Friction: The exporter types an answer casually (e.g. 'MOQ 500 pieces').",
                 "• Dynamic Product-Specific Questions: For watches, it asks about case material; for toys, child safety & age group; for balls, ball size matrix."
             ], "URDU DIALOGUE LOOP", C_AMBER)

    # =========================================================================
    # SLIDE 9: LIVE SCREENSHOT: GENERATED LISTING & 0-100 SCORER
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Live UI Screenshot: RAG Listing Preview & Quality Scorer")

    add_image_if_exists(s9, "ss_listing_preview.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Screenshot 3: RAG Listing Output (Title, 5 Bullets, 15 Keywords) and 0-100 Rubric Quality Gauge")

    add_card(s9, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "High-Converting Export Listing",
             [
                 "• Title Optimization: Character-length compliant title with primary commercial keywords.",
                 "• 5 Buyer-Focused Bullets: Structured around durability, OEM customization, factory direct pricing, and transit timelines.",
                 "• 15 Backend SEO Keywords: High-intent B2B search terms for North America and European buyers.",
                 "• Quality Rubric Score: Evaluated across 5 dimensions with a 94/100 composite score.",
                 "• Urdu Approval Summary: Exporter reviews an Urdu summary before approving for publish."
             ], "EXPORT-READY OUTPUT", C_EMERALD)

    # =========================================================================
    # SLIDE 10: LIVE SCREENSHOTS: ALIBABA & AMAZON PUBLISHING
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Live Marketplace Previews: Alibaba Trade & Amazon SP-API")

    add_image_if_exists(s10, "ss_alibaba.png", Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.4),
                        "Screenshot 4: Verified Alibaba Gold Supplier Showcase (/marketplace/alibaba/sample)")

    add_image_if_exists(s10, "ss_amazon.png", Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4),
                        "Screenshot 5: Amazon Seller Central Buy Box & SP-API Catalog (/marketplace/amazon/sample)")

    # =========================================================================
    # SLIDE 11: LIVE SCREENSHOT: BUYER COMMUNICATION AGENT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Live UI Screenshot: Buyer Communication Agent Simulator")

    add_image_if_exists(s11, "ss_buyer_agent.png", Inches(0.8), Inches(1.4), Inches(7.4), Inches(5.4),
                        "Screenshot 6: Buyer RFQ received -> Urdu escalation alert -> Synthesized B2B English reply")

    add_card(s11, Inches(8.5), Inches(1.4), Inches(4.0), Inches(5.4),
             "Autonomous Negotiation Loop",
             [
                 "1. Incoming Buyer Message: Commercial buyer in Chicago inquires: 'Can you do 200 watches with custom logo on the dial? What is your FOB price?'.",
                 "2. AI Agent Urdu Alert: Agent translates inquiry intent and alerts the exporter in Urdu: 'USA ke buyer ne custom quote maanga hai. Aap ka kya rate hai?'.",
                 "3. Exporter Casual Urdu Reply: Exporter responds casually: 'iska rate 26 dollar hai aur 12 din lagain gay'.",
                 "4. Synthesized English Quote: Agent crafts a courteous, tone-checked B2B quotation confirming $26.00 FOB price and 12-day turnaround."
             ], "NEGOTIATION AGENT", C_NAVY)

    # =========================================================================
    # SLIDE 12: FINANCIAL & REGULATORY COMPLIANCE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Financial & Compliance: Payment Optimizer & FBR 0.25% Tax")

    add_card(s12, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4),
             "Payment Gateway Optimizer",
             [
                 "• Payoneer vs Wise Fee Comparison: Evaluates transaction fees and foreign exchange margins based on buyer country.",
                 "• USA & North America Orders: Recommends Payoneer for direct integration with Amazon payouts and Alibaba Trade Assurance disbursements.",
                 "• UK & European Orders: Recommends Wise Business for direct SEPA / IBAN bank transfers with lower conversion spreads.",
                 "• Transparent Fee Breakdown: Displays estimated gateway fees and net exporter payout in USD & PKR."
             ], "GATEWAY OPTIMIZER", C_BLUE)

    add_card(s12, Inches(6.8), Inches(1.4), Inches(5.6), Inches(5.4),
             "FBR 0.25% Export Tax Regime",
             [
                 "• Concessionary Export Slab: Guides manufacturers to qualify for the 0.25% Final Tax Regime under PSEB & Export Incentive policies (saving 0.75% vs standard 1% withholding).",
                 "• Electronic Proceeds Realization Certificate (e-PRC): Emphasizes obtaining digital e-PRC certificates from commercial Pakistani banks upon remittance arrival.",
                 "• Exporter Guidance in Urdu: Delivers clear, non-technical tax advice so factory owners stay fully compliant without hiring expensive consultants."
             ], "FBR TAX COMPLIANCE", C_EMERALD)

    # =========================================================================
    # SLIDE 13: 3-MINUTE DEMO VIDEO PITCH SCRIPT
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Hackathon Demo Pitch Video Script (Exact 3-Minute Timing)")

    cues = [
        ("0:00 - 0:30", "The Hook & Problem", "Show a real Urdu description from a Sialkot exporter. Ask: 'How does an Urdu speaker reach buyers in the USA without getting ripped off?'"),
        ("0:30 - 1:00", "Voice / Urdu Input", "Speak or type the Urdu sentence into the dashboard. Show live extracted tags (Product, Material, MOQ, Price) appearing instantly."),
        ("1:00 - 1:20", "Smart Urdu Slot Loop", "Demonstrate missing MOQ on surgical scissors. System asks conversational Urdu question. Answer it, watch listing complete."),
        ("1:20 - 1:50", "RAG Output & 0-100 Score", "Showcase generated English title, 5 bullets, 15 SEO keywords. Point to 0-100 quality score gauge and auto-improve loop."),
        ("1:50 - 2:10", "Market Intelligence", "Show suggested price ($48 vs $40 base), margin radar (+32%), and Payoneer vs Wise FBR 0.25% tax guidance."),
        ("2:10 - 2:30", "1-Click Publish Live", "Click 'Approve & Publish'. Open live Alibaba Trade Showcase and Amazon SP-API pages with live URLs."),
        ("2:30 - 3:00", "Buyer Agent & Roadmap", "Demonstrate live buyer inquiry simulation; state honest MVP limitations (mock APIs) and Phase 2-5 roadmap.")
    ]

    for idx, (time_slot, title, script) in enumerate(cues):
        top_pos = Inches(1.35 + idx * 0.78)
        shape = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), Inches(0.68))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_WHITE
        shape.line.color.rgb = C_AMBER if idx in [1, 2, 5] else C_BLUE
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = f"[{time_slot}] {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_NAVY
        run = p.add_run()
        run.text = script
        run.font.bold = False
        run.font.size = Pt(10)
        run.font.color.rgb = C_GRAY

    # =========================================================================
    # SLIDE 14: BUSINESS MODEL & 12-MONTH ROADMAP
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Business Model & 12-Month Execution Roadmap")

    add_card(s14, Inches(0.8), Inches(1.4), Inches(3.6), Inches(5.4),
             "SaaS Pricing Tiers",
             [
                 "Starter ($29/mo): Urdu-to-English listings, Alibaba & Amazon formatting, quality scoring.",
                 "Pro ($49/mo): Everything in Starter + Market pricing intelligence + Payment optimizer.",
                 "Business ($99/mo): Everything in Pro + Buyer reply agent + FBR tax reports + Priority dispatch.",
                 "Path to $1M ARR: 100 paid users by Month 6 ($5k/mo); 1,000+ paid users by Month 12 ($50k+/mo)."
             ], "SUBSCRIPTION TIERS", C_BLUE)

    add_card(s14, Inches(4.8), Inches(1.4), Inches(7.6), Inches(5.4),
             "12-Month Execution Roadmap",
             [
                 "Phase 1 (Day 1 - Month 1) [Hackathon MVP]: Working demo, 10 exporter interviews in Sialkot, apply for Alibaba & Amazon developer accounts.",
                 "Phase 2 (Months 2 - 3) [Official APIs]: Live OAuth2 marketplace connectors, real-time Alibaba RFQ & Amazon SP-API feeds, free beta with 50 exporters.",
                 "Phase 3 (Months 4 - 6) [Monetization]: Stripe & Safepay billing live, payment optimizer, tax module launch, target: 100 paying customers ($5k/mo).",
                 "Phase 4 (Months 7 - 9) [Scaling]: Buyer auto-reply agent, mobile app for factory managers, regional expansion to Bangladesh & Sri Lanka.",
                 "Phase 5 (Months 10 - 12) [Market Leader]: 100-SKU bulk catalog importer, automated competitor price tracking alerts, factory direct sales team."
             ], "5-PHASE STAGED EXECUTION", C_EMERALD)

    # =========================================================================
    # SLIDE 15: TEAM CORETECH INNOVATION & DELIVERABLES
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Team CoreTech Innovation & Shared Responsibilities")

    members = [
        ("Sufyan Arain", "Team Lead", "Project architecture, integration, demo pitch, final submission delivery"),
        ("Shahzaib Sheikh", "Backend Developer", "FastAPI microservices, mock marketplace APIs, SQLite database schema"),
        ("Sehar", "AI / ML Engineer", "NLP pipeline, prompt engineering, rubric scoring engine, RAG store"),
        ("Nimra", "UI / UX Designer & Frontend", "Responsive dashboard layout, Noto Nastaliq Urdu styling, live preview pages"),
        ("Zammad", "Researcher & Documentation", "Sialkot/Faisalabad export pain points, test datasets, README & pitch script")
    ]

    for idx, (name, role, resp) in enumerate(members):
        top_pos = Inches(1.4 + idx * 1.05)
        shape = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.7), Inches(0.92))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_WHITE
        shape.line.color.rgb = C_BLUE
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = f"{name} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY
        run_role = p.add_run()
        run_role.text = f"— {role.upper()}"
        run_role.font.bold = True
        run_role.font.size = Pt(11)
        run_role.font.color.rgb = C_BLUE

        p2 = tf.add_paragraph()
        p2.text = f"Primary Contributions: {resp}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_GRAY

    # Save presentation
    output_path = os.path.join(BASE_DIR, "AI_Export_Manager_Hackathon_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully generated with embedded diagrams and screenshots: {output_path}")

if __name__ == "__main__":
    create_deck()
