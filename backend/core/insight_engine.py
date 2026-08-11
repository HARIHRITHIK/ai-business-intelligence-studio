import pandas as pd
import numpy as np
import uuid
from core.nlg import NLGEngine

class InsightEngine:
    def __init__(self):
        self.nlg = NLGEngine()

    def generate(self, df: pd.DataFrame, profile: dict) -> list:
        insights = []
        roles = profile.get('column_types', {})
        
        numerical_cols = [c for c, r in roles.items() if r == 'numerical']
        categorical_cols = [c for c, r in roles.items() if r == 'categorical']
        datetime_cols = [c for c, r in roles.items() if r == 'datetime']
        
        # Helper to boost score for key business words
        def get_relevance(col):
            col_lower = col.lower()
            key_words = ['revenue', 'sales', 'profit', 'margin', 'churn', 'attrition', 'cost', 'customer']
            if any(w in col_lower for w in key_words):
                return 0.9
            return 0.5
            
        # 1 & 7. Trend & Decline warning
        if datetime_cols and numerical_cols:
            date_col = datetime_cols[0]
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col])
            
            if not df_temp.empty:
                df_temp.set_index(date_col, inplace=True)
                for num_col in numerical_cols:
                    try:
                        resampled = df_temp[num_col].resample('ME').sum()
                        if len(resampled) >= 2:
                            last = resampled.iloc[-1]
                            prev = resampled.iloc[-2]
                            if prev > 0:
                                pct_change = ((last - prev) / prev) * 100
                                mag = min(abs(pct_change) / 100, 1.0)
                                score = (0.7 + 0.3 * get_relevance(num_col)) * mag
                                if pct_change > 5:
                                    insight = {
                                        "id": str(uuid.uuid4()),
                                        "icon": "📈",
                                        "type": "trend_up",
                                        "col": num_col,
                                        "pct": abs(pct_change),
                                        "category": "Trend",
                                        "severity": "positive",
                                        "score": score
                                    }
                                    insights.append(insight)
                                elif pct_change < -5:
                                    insight = {
                                        "id": str(uuid.uuid4()),
                                        "icon": "📉",
                                        "type": "trend_down",
                                        "col": num_col,
                                        "pct": abs(pct_change),
                                        "category": "Trend",
                                        "severity": "warning",
                                        "score": score + 0.2 # boost warnings
                                    }
                                    insights.append(insight)
                    except Exception:
                        pass
                        
        # 2. Anomaly
        for num_col in numerical_cols:
            series = df[num_col].dropna()
            if len(series) > 10:
                z_scores = np.abs((series - series.mean()) / series.std())
                outliers = z_scores > 3
                outlier_count = outliers.sum()
                if outlier_count > 0:
                    score = min(outlier_count / len(series) * 5, 1.0) * get_relevance(num_col)
                    insights.append({
                        "id": str(uuid.uuid4()),
                        "icon": "🔍",
                        "type": "anomaly",
                        "col": num_col,
                        "count": int(outlier_count),
                        "category": "Data Quality",
                        "severity": "info",
                        "score": score
                    })
                    
        # 3. Segment Dominance
        for cat_col in categorical_cols:
            for num_col in numerical_cols:
                try:
                    grouped = df.groupby(cat_col)[num_col].sum()
                    total = grouped.sum()
                    if total > 0:
                        top_cat = grouped.idxmax()
                        top_val = grouped.max()
                        val_pct = (top_val / total) * 100
                        
                        counts = df[cat_col].value_counts()
                        total_records = len(df)
                        record_pct = (counts[top_cat] / total_records) * 100
                        
                        if val_pct > 40 and val_pct > record_pct * 1.5:
                            insights.append({
                                "id": str(uuid.uuid4()),
                                "icon": "👥",
                                "type": "segment_dominance",
                                "category_col": cat_col,
                                "category": str(top_cat),
                                "metric": num_col,
                                "metric_pct": float(val_pct),
                                "record_pct": float(record_pct),
                                "category_name": "Segment",
                                "severity": "positive",
                                "score": 0.8 * get_relevance(num_col)
                            })
                except Exception:
                    pass

        # 4. Correlation
        if len(numerical_cols) >= 2:
            try:
                corr_matrix = df[numerical_cols].corr()
                for i in range(len(numerical_cols)):
                    for j in range(i+1, len(numerical_cols)):
                        c1 = numerical_cols[i]
                        c2 = numerical_cols[j]
                        val = corr_matrix.loc[c1, c2]
                        if abs(val) > 0.7:
                            insights.append({
                                "id": str(uuid.uuid4()),
                                "icon": "🔗",
                                "type": "correlation",
                                "col1": c1,
                                "col2": c2,
                                "strength": float(abs(val)),
                                "category": "Relationship",
                                "severity": "info",
                                "score": float(abs(val)) * max(get_relevance(c1), get_relevance(c2))
                            })
            except Exception:
                pass

        # 5. Missing data
        for col in df.columns:
            missing = df[col].isnull().sum()
            missing_pct = (missing / len(df)) * 100
            if missing_pct > 10:
                insights.append({
                    "id": str(uuid.uuid4()),
                    "icon": "⚠️",
                    "type": "missing",
                    "col": col,
                    "pct": float(missing_pct),
                    "category": "Data Quality",
                    "severity": "warning",
                    "score": 0.6
                })
                
        # 8. Imbalance detection (binary/low-cardinality targets)
        binary_cols = [c for c in categorical_cols
                       if df[c].nunique() == 2 and c.lower() not in ['gender', 'sex']]
        for col in binary_cols:
            counts = df[col].value_counts(normalize=True) * 100
            dominant_pct = float(counts.iloc[0])
            if dominant_pct >= 70:
                insights.append({
                    "id": str(uuid.uuid4()),
                    "icon": "⚠️",
                    "type": "imbalance",
                    "col": col,
                    "dominant_pct": dominant_pct,
                    "dominant_val": str(counts.index[0]),
                    "category": "Distribution",
                    "severity": "warning" if dominant_pct >= 80 else "info",
                    "score": 0.55 * get_relevance(col)
                })

        for num_col in numerical_cols:
            series = df[num_col].dropna()
            if len(series) > 10:
                skewness = series.skew()
                if abs(skewness) > 2:
                    insights.append({
                        "id": str(uuid.uuid4()),
                        "icon": "⚠️",
                        "type": "skew",
                        "col": num_col,
                        "skew_val": float(skewness),
                        "category": "Distribution",
                        "severity": "info",
                        "score": 0.5 * get_relevance(num_col)
                    })
                    
        # Apply NLG — populate headline, explanation, business_implication
        for ins in insights:
            ins['headline'] = self.nlg.insight_to_text(ins)
            ins['explanation'] = self.nlg.insight_explanation(ins)
            ins['business_implication'] = self.nlg.insight_business_implication(ins)

        # Sort by score descending
        insights.sort(key=lambda x: x.get('score', 0), reverse=True)
        return insights

    def top3(self, insights: list) -> list:
        return insights[:3]
