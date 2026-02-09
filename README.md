# Cyber-Suraksha 🛡️

AI-powered First Responder for Financial Fraud Recovery in Maharashtra.

## 📺 Project Demo
Watch the official walkthrough: [https://youtu.be/ofjxcuQHB8c](https://youtu.be/ofjxcuQHB8c)

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
# Clone the repository
git clone https://github.com/saad-aids/cyber-suraksha.git
cd cyber-suraksha

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

## 🌟 Real Impact Stories
### The Trusted Office Boy (Mumbai Case)
In a recent incident, an office assistant misused a business smartphone to transfer **₹45,000** via UPI. By using Cyber-Suraksha's Nodal Router, the funds were successfully frozen within **20 minutes**, well within the Golden Hour window.

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6)
- **Backend**: FastAPI (Python)
- **Orchestration**: LangChain + LangGraph
- **LLM**: Google Gemini 1.5 Pro
- **API**: RBI Nodal Officer Database Integration

## 📁 Project Structure
```
cyber-suraksha/
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── graph.py             # LangGraph workflow
│   ├── nodes/               # Agent nodes (Triage, Evidence, etc.)
│   └── data/                # Nodal Officers & Scam Types Data
├── frontend/
│   ├── index.html           # Main UI
│   ├── css/styles.css       # Custom styling
│   └── js/                  # App logic & Wizard workflow
├── .gitignore
└── README.md
```

## 👥 Team
Built for **Agentic War Hackathon 2026** - Full Stack AI Challenge.
Developer: **Saad-aids**

## 📄 License
MIT
