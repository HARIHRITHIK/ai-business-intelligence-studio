# 📊 AI Business Intelligence Studio

> **An automated AI Analyst platform that ingests raw tabular business data and surfaces executive-level statistical insights, machine learning driver analysis, and publication-ready PDF reports in seconds.**

<p align="center">
  <a href="https://ai-business-intelligence-studio.onrender.com" target="_blank">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-ai--business--intelligence--studio.onrender.com-4f8ef7?style=for-the-badge" alt="Live Demo" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/HARIHRITHIK/ai-business-intelligence-studio/actions/workflows/ci.yml"><img src="https://github.com/HARIHRITHIK/ai-business-intelligence-studio/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline" /></a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18.2-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Vite-5.4-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square" alt="License" />
</p>

---

## 🎯 Target Roles & Competencies

- **Primary**: **Data Scientist**, **ML Engineer**, **Python Developer**
- **Secondary**: **AI Engineer**, **Software Engineer**, **Backend Developer**

---

## 💡 Why This Project?

Traditional BI platforms are passive dashboards displaying charts that non-technical stakeholders struggle to interpret. **AI Business Intelligence Studio** was engineered as an active **AI Analyst**:

1. Ingests structured business datasets (CSV or Excel).
2. Computes an automated **Data Quality Score (0–100)** and profiles every column.
3. Discovers statistical anomalies, trends, and correlations across all dimensions.
4. Immediately prioritizes and surfaces the **Top 3 Findings** in plain English.
5. Trains an **AutoML Lite** predictive model to identify key metric drivers.
6. Generates a standalone **visual PDF report** rendered entirely in pure Python.

---

## 🚀 Instant 1-Click Demo Experience

Recruiters and evaluators can explore the platform immediately without uploading their own data:

- 🛍️ **Retail Sales** (~800 records): Regional performance, product category margins, holiday seasonal spikes, and revenue trends.
- 👥 **HR Analytics** (~400 records): Departmental turnover, salary disparities, tenure correlation, and attrition patterns.
- 📊 **Customer Churn** (~700 records): Contract type retention, support ticket correlation, and customer tenure drivers.

---

## ✨ Core Analytical Features

- **🚀 Top Findings First**: Evaluates statistical significance and surfaces the top 3 high-impact patterns immediately upon ingestion.
- **📈 Comprehensive Statistical Discovery**:
  - **Z-Score Anomaly Detection**: Identifies outliers exceeding $|z| > 3$ thresholds.
  - **Pearson Linear Correlation**: Evaluates relationships across all numerical pairs ($|r| > 0.70$).
  - **Segment Dominance Analysis**: Flags categories driving disproportionate metric concentration.
  - **Distribution Skewness & Class Imbalance**: Measures distribution moments ($|\text{skew}| > 2.0$) and binary imbalance ($\ge 70/30$).
- **🔮 Prediction Studio (AutoML Lite)**:
  - Automatically identifies task type (**Regression** vs. **Classification**).
  - Preprocesses data via median/mode imputation, `LabelEncoder`, and `StandardScaler`.
  - Evaluates cross-validated models (`Ridge`, `LogisticRegression`, `RandomForest`).
  - Returns ranked feature importances and plain-English driver attribution.
- **📄 Sub-Second Dual Export**:
  - 🌐 **Interactive HTML Report**: Responsive browser report with Plotly.js chart interactions.
  - 📄 **Standalone PDF Report**: Pure-Python Matplotlib/FPDF2 export embedding crisp chart graphics in sub-second time.

---

## 🏗️ Architecture & Data Flow

```
┌───────────────────────────────────────────────────────────────┐
│                       React + Vite SPA                        │
│  - Glassmorphic Dark Design System (#080d1a Palette)          │
│  - Interactive Column Profiler Drawer & Full Data Preview     │
│  - Plotly.js Visualizations & Active Scroll-Spy Sidebar       │
│  - AutoML Driver Studio & Instant PDF Export Trigger          │
└───────────────────────────────┬───────────────────────────────┘
                                │ REST API (JSON)
┌───────────────────────────────▼───────────────────────────────┐
│                        FastAPI Backend                        │
│  /api/upload                 /api/overview/{session_id}       │
│  /api/samples/{name}         /api/insights/{session_id}       │
│  /api/charts/{session_id}    /api/recommendations/...         │
│  /api/predict/{session_id}   /api/report/html|pdf/...         │
└───────────────────────────────┬───────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
   Data Profiler         Insight Engine          Report Generator
(Role Inference,       (Z-Scores, Pearson,     (Pure-Python Matplotlib
Quality Score, Stats)   Segment Dominance)        + FPDF2 Engine)
```

