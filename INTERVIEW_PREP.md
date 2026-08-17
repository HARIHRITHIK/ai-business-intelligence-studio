# 🎯 Technical Interview Defense & Architectural Reference

> **AI Business Intelligence Studio** — Portfolio Architecture & Interview Guide.

---

## 1. Executive Summary (The 30-Second Pitch)

> *"Most traditional business intelligence platforms are passive dashboards displaying charts that non-technical business stakeholders struggle to interpret. I engineered the **AI Business Intelligence Studio** as an active 'AI Analyst' platform. It ingests tabular datasets (CSV/Excel), executes automated statistical profiling (Z-score anomaly detection, Pearson correlation matrix, segment dominance), trains an automated lightweight machine learning driver model, and immediately surfaces the **Top 3 Findings** in plain English alongside high-resolution visual evidence and instant downloadable PDF reports."*

---

## 2. Target Role Alignment

- **Primary**: **Data Scientist**, **ML Engineer**, **Python Developer**
- **Secondary**: **AI Engineer**, **Software Engineer**, **Backend Developer**

---

## 3. Core Architectural Components

### A. Data Profiling & Health Scoring (`core/profiler.py`)
- **Column Role Detection**: Distinguishes `numerical`, `categorical`, `datetime`, `id`, and `text` columns using cardinality heuristics and datetime parsing with fallback handling.
- **Data Quality Score (0–100)**: Formulated as a weighted composite metric:
  $$\text{Quality Score} = 0.50 \times \text{Completeness} + 0.30 \times \text{Uniqueness} + 0.20 \times \text{Consistency}$$
  - **Completeness**: Percentage of non-null cells across the matrix.
  - **Uniqueness**: Ratio of non-duplicate records.
  - **Consistency**: Column type homogeneity across records.

### B. Statistical Discovery Engine (`core/insight_engine.py`)
Executes real mathematical tests across all dimensions:
1. **Time-Series Momentum**: Computes Period-over-Period growth rates ($\Delta \% > 5\%$ or $< -5\%$) across datetime groupings.
2. **Outlier & Anomaly Detection**: Flags data points exceeding $|z| > 3$ standard deviations from the column mean:
   $$z = \frac{x - \mu}{\sigma}$$
3. **Segment Dominance**: Flags categories contributing $>40\%$ of a metric volume while representing a significantly smaller percentage of records (concentration risk).
4. **Pearson Linear Correlation**: Evaluates correlation coefficients across all numerical pairs ($|r| > 0.70$):
   $$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
5. **Distribution Skewness**: Calculates third standardized moment ($|\text{skew}| > 2.0$) to detect long-tail distributions.
6. **Class Imbalance**: Detects binary targets with $\ge 70/30$ dominance.

### C. Natural Language Generation (NLG) (`core/nlg.py`)
- Translates raw statistical findings into structured executive narratives:
  - **Headline**: High-impact, jargon-free summary statement.
  - **Data Explanation**: Contextual details explaining the underlying statistical metric.
  - **Strategic Takeaway**: Actionable recommendation (*"What should leadership do about this?"*).

### D. AutoML Lite Predictor (`core/predictor.py`)
- **Task Auto-Detection**: Infers `Classification` vs `Regression` based on target cardinality ($\le 10$ unique values or categorical dtype) vs continuous floats.
- **Preprocessing Pipeline**:
  - Drops identifier/free-text columns.
  - Imputes missing values via median (numerical) and mode (categorical).
  - Encodes categorical predictors via `LabelEncoder`.
  - Normalizes numerical predictors using `StandardScaler` ($\mu = 0, \sigma = 1$).
- **Model Evaluation**: Compares baseline models (`Ridge` / `LogisticRegression`) against tree ensembles (`RandomForest`, restricted to `max_depth=6` to prevent overfitting on small datasets).
- **Feature Importance Attribution**: Extracts Gini impurity reduction or normalized coefficient magnitudes to rank top business drivers.

