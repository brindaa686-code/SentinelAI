SentinelAI — Cybersecurity Threat Detection & Response Agent
    SentinelAI is an AI-powered cybersecurity monitoring agent that reads firewall
log data, detects attacks based on the characteristics of each log entry,
scores the risk, takes an automated response action, and then explains the
findings to the user in plain language through a conversational dashboard.

Unlike a typical rule-based log scanner, SentinelAI is designed to *talk* to
the user — a local LLM (via [Ollama](https://ollama.com)) turns raw detection
labels into a clear, human-readable summary with a suggested next step.

 Architecture

The project is split into two independently runnable parts:


cyber_ai_agent/
├── frontend/          # Streamlit chat dashboard (the UI)
└── backend/           # Flask API + detection/decision/response pipeline


See [`frontend/README.md`](frontend/README.md) and
[`backend/README.md`](backend/README.md) for details on each part.
 
  How a request flows through the system


User types a message in the dashboard (frontend)
        │
        ▼
Flask /chat endpoint (backend/llm_integration/llm_server.py)
        │
        ▼
1. INPUT LAYER      → reads pfirewall.log line by line
2. DETECTION ENGINE → each line checked against 6 attack detectors
3. DECISION ENGINE  → matches converted into a risk score + severity
4. RESPONSE SYSTEM  → logs / alerts / blocks based on severity
5. LLM INTEGRATION  → Ollama (gemma) explains the findings in plain English
        │
        ▼
JSON reply + detections sent back to the dashboard


 Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- The `gemma` model pulled:
  
  ollama pull gemma
  

 Setup

From the project root:
pip install -r requirements.txt

 Running the project

You need **two terminals** running at the same time.

**Terminal 1 — backend (Flask + detection pipeline):**
cd backend
python -m llm_integration.llm_server

**Terminal 2 — frontend (Streamlit dashboard):**
cd frontend
python -m streamlit run app.py

Then open the dashboard in your browser (Streamlit will show the local URL,
typically `http://localhost:8501`) and type:

Analyze firewall logs

## Project structure


cyber_ai_agent/
├── .gitignore
├── requirements.txt
├── README.md
├── frontend/
│   ├── README.md
│   └── app.py
└── backend/
    ├── README.md
    ├── main.py
    ├── pfirewall.log
    ├── security_log.txt
    ├── dashboard/
    ├── input_layer/
    │   ├── firewall_parser.py
    │   ├── email_scanner.py
    │   ├── ip_tracker.py
    │   └── login_monitor.py
    ├── detection_engine/
    │   ├── pipeline.py
    │   ├── brute_force.py
    │   ├── phishing_detection.py
    │   ├── ip_abuse.py
    │   ├── unauthorized_access.py
    │   ├── spam_detection.py
    │   └── anomaly_detection.py
    ├── decision_engine/
    │   └── risk_scoring.py
    ├── response_system/
    │   ├── responder.py
    │   ├── block_ip.py
    │   ├── quarantine.py
    │   ├── send_alerts.py
    │   └── log_event.py
    └── llm_integration/
        ├── llm_server.py
        └── ollama_client.py


 

 
