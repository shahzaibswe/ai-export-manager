# AI Export Manager 🇵🇰 🌐
> **From Urdu description to a live global listing**  
> *Official NLP Hackathon Implementation for CoreTech Innovation*

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-11%20Passed-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Marketplaces-Alibaba%20%7C%20Amazon-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## 1. Problem Statement
Exporters in Pakistani industrial clusters such as **Sialkot** (leather goods, surgical instruments, sports gear) and **Faisalabad** (home textiles and cotton fabrics) manufacture world-class products. However, they face steep barriers when entering global digital trade:
- **Language Barrier:** Most small and medium exporters think, negotiate, and describe products in **Urdu** or **Roman Urdu**, whereas international B2B/B2C buyers on Alibaba and Amazon expect fluent, keyword-rich English.
- **Listing Complexity:** Every global marketplace enforces rigid title formatting, attributes, character limits, and SEO keyword conventions. Sub-par listings get buried in search algorithms.
- **Pricing Blind Spot:** Exporters frequently under- or over-price because they lack visibility into US and EU market willingness-to-pay.
- **Payment & Regulatory Confusion:** Navigating international payout rails (Payoneer vs Wise) and complying with FBR 0.25% concessionary export tax regimes and e-PRC certificates is cumbersome.
- **Time & Trust:** Manual copy-pasting is error-prone, and shop owners hesitate to hand over shop passwords.

---

## 2. Solution Overview
**AI Export Manager** eliminates these obstacles with an end-to-end, human-in-the-loop NLP pipeline. An exporter describes a product using spoken or typed Urdu/Roman Urdu, and the platform delivers:
1. **Automated Attribute Extraction (NER):** Parses product category, materials, sizing matrices, colorways, MOQ, unit prices, and lead times.
2. **Smart Urdu Dialogue Slot-Filler:** If key commercial parameters are missing (e.g. MOQ), the system prompts the exporter in conversational Urdu.
3. **Few-Shot RAG Listing Generation:** Crafts a marketplace-compliant title, 5 benefit-driven bullets, an SEO markdown overview, and 15 high-ranking keywords.
4. **Rubric-Based Quality Scorer & Auto-Improve Loop:** Evaluates the draft on a 0–100 scale; automatically refines drafts until score $\ge 80$.
5. **Market Intelligence & Price Insight:** Recommends optimal FOB prices and flags target market demand trends.
6. **One-Click Publish to Mock APIs:** Deploys listings to simulated **Alibaba Trade Showcase** and **Amazon SP-API** storefronts.
7. **Autonomous Buyer Communication Agent:** Classifies buyer inquiries and translates exporter replies from Urdu to professional B2B English.

---

## 3. Technology Stack

| Layer | Choice | Rationale |
|---|---|---|
| **Frontend** | Modern Responsive Dashboard (Tailwind CSS, FontAwesome, Noto Nastaliq Urdu) | Fast, mobile-responsive dashboard with real-time score gauges and audio simulation |
| **Backend API** | Python FastAPI + Uvicorn | High-performance asynchronous REST API for NLP orchestration |
| **NLP & Schemas** | Pydantic v2 + Regex normalizers + LLM-ready prompt templates | Type-safe structured extraction and validation |
| **Data Layer** | SQLite3 + In-Memory Caching | Embedded ACID-compliant persistence for drafts, shops, and inquiries |
| **Marketplaces** | Mock Alibaba Trade API + Mock Amazon SP-API | Reproducible end-to-end publishing without external API credential blockers |
| **Testing** | Pytest | 100% automated test coverage across extraction, slot filling, scoring, and endpoints |

---

## 4. Setup & Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Modern web browser (Chrome, Edge, Firefox)

### Installation Steps
```bash
# 1. Navigate to project directory
cd ai-export-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated test suite
python -m pytest tests/ -v

# 4. Launch the application
python run.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to access the live dashboard.

---

## 5. AI & NLP Methodology (7-Stage Pipeline)

```mermaid
flowchart TD
    A["Exporter Input (Urdu / Roman Urdu Text or Voice)"] --> B["Stage 1: Preprocess & Normalize (Unicode, Verbal Numbers)"]
    B --> C["Stage 2: NER & Attribute Extraction (Pydantic Schema)"]
    C --> D{"All Required Slots Present?"}
    D -- "No" --> E["Urdu Follow-up Question Prompt"]
    E --> A
    D -- "Yes" --> F["Stage 3: RAG Listing Generator (Title, 5 Bullets, 15 Keywords)"]
    F --> G["Stage 4: Platform Formatter (Alibaba / Amazon)"]
    G --> H{"Quality Score >= 80/100?"}
    H -- "No" --> I["Auto-Improve Loop (Re-prompt & Optimize)"]
    I --> H
    H -- "Yes" --> J["Stage 5: Human Review (Urdu Summary Approval)"]
    J --> K["Stage 6: One-Click Publish (Alibaba / Amazon API)"]