### E. High-Speed Export Engine (`core/reporter.py`)
- **Why pure-Python?** Headless Chromium (Kaleido / Puppeteer / WeasyPrint) requires heavy C-system libraries, uses ~400MB memory per render, and frequently hangs on Windows/Linux containers.
- **The Solution**: Renders Plotly JSON figure specifications directly into in-memory PNG buffers via `matplotlib` (Agg backend), embedding crisp chart images into an `FPDF2` document in **sub-second time**.

---

## 4. Top 10 Technical Interview Questions & Model Answers

### Q1: Why build an "AI Analyst" instead of an interactive dashboard?
> **Answer**: *"Dashboards answer questions you already know to ask, but require business users to visually inspect charts and interpret data themselves. An AI Analyst proactively answers 'What changed?' and 'Why does it matter?' by running automated statistical tests across all column combinations and presenting prioritized, plain-English findings."*

### Q2: How do you prevent overfitting in the AutoML Prediction Studio?
> **Answer**: *"On business datasets of modest size (100–10,000 rows), deep decision trees easily memorize noise. I constrained the tree ensembles to `max_depth=6` and `n_estimators=25`, applied feature scaling via `StandardScaler`, and used cross-validation scoring ($R^2$ for regression, Accuracy for classification) to choose the best generalizable model."*

### Q3: How do you rank competing statistical insights to surface the Top 3?
> **Answer**: *"The insight engine computes a composite score weighting statistical effect size (e.g. correlation magnitude $|r|$, outlier count ratio, or growth rate), business relevance domain weighting (boosting metrics like Revenue, Margin, Churn, or Salary), and actionability. The top 3 highest composite scores are surfaced first."*

### Q4: How is session state managed, and how would you scale it horizontally?
> **Answer**: *"For fast, lightweight exploration without requiring user registration, sessions are held in an in-memory dictionary paired with an asynchronous 2-hour TTL background cleanup task. In a horizontally scaled production environment across multiple container replicas, I would replace the in-memory dictionary with a distributed Redis cluster or persist uploaded artifacts to an S3 bucket with signed URLs."*

### Q5: How did you implement high-performance PDF export without headless browsers?
> **Answer**: *"Standard web-to-PDF tools like WeasyPrint or Kaleido rely on headless browser subprocesses that have high memory footprints and platform-specific binary dependencies. I implemented a pure-Python rendering bridge using Matplotlib's headless Agg backend to parse Plotly figure JSON and stream PNG byte buffers directly into FPDF2. This dropped export latency to sub-second speeds and eliminated all external C-runtime dependencies."*

### Q6: How does the application handle missing data or dirty datasets?
> **Answer**: *"The `DataProfiler` performs automated data hygiene checks. For profiling, it computes missing percentages and filters nulls per analysis. In the AutoML pipeline, numerical features are imputed using column medians (robust to outliers) and categoricals using mode. Furthermore, columns with >10% missing values automatically trigger a Data Quality Warning insight."*

### Q7: Why FastAPI instead of Flask or Django?
> **Answer**: *"FastAPI provides asynchronous concurrency (ASGI), native Pydantic data validation with strict type hints, automatic interactive OpenAPI/Swagger documentation (`/docs`), and high request throughput, making it ideal for high-speed analytical APIs."*

### Q8: How did you package the frontend and backend for deployment?
> **Answer**: *"The React application is compiled into static assets (`dist/`) via Vite and served directly through FastAPI's static file mount with a fallback SPA router. This packages the entire application into a single containerized deployment, reducing hosting costs to zero and eliminating cross-origin CORS latency in production."*

### Q9: What metrics do you use for data quality scoring?
> **Answer**: *"Quality score is a composite index (0–100) combining completeness (percentage of populated cells, weighted at 50%), uniqueness (percentage of non-duplicate records, weighted at 30%), and consistency (absence of mixed data types within individual columns, weighted at 20%)."*

### Q10: If you had another sprint on this project, what would you build next?
> **Answer**: *"I would implement automated time-series forecasting (e.g., exponential smoothing or ARIMA for multi-period projections), add CSV/Excel report data exports, and allow users to ask ad-hoc questions via a lightweight semantic natural language query interface."*