---

## ⚖️ Engineering Decisions & Trade-Offs

| Decision | Alternative Considered | Rationale |
| :--- | :--- | :--- |
| **Pure-Python PDF Engine** | Headless Chrome (Kaleido / Puppeteer / WeasyPrint) | Headless browsers consume ~400MB per render and frequently crash in container environments. A custom Matplotlib Agg backend streams PNG buffers directly into FPDF2 with zero external C-dependencies in sub-second time. |
| **Interpretable AutoML Lite** | Deep Neural Networks / AutoGluon | Tabular business datasets (100–10,000 rows) require fast, interpretable drivers rather than black-box models. Constrained ensemble trees (`max_depth=6`) prevent overfitting and deliver instant results. |
| **Ephemeral In-Memory Cache** | PostgreSQL / MongoDB | For rapid ad-hoc dataset analysis without authentication barriers, in-memory sessions with background 2-hour TTL cleanup provide high speed with zero database overhead. |

---

## 📂 Repository Structure

```
ai-business-intelligence-studio/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions automated test & build pipeline
├── backend/
│   ├── api/
│   │   └── routes.py           # FastAPI REST endpoints & session store
│   ├── core/
│   │   ├── profiler.py         # Column role inference & quality scoring
│   │   ├── insight_engine.py   # Statistical discovery algorithms
│   │   ├── nlg.py              # Natural Language Generation engine
│   │   ├── chart_builder.py    # Plotly interactive chart specifications
│   │   ├── predictor.py        # AutoML pipeline & feature importance
│   │   └── reporter.py         # Pure-Python PDF & HTML report generator
│   ├── data/samples/           # Retail Sales, HR Analytics, Churn CSVs
│   ├── tests/
│   │   ├── test_api.py         # End-to-end API integration tests
│   │   └── test_core.py        # Profiler, insight, and predictor unit tests
│   ├── main.py                 # FastAPI application & SPA static server
│   ├── requirements.txt        # Pinned Python dependencies
│   └── Procfile                # Render deployment configuration
├── frontend/
│   ├── src/
│   │   ├── components/         # TopFindings, DataOverview, PredictionStudio...
│   │   ├── hooks/useAnalysis.js # Reactive API state orchestrator
│   │   └── styles/             # Design tokens & glassmorphism system
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Vite build & proxy configuration
├── INTERVIEW_PREP.md           # Comprehensive technical interview guide
├── LICENSE                     # MIT Open Source License
└── README.md
```

---

## ⚡ Quickstart & Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend development)

### 1. Clone & Navigate
```bash
git clone https://github.com/HARIHRITHIK/ai-business-intelligence-studio.git
cd ai-business-intelligence-studio
```

### 2. Run Backend & Automated Tests
```bash
cd backend
pip install -r requirements.txt
pytest tests -v
```

### 3. Launch Application
```bash
python -m uvicorn main:app --reload --port 8050
```

Open **`http://localhost:8050`** in your browser.

---

## 📖 API Documentation

FastAPI automatically generates interactive Swagger documentation available at:
- **Swagger UI**: `http://localhost:8050/docs`
- **ReDoc**: `http://localhost:8050/redoc`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/health` | `GET` | Service status, API version, and active session count |
| `/api/samples/{name}` | `POST` | Ingests preloaded sample (`retail_sales`, `hr_analytics`, `customer_churn`) |
| `/api/upload` | `POST` | Uploads multipart CSV or Excel dataset (max 50MB) |
| `/api/overview/{session_id}` | `GET` | Returns dataset shape, memory footprint, completeness, and column profiles |
| `/api/insights/{session_id}` | `GET` | Returns ranked statistical findings with NLG explanations |
| `/api/charts/{session_id}` | `GET` | Returns Plotly figure JSON configurations for visual evidence |
| `/api/recommendations/{session_id}` | `GET` | Returns prioritized executive business recommendations |
| `/api/predict/{session_id}` | `POST` | Executes AutoML feature importance model on selected target |
| `/api/report/html/{session_id}` | `GET` | Renders interactive full-page HTML report |
| `/api/report/pdf/{session_id}` | `GET` | Generates downloadable visual PDF report |

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
