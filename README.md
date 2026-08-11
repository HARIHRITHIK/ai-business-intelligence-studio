# 📊 AI Business Intelligence Studio

> **Transform raw business data into actionable executive intelligence through automated statistical analysis, natural language generation, and machine learning.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-green.style=flat-square)](LICENSE)

---

## 💡 Overview

**AI Business Intelligence Studio** is a production-grade full-stack web application designed as an **AI Analyst** rather than a static dashboard grid. 

Instead of forcing stakeholders to interpret raw charts, the application ingests structured business datasets (CSV/Excel), executes automated statistical analysis, and immediately surfaces the **Top 3 Findings** alongside plain-English business implications, interactive visual evidence, strategic recommendations, and downloadable PDF reports.

---

## ✨ Key Features

- **🚀 Top Findings First**: Surfacing the 3 most statistically significant patterns immediately upon dataset upload.
- **📈 Automated Statistical Engine**:
  - **Time Series Trend Analysis**: Detects MoM/QoQ/YoY growth trajectories.
  - **Z-Score Anomaly Detection**: Flags outliers exceeding $|z| > 3$ thresholds.
  - **Segment Dominance Analysis**: Identifies disproportionate metric contributions across categories.
  - **Pearson Correlation Matrix**: Calculates linear relationships ($|r| > 0.7$) across numerical fields.
  - **Class Imbalance & Skewness Profiling**: Detects skewed distributions ($|skew| > 2$) and binary class imbalances.
- **🔮 Prediction Studio (AutoML Lite)**: On-demand target forecasting using scaled features (`StandardScaler`), model cross-validation ($R^2$ / Accuracy scoring), and feature importance driver extraction.
- **📄 Instant Dual Export Options**:
  - 🌐 **Interactive HTML Report**: In-browser responsive report with Plotly.js chart interactions.
  - 📄 **Standalone PDF Report**: Sub-second pure-Python PDF rendering (`fpdf2` + `matplotlib`) with embedded chart figures.
- **🛍️ Built-in Sample Datasets**: Includes pre-configured datasets for Retail Sales, HR Analytics, and Customer Churn.

---

## 🏗️ Technical Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   React + Vite SPA                       │
│  - Glassmorphic UI & Animated background design system   │
│  - Top Findings & Categorized Insight Cards              │
│  - Plotly.js Interactive Evidence Visualizations         │
│  - Prediction Studio & Executive Recommendation Engine   │
└────────────────────────────┬─────────────────────────────┘
                             │ REST API (JSON)
┌────────────────────────────▼─────────────────────────────┐
│                    FastAPI Backend                       │
│  /api/upload               /api/overview/{session_id}   │
│  /api/samples/{name}       /api/insights/{session_id}   │
│  /api/charts/{session_id}  /api/recommendations/...     │
│  /api/predict/{session_id} /api/report/html|pdf/...     │
└────────────────────────────┬─────────────────────────────┘
                             │
     ┌───────────────────────┼───────────────────────┐
     ▼                       ▼                       ▼
Data Profiler             Insight Engine           Report Generator
(Pandas / Scipy)       (NLG & Math Profiler)     (fpdf2 / Matplotlib)
```

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, Vite, Axios, Plotly.js, React-Dropzone, CSS Custom Properties |
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pandas, Scikit-Learn, SciPy, Jinja2 |
| **Export Engine** | `fpdf2` (PDF Document Layout), `matplotlib` (Pure-Python Chart Rendering) |
| **Styling** | Custom Glassmorphic Dark Design System (`#080d1a` Palette, Inter & Fira Code) |

---

## 📂 Project Structure

```
Business Intelligence Studio/
├── backend/
│   ├── api/
│   │   └── routes.py           # FastAPI REST API endpoints
│   ├── core/
│   │   ├── profiler.py         # Data quality scoring & role detection
│   │   ├── insight_engine.py   # Statistical pattern discovery algorithms
│   │   ├── nlg.py              # Natural Language Generation engine
│   │   ├── chart_builder.py    # Plotly visualization builder
│   │   ├── predictor.py        # AutoML pipeline & feature importance
│   │   └── reporter.py         # HTML & pure-Python PDF report generators
│   ├── data/
│   │   └── samples/            # Retail Sales, HR Analytics, Churn CSVs
│   ├── main.py                 # App entry point & static file server
│   ├── requirements.txt        # Python dependencies
│   └── Procfile                # Deployment configuration
├── frontend/
│   ├── src/
│   │   ├── components/         # TopFindings, EvidenceChart, PredictionStudio...
│   │   ├── hooks/              # useAnalysis state orchestrator
│   │   ├── styles/             # Design tokens, glassmorphism, keyframe animations
│   │   └── utils/              # Axios API client
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite build config
└── README.md
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend development)

### Running the Application

FastAPI serves both the REST API and the compiled React production frontend at a single URL.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/business-intelligence-studio.git
   cd business-intelligence-studio
   ```

2. **Set up the Python Environment**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the Application Server**:
   ```bash
   python -m uvicorn main:app --reload --port 8050
   ```

4. **Access in Browser**:
   Open **`http://localhost:8050`**

---

## ☁️ Free Cloud Deployment (Render.com)

This project is optimized for 100% free deployment on **Render**:

1. Push your repository to GitHub.
2. Log into [Render.com](https://render.com) and click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. Configure the Web Service settings:
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
5. Click **Create Web Service**. Your application will be live on Render's free URL!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
