# 🏗️ Architecture & Technical Design

This document details the architectural design, component interactions, and data pipeline of the **AI Business Intelligence Studio**.

---

## 1. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Client Browser                                │
│                     React 18 SPA (Vite Bundled)                         │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────┐  │
│  │   Landing Hero   │  │  Data Overview   │  │  Top Findings &       │  │
│  │ (1-Click Sample) │  │  (Quality/Stats) │  │  Business Insights    │  │
│  └────────┬─────────┘  └────────┬─────────┘  └───────────┬───────────┘  │
│           │                     │                        │              │
│  ┌────────┴─────────┐  ┌────────┴─────────┐  ┌───────────┴───────────┐  │
│  │ Plotly.js Visual │  │ Prediction Studio│  │ Report Export Triggers│  │
│  │ Evidence Charts  │  │ (Driver Model)   │  │ (HTML Tab / PDF File) │  │
│  └──────────────────┘  └──────────────────┘  └───────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTP REST (JSON / Multipart)
┌────────────────────────────────────▼────────────────────────────────────┐
│                         FastAPI Web Server                              │
│                          (ASGI / Uvicorn)                               │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ REST Routing Layer (`api/routes.py`)                              │  │
│  │ • POST /api/upload         • GET  /api/overview/{session_id}     │  │
│  │ • POST /api/samples/{name} • GET  /api/insights/{session_id}     │  │
│  │ • POST /api/predict/{id}   • GET  /api/charts/{session_id}        │  │
│  │ • GET  /api/report/html    • GET  /api/report/pdf                 │  │
│  └──────────────────┬───────────────────────────────┬────────────────┘  │
│                     │                               │                   │
│  ┌──────────────────▼──────────────┐  ┌─────────────▼────────────────┐  │
│  │ Ephemeral Session Store (RAM)   │  │ Background Worker Task       │  │
│  │ In-memory dictionary per UUID   │  │ 2-Hour TTL Session Cleanup   │  │
│  └──────────────────┬──────────────┘  └──────────────────────────────┘  │
│                     │                                                   │
│                     ▼                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Core Analytical Engine (`backend/core/`)                          │  │
│  │                                                                   │  │
│  │  ┌──────────────────────┐           ┌──────────────────────────┐  │  │
│  │  │ DataProfiler         │           │ InsightEngine            │  │  │
│  │  │ • Type/Role Detect   │           │ • Z-Score Anomaly (|z|>3)│  │  │
│  │  │ • Quality Score 0-100│           │ • Pearson Matrix (|r|>0.7│  │  │
│  │  │ • Column Statistics  │           │ • Segment Dominance      │  │  │
│  │  └──────────┬───────────┘           └────────────┬─────────────┘  │  │
│  │             │                                    │                │  │
│  │  ┌──────────▼───────────┐           ┌────────────▼─────────────┐  │  │
│  │  │ AutoMLPredictor      │           │ NLGEngine                │  │  │
│  │  │ • Task Auto-Detect   │           │ • Headline Synthesis     │  │  │
│  │  │ • StandardScaler     │           │ • Explanation Paragraph  │  │  │
│  │  │ • Cross-Validation   │           │ • Strategic Takeaways    │  │  │
│  │  │ • Driver Importances │           └────────────┬─────────────┘  │  │
│  │  └──────────┬───────────┘                        │                │  │
│  │             │                                    │                │  │
│  │  ┌──────────▼───────────┐           ┌────────────▼─────────────┐  │  │
│  │  │ ChartBuilder         │           │ ReportGenerator          │  │  │
│  │  │ • Dark Layouts       │           │ • HTML Responsive Report │  │  │
│  │  │ • Plotly JSON Specs  │           │ • Pure-Python PDF Engine │  │  │
│  │  │ • Categorical / TS   │           │   (Matplotlib + FPDF2)   │  │  │
│  │  └──────────────────────┘           └──────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. End-to-End Data Lifecycle

```
[ User Action: Ingest Dataset / Select Sample ]
                       │
                       ▼
         [ 1. Data Profiling & Hygiene ]
         • Parse tabular structure with Pandas
         • Infer column data roles (numerical, categorical, datetime, id)
         • Calculate composite Data Quality Score (0–100)
                       │
                       ▼
         [ 2. Statistical Insight Discovery ]
         • Compute Z-score anomaly vectors
         • Evaluate Pearson correlation matrix across numerical pairs
         • Analyze segment concentration and distribution skewness
         • Rank and filter Top 3 primary findings
                       │
                       ▼
         [ 3. Executive NLG Narrative Synthesis ]
         • Generate plain-English headlines, statistical context, and strategic business takeaways
                       │
                       ▼
         [ 4. Interactive Visualization & Exploration ]
         • Build Plotly.js chart configurations
         • Stream structured profile and insight payloads to React SPA
                       │
                       ▼
         [ 5. On-Demand Driver Prediction (AutoML Lite) ]
         • User selects target metric
         • Feature preprocessing: imputation, LabelEncoder, StandardScaler
         • Train candidate models with cross-validation
         • Extract normalized feature importance weights
                       │
                       ▼
         [ 6. Automated Multi-Page PDF & HTML Reporting ]
         • Render Plotly specs to in-memory PNG buffers via Matplotlib Agg backend
         • Assemble styled multi-page PDF document via FPDF2 in sub-second time
```

---

## 3. Core Architectural Decisions

### Pure-Python PDF Generation vs. Headless Browsers
- **Challenge**: Traditional HTML-to-PDF generators (WeasyPrint, Kaleido, Puppeteer) rely on Chromium or WebKit subprocesses that consume ~400MB of RAM, take multiple seconds to launch, and suffer from OS-level font/binary incompatibilities in containerized cloud environments.
- **Solution**: A custom pure-Python rendering bridge converts Plotly JSON specifications directly into in-memory PNG images using Matplotlib's headless `Agg` backend and embeds them into structured `FPDF2` documents.
- **Result**: Generates publication-quality PDF reports with embedded charts in under one second on standard CPU cores with zero external C-dependencies.

### Interpretable AutoML Lite vs. Black-Box Models
- **Challenge**: Complex deep neural networks or heavy ensemble stacks are prone to overfitting on small-to-medium business datasets (100–10,000 rows) and function as uninterpretable black boxes.
- **Solution**: Evaluates regularized linear/logistic models and constrained tree ensembles (`max_depth=6`, `n_estimators=25`) using cross-validation.
- **Result**: Delivers fast, generalizable models with directly interpretable feature importance rankings.
