# DropWise AI

## AI-Powered Customer Drop-Off Intelligence Platform

DropWise AI is a multi-agent analytics system that helps e-commerce brands understand why customers leave without purchasing.

It analyzes customer session data, extracts behavioral signals, predicts drop-off reasons, generates explainable evidence, and recommends actions to improve conversion.

---

## Key Features

- Multi-agent drop-off analysis pipeline
- FastAPI backend
- React analytics dashboard
- Dataset upload and single-session upload
- Drop-off reason prediction
- Confidence scoring
- Evidence generation
- Business recommendations
- Charts and visual insights
- Reason vs confidence heatmap
- Session detail drawer
- PDF brand report export
- Future n8n automation-ready architecture

---

## Multi-Agent Pipeline

```text
Session Data
    ↓
Preprocessing Agent
    ↓
Behavior Extraction Agent
    ↓
Signal Detection Agent
    ↓
Reason Detection Agent
    ↓
Evidence Agent
    ↓
Recommendation Agent
    ↓
Analytics Dashboard
```

---

## Agents

### 1. Preprocessing Agent
Cleans and structures raw session data.

### 2. Behavior Extraction Agent
Extracts user behavior metrics such as price checks, coupon searches, review checks, cart additions, checkout attempts, and product visits.

### 3. Universal Signal Agent
Detects signals such as price sensitivity, trust seeking, checkout friction, delivery concern, and low purchase intent.

### 4. Reason Detection Agent
Predicts the most likely drop-off reason.

### 5. Evidence Agent
Generates evidence explaining why a reason was predicted.

### 6. Recommendation Agent
Suggests business actions to reduce similar future drop-offs.

---

## Drop-Off Reasons Detected

- Price Concern
- Trust Concern
- Product Fit Concern
- Product Information Gap
- Checkout Friction
- Delivery Concern
- Comparison Shopping
- Low Purchase Intent

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- React
- Vite
- Axios
- Chart.js

### Automation/Future Integration
- n8n
- Webhooks
- Google Sheets / Supabase
- Email / Slack alerts

---

## Project Structure

```text
DropWise-AI/
│
├── backend/
│   ├── agents/
│   ├── schemas/
│   ├── data/
│   ├── main.py
│   ├── evaluate_pipeline.py
│   ├── generate_sessions.py
│   ├── convert.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## API Endpoints

### Health Check

```http
GET /
```

### Analyze Single Session

```http
POST /upload-session
```

Accepts one `.json` session file.

### Analyze Full Dataset

```http
POST /upload-dataset
```

Accepts `.jsonl` dataset file.

---

## Sample Input Format

```json
{
  "session_id": "sess_123456",
  "user_id": "anon_1234",
  "device": "desktop",
  "events": [
    {
      "type": "page_view",
      "timestamp": 1718000000,
      "page": "/products/sample-product",
      "element": null,
      "depth_percent": null
    },
    {
      "type": "click",
      "timestamp": 1718000010,
      "page": "/products/sample-product",
      "element": "price",
      "depth_percent": null
    }
  ],
  "pages_visited": ["/", "/products/sample-product", "EXIT"]
}
```

---

## Sample Output

```json
{
  "predicted_reason": "price_concern",
  "secondary_reason": "checkout_friction",
  "confidence_score": 0.82,
  "confidence_level": "high",
  "evidence": [
    "User checked price-related elements multiple times.",
    "User searched for coupon or discount information."
  ],
  "recommended_actions": [
    "Show shipping charges earlier before the cart page.",
    "Offer limited-time coupons or first-order discounts."
  ]
}
```

---

## Dashboard Features

The dashboard provides:

- KPI summary cards
- Drop-off reason distribution chart
- Confidence split chart
- Prediction status chart
- Category-wise accuracy
- Average confidence by reason
- Secondary reason distribution
- Device distribution
- Review count by reason
- Model funnel
- AI dataset summary
- Reason vs confidence heatmap
- Search and filters
- Clickable session detail drawer
- PDF report export

---

## Evaluation

The current prototype was evaluated on synthetic e-commerce session data.

```text
Total Sessions: 80
Accuracy: 90%
Correct Predictions: 72
Review Needed: 8
```

---

## AI Dataset Summary Example

```text
34% users dropped due to Product Information Gap.
8 sessions need manual review.
Product Fit Concern has the lowest confidence.
Recommended Action: Improve PDP content, size guides, FAQs, and trust signals.
```

---

## n8n Automation Possibility

DropWise AI can be extended using n8n as an automation layer.

### Possible n8n Workflow

```text
Website / Session Tracker
        ↓
n8n Webhook
        ↓
FastAPI DropWise Backend
        ↓
Reason Detection
        ↓
Store Results in Google Sheets / Supabase
        ↓
Send Daily Brand Report
        ↓
Slack / Email Alerts
```

### Use Cases

- Real-time session ingestion
- Daily brand performance reports
- Drop-off spike alerts
- Automatic CSV/Google Sheet updates
- Email reports to brand owners
- Slack alerts for high checkout friction
- CRM integration

This makes DropWise AI scalable beyond a dashboard and turns it into an automated customer intelligence system.

---

## Business Impact

DropWise AI helps brands:

- Understand why users abandon sessions
- Improve conversion rates
- Prioritize UX improvements
- Identify product-page weaknesses
- Reduce checkout friction
- Improve customer trust
- Generate actionable recommendations

---

## Future Improvements

### Product Improvements

- Real website tracking integration
- Real-time clickstream ingestion
- Session replay integration
- Customer journey timeline
- Funnel drop-off analytics
- Cohort analysis
- User segmentation
- Exportable analytics reports

### AI Improvements

- LLM-based explanation agent
- Automatic business summary generation
- Conversational analytics assistant
- Predictive conversion scoring
- A/B test recommendation engine

### Automation Improvements

- n8n webhook pipeline
- Scheduled daily reports
- Slack/email alerts
- Supabase/PostgreSQL storage
- CRM integrations

### Deployment Improvements

- Deploy frontend on Vercel
- Deploy backend on Render
- Add authentication
- Add multi-brand workspace support

---

## How to Run Complete Project

### Terminal 1 — Backend

```bash
cd backend
uvicorn main:app --reload
```

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

## Hackathon Deliverables

This prototype includes:

- Source code
- FastAPI backend
- React frontend
- Synthetic dataset
- Technical documentation-ready architecture
- Dashboard screenshots
- PDF report export
- Demo-ready workflow

---

## Team

- Parv Gupta
- Tanishka Goyal
- Shagun Mishra

## Project Repository

GitHub Repository: https://github.com/Parv-Gpu/Dropwise-AI

---
