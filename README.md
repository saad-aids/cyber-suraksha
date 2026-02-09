# Cyber-Suraksha

AI-powered First Responder for Financial Fraud Recovery in Maharashtra.

## 🎯 Problem Statement

The "Cyber Golden Hour" - the first 60 minutes after a scam - is critical for freezing fraudulent transactions. Current systems (1930 helpline, NCRP) face delays due to GPS-based routing, complex forms, and manpower issues.

**Cyber-Suraksha** is an agentic AI system that acts as a first responder to:
- Classify scam types instantly
- Collect evidence efficiently
- Route to correct bank nodal officers
- Generate ready-to-submit reports

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HTML/CSS/JS Frontend                      │
│         (Fraud Reporting Wizard + Nodal Directory)          │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│                     FastAPI Backend                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              LangGraph 4-Node Workflow                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Triage   │→ │ Evidence │→ │  Nodal   │→ │ Portal   │    │
│  │ Auditor  │  │Collector │  │  Router  │  │ Reporter │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Gemini LLM API                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Create .env file in backend/
GOOGLE_API_KEY=your_gemini_api_key
```

### 3. Run the Application

```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Serve frontend
cd frontend
python -m http.server 5500
```

### 4. Open in Browser

Navigate to `http://localhost:5500`

## 📋 Features

| Feature | Description |
|---------|-------------|
| 🎯 Scam Classification | LLM-powered fraud type detection |
| ⏱️ Golden Hour Timer | Visual urgency countdown |
| 🏦 Nodal Officer Lookup | Direct bank contacts database |
| 📝 Report Generation | Maha-Cyber Portal ready format |
| 🔍 Suspect Check | I4C repository simulation |

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI
- **Orchestration**: LangChain + LangGraph
- **LLM**: Google Gemini API

## 📁 Project Structure

```
cyber-suraksha/
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── graph.py             # LangGraph workflow
│   ├── nodes/               # Agent nodes
│   └── data/                # Databases
├── frontend/
│   ├── index.html
│   ├── css/styles.css
│   └── js/
└── README.md
```

## 👥 Team

Built for **Agentic War Hackathon** - Full Stack AI Challenge

## 📄 License

MIT