```

### 5.1 Quality Score Rubric (0–100 Points)
- **Required Attributes Complete (30 pts):** Material, size matrix, colors, MOQ, unit price, lead time.
- **Title Quality (20 pts):** Length optimization, primary keywords, zero spam.
- **Bullet Clarity & Buyer Benefits (20 pts):** 5 distinct commercial benefit bullets.
- **SEO Keywords (15 pts):** 15 high-intent export keywords.
- **Policy Compliance (15 pts):** Zero prohibited contact leaks (WhatsApp, phone numbers) or unsupported claims.

---

## 6. Model & API Usage

- **Input Normalization:** Translates Roman Urdu colloquialisms (`chamra` $\to$ leather, `paanch sau` $\to$ 500, `kam az kam` $\to$ MOQ).
- **RAG Store:** Vectorized knowledge base of top-performing export listings from Sialkot and Faisalabad.
- **LLM Integration Ready:** Direct drop-in hooks for Claude Sonnet or OpenAI / Gemini APIs via standard environment variables. Built-in deterministic NLP engine ensures 100% offline functionality for evaluators.

---

## 7. Key Features & Endpoints

### 7.1 Core Endpoints
- `POST /api/v1/listings/draft` — Submits Urdu input, executes normalization, extraction, and slot-checking.
- `POST /api/v1/listings/{id}/answer` — Submits answers to conversational Urdu follow-up prompts.
- `GET /api/v1/listings/{id}` — Fetches the generated draft, quality score, and Urdu summary.
- `POST /api/v1/listings/{id}/publish` — Publishes to Alibaba / Amazon mock APIs and returns live preview URLs.
- `GET /api/v1/market/insights?listing_id=...` — Returns price suggestions and demand benchmarks.
- `POST /api/v1/buyer/inquiries` — Simulates incoming international buyer requests.
- `POST /api/v1/buyer/inquiries/{id}/reply` — Translates exporter Urdu replies into tone-checked English quotes.
- `GET /api/v1/payment-tax/optimize` — Payoneer vs Wise optimizer and FBR 0.25% export tax calculation.

---

## 7.2 UI Layout & Live Screenshots

```
+----------------------------------------------------------------------------------------------------+
|  AI EXPORT MANAGER  [NLP HACKATHON MVP]                          DEMO DECK | DEMO: localhost:8000  |
+----------------------------------------------------------------------------------------------------+
| [EXPORTER INPUT (URDU / ROMAN URDU)]                               [PRESETS: Watches, Toys, Balls] |
| > "Mere paas luxury quartz watches hain stainless steel case aur leather strap ke sath..."         |
| [🎤 Voice Input]                                              [Process with NLP Engine ->]         |
+----------------------------------------------------------------------------------------------------+
| [SMART URDU FOLLOW-UP (If slots missing)]                                                          |
| "Aap ki Luxury Watches kis material ki bani hain? (Stainless Steel 316L, Leather Strap, Ceramic)"  |
+----------------------------------------------------------------------------------------------------+
| [RAG GENERATED LISTING PREVIEW]                      | [QUALITY SCORE RUBRIC (0-100)]              |
| Title: Luxury Quartz Chronograph Watch, 316L Steel...| Composite Score: 94 / 100 [PASSED >= 80]    |
| • 5 Buyer-Focused Benefit Bullets                    | Attributes (30) Title (20) Bullets (20)     |
| • 15 High-Intent SEO Keywords                        | Keywords (15) Policy Compliance (15)        |
| • Urdu Khulasa (Approval Summary)                    |---------------------------------------------|
| [APPROVE & PUBLISH TO MARKETPLACE ->]                | [MARKET INTELLIGENCE & PRICE RADAR]         |
| -> Alibaba Trade Showcase: /marketplace/alibaba/{id} | Suggested FOB: $31.25 (US Range: $15-$65)   |
| -> Amazon SP-API Catalog:  /marketplace/amazon/{id}  | Payment: Payoneer vs Wise (FBR 0.25% Tax)   |
+----------------------------------------------------------------------------------------------------+
| [BUYER COMMUNICATION AGENT SIMULATOR]                                                              |
| Buyer (Chicago, USA): "Can you do 200 watches with our custom logo on the dial? What is your FOB?" |
| AI Alert (Urdu): "USA buyer ne custom quote maangi hai. Aap ka kya rate hai?"                     |
| Exporter Reply: "iska rate 26 dollar hai aur 12 din lagain gay"                                   |
| AI English Output: "Dear Marcus Vance, our confirmed FOB unit price is $26.00 with 12 days lead..."|
+----------------------------------------------------------------------------------------------------+
```

---

## 7.3 Hackathon Demo Video Pitch Script (3-Minute Exact Cue)

| Timestamp | Screen Action | Speaker Narration Script |
|---|---|---|
| **0:00 – 0:30** | Show real Urdu handwritten/typed exporter quote | *"Exporters in Sialkot and Faisalabad manufacture world-class goods, but they lose 30% revenue because global buyers search in English. How does an Urdu speaker list on Alibaba and Amazon without middlemen?"* |
| **0:30 – 1:00** | Click preset or voice input on Dashboard | *"With AI Export Manager, the exporter speaks or types one natural Urdu sentence. Watch live as our NLP engine extracts the category, materials, MOQ, and unit price as verified attributes."* |
| **1:00 – 1:20** | Trigger missing slot on Surgical Scissors | *"If any critical parameter like MOQ is missing, the AI doesn't crash—it initiates a smart dialogue in natural Urdu asking for the missing info. The exporter replies casually, and the listing completes."* |
| **1:20 – 1:50** | Display generated listing & score gauge | *"Here is the generated English listing: marketplace-compliant title, 5 benefit-driven bullets, 15 SEO tags, and a 0-100 rubric score that automatically self-improves until it passes 80."* |
| **1:50 – 2:10** | Show Market Intelligence & Tax Card | *"Our pricing engine compares US/EU market willingness-to-pay ($31.25 suggested), while our compliance advisor calculates Payoneer vs Wise fees and FBR 0.25% export tax."* |
| **2:10 – 2:30** | Click 'Approve & Publish' | *"With one click, the exporter approves the Urdu summary, and the product goes live on our simulated Alibaba Trade Showcase and Amazon SP-API storefront with live ASINs."* |
| **2:30 – 3:00** | Simulate live Buyer Inquiry & Closing | *"When an international buyer sends an inquiry, our agent negotiates in Urdu with the exporter and replies in fluent B2B English. We are CoreTech Innovation, bringing Pakistani exporters directly to the global stage."* |

---

## 7.4 Presentation Deck & Pitch Resources
- **Interactive Web Deck:** Open [`http://127.0.0.1:8000/presentation`](http://127.0.0.1:8000/presentation) in any browser (Press `F11` for Fullscreen; navigate with Arrow Keys).
- **PowerPoint File:** [`AI_Export_Manager_Hackathon_Presentation.pptx`](file:///C:/Users/n%20tech/.gemini/antigravity/scratch/ai-export-manager/AI_Export_Manager_Hackathon_Presentation.pptx) (15 16:9 widescreen slides).

---

## 8. Team CoreTech Innovation

| Member | Position | Primary Responsibilities |
|---|---|---|
| **Sufyan Arain** | **Team Lead** | Project Architecture, Integration, Final Submission & Pitch |
| **Shahzaib Sheikh** | **Backend Developer** | FastAPI Core, Mock Marketplace APIs, SQLite Database |
| **Sehar** | **AI / ML Engineer** | NLP Pipeline, Prompt Schemas, Quality Scorer & RAG Store |
| **Nimra** | **UI / UX Designer & Frontend** | Dashboard Design, Noto Nastaliq Integration, Live Previews |
| **Zammad** | **Researcher & Documentation** | Exporter Benchmarks (Sialkot/Faisalabad), Test Suite & Documentation |

---

## 9. 12-Month Roadmap
- **Phase 1 (Month 1):** Hackathon MVP, 10 Sialkot exporter field interviews, Alibaba/Amazon developer account registration.
- **Phase 2 (Month 2–3):** Official OAuth2 Marketplace APIs, live Amazon SP-API and Alibaba Open Platform connect.
- **Phase 3 (Month 4–6):** Monetization ($29 Starter, $49 Pro, $99 Business), integrated Payoneer & Wise webhooks.
- **Phase 4 (Month 7–9):** Automated FBR e-PRC tax filing, Urdu mobile app for factory floor workers.
- **Phase 5 (Month 10–12):** Bulk 100-SKU upload, automated competitor price tracking, expansion across South Asia.

---

*Developed with pride for the NLP Hackathon 2026 by CoreTech Innovation.*
