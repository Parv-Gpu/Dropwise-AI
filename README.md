# DropWise AI

<p align="center">
  <img src="assets/dashboard-main.png" width="100%">
</p>

<h3 align="center">
AI-Powered Customer Drop-Off Intelligence Platform
</h3>

<p align="center">
Identify why customers leave without purchasing using a Multi-Agent AI System.
</p>

---

# Overview

DropWise AI is an AI-powered customer behavior intelligence platform designed for ecommerce brands.

Instead of only showing metrics like:

- Page Views
- Sessions
- Clicks
- Bounce Rate

DropWise AI explains:

> Why did this customer leave without purchasing?

The platform uses a Multi-Agent AI Pipeline to analyze session behavior, detect intent signals, predict drop-off reasons, generate evidence, and recommend business actions.

---

# Problem Statement

Ecommerce brands generate thousands of customer sessions daily.

Traditional analytics tools can show:

- What happened
- When it happened

But they cannot explain:

- Why users left
- What caused abandonment
- Which issue should be fixed first

Manual session analysis is expensive and not scalable.

DropWise AI automatically identifies drop-off reasons and provides actionable recommendations.

---

# System Architecture

<p align="center">
  <img src="assets/system-architecture.png" width="100%">
</p>

### Architecture Components

### Data Sources

- Website / Ecommerce Store
- Session Tracker
- Event Logs
- Uploaded JSON / JSONL Files
- Synthetic Datasets

### Ingestion Layer

- FastAPI Backend
- Dataset Upload
- Session Upload
- Input Validation
- Structured Parsing

### Multi-Agent Pipeline

#### 1. Preprocessing Agent

- Cleans session data
- Normalizes input
- Generates structured session objects

#### 2. Behavior Extraction Agent

Extracts:

- Price checks
- Coupon searches
- Review interactions
- Checkout attempts
- Delivery checks
- Product page visits

#### 3. Signal Detection Agent

Detects:

- Price Sensitivity
- Trust Seeking
- Delivery Concern
- Checkout Friction
- Product Fit Concern
- Comparison Shopping

#### 4. Reason Detection Agent

Predicts:

- Primary Reason
- Secondary Reason
- Confidence Score

#### 5. Evidence Agent

Generates explainable evidence.

#### 6. Recommendation Agent

Generates business recommendations.

---

# Features

## Dataset Analysis

Upload a JSONL dataset and instantly analyze:

- Total Sessions
- Accuracy
- Review Required Sessions
- Confidence Distribution
- Drop-Off Distribution

---

## Session Intelligence

Analyze individual customer sessions using:

- Session ID
- User ID

View:

- Evidence
- Signals
- Behavior Metrics
- Recommendations

---

## AI Dataset Summary

Automatically generates business insights:

- Top drop-off reason
- Lowest confidence category
- Most reviewed reason
- Recommended action

---

## PDF Report Export

Generate downloadable business reports containing:

- Dashboard Summary
- Accuracy Metrics
- Recommendations
- Charts
- Insights

---

# Dashboard Screenshots

## Main Dashboard

<p align="center">
  <img src="assets/dashboard-main.png" width="100%">
</p>

---

## Top Insights + Reason Distribution

<p align="center">
  <img src="assets/dashboard-insights.png" width="100%">
</p>

---

## Accuracy & Confidence Analytics

<p align="center">
  <img src="assets/dashboard-analytics.png" width="100%">
</p>

---

## Heatmap Analysis

<p align="center">
  <img src="assets/dashboard-heatmap.png" width="100%">
</p>

---

## Review Funnel & Quality Metrics

<p align="center">
  <img src="assets/dashboard-review.png" width="100%">
</p>

---

# Dashboard Analytics

The dashboard provides:

### KPI Cards

- Total Sessions
- Accuracy
- Correct Predictions
- Review Needed
- Average Confidence
- Unique Reasons

### Insight Cards

- Top Drop-Off Reason
- Most Review Needed Reason
- Lowest Confidence Reason
- Best Performing Category

### Interactive Charts

- Drop-Off Reason Distribution
- Confidence Split
- Prediction Status
- Category-wise Accuracy
- Average Confidence by Reason
- Secondary Reason Distribution
- Device Distribution
- Review Count by Reason
- Model Funnel

### Heatmap

Reason vs Confidence Matrix

Helps identify:

- High-confidence categories
- Weak prediction areas
- Categories requiring model tuning

---

# Multi-Agent Pipeline

```text
Customer Session Data
         │
         ▼
Preprocessing Agent
         │
         ▼
Behavior Extraction Agent
         │
         ▼
Signal Detection Agent
         │
         ▼
Reason Detection Agent
         │
         ▼
Evidence Agent
         │
         ▼
Recommendation Agent
         │
         ▼
Analytics Dashboard
```

---

# Drop-Off Reasons Supported

- Price Concern
- Trust Concern
- Product Information Gap
- Product Fit Concern
- Checkout Friction
- Delivery Concern
- Comparison Shopping
- Low Purchase Intent

---

# Tech Stack

## Frontend

- React
- Vite
- Axios
- Chart.js
- html2canvas
- jsPDF

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## AI Layer

- Groq LLM
- Prompt Engineering
- Multi-Agent Architecture

## Deployment

### Frontend

- Vercel

### Backend

- Render

---

# Project Structure

```bash
DropWise-AI
│
├── backend
│   ├── agents
│   ├── schemas
│   ├── data
│   ├── main.py
│   ├── evaluate_pipeline.py
│   ├── generate_sessions.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
├── assets
│   ├── system-architecture.png
│   ├── dashboard-main.png
│   ├── dashboard-insights.png
│   ├── dashboard-analytics.png
│   ├── dashboard-heatmap.png
│   └── dashboard-review.png
│
└── README.md
```

---

# Local Setup

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Live Deployment

## Frontend

```text
https://dropwise-ai.vercel.app/
```

## Backend

```text
https://dropwise-ai-backend.onrender.com
```

## GitHub Repository

```text
https://github.com/Parv-Gpu/Dropwise-AI
```

---

# Future Improvements

- Real Session Replay Integration
- Live Website Tracking
- n8n Automation Workflows
- Slack Notifications
- Email Reports
- Google Sheets Sync
- CRM Integration
- Predictive Conversion Scoring
- Customer Journey Visualization
- Real-Time Alerts

---

# Team

### Parv Gupta

### Tanishka Goyal

### Shagun Mishra

---

# Hackathon Submission

Built for:

**Bharat Academix CodeQuest 2026**

Theme:

**AI/ML Solutions for Real-World Problems**

---

# 📄 License

This project is intended for educational, research, and hackathon purposes.
