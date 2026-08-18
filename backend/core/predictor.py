import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import plotly.graph_objects as go
import json

class AutoMLPredictor:
    def __init__(self):
        pass

    def predict(self, df: pd.DataFrame, target_col: str) -> dict:
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found.")
            
        df_clean = df.copy()
        
        # Drop rows where target is NaN
        df_clean = df_clean.dropna(subset=[target_col])
        if df_clean.empty:
            raise ValueError("Target column contains no valid non-null values.")

        # Determine task type
        is_classification = False
        if df_clean[target_col].dtype == 'object' or df_clean[target_col].nunique() <= 10:
            is_classification = True
            
        task_type = "classification" if is_classification else "regression"
        
        # Drop dates, IDs, and high-cardinality text columns (>50% unique object strings)
        cols_to_drop = []
        for col in df_clean.columns:
            if col == target_col:
                continue
            cname = col.lower()
            if 'date' in cname or 'time' in cname or 'id' in cname:
                cols_to_drop.append(col)
                continue
            if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                cols_to_drop.append(col)
                continue
            if df_clean[col].dtype == 'object' and df_clean[col].nunique() > (len(df_clean) * 0.5):
                cols_to_drop.append(col)
                continue
                
        df_clean = df_clean.drop(columns=cols_to_drop, errors='ignore')
        
        # Target variable y
        y = df_clean[target_col]
        if is_classification and y.dtype == 'object':
            y = LabelEncoder().fit_transform(y.astype(str))
            
        X = df_clean.drop(columns=[target_col], errors='ignore')
        
        # Process feature columns
        for col in X.columns:
            if pd.api.types.is_numeric_dtype(X[col]):
                X[col] = X[col].fillna(X[col].median())
            else:
                most_freq = X[col].mode()[0] if not X[col].mode().empty else "Unknown"
                X[col] = X[col].fillna(most_freq)
                X[col] = LabelEncoder().fit_transform(X[col].astype(str))
                
        if X.empty or len(X.columns) == 0:
            raise ValueError("No valid predictor columns available after filtering.")

        # Scale features for fast linear/logistic model convergence
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
            
        # Select fast models
        if is_classification:
            models = {
                "Logistic Regression": LogisticRegression(max_iter=300),
                "Random Forest": RandomForestClassifier(n_estimators=25, max_depth=6, random_state=42)
            }
            scoring = 'accuracy'
            metric_name = 'Accuracy'
        else:
            models = {
                "Linear Regression": Ridge(),
                "Random Forest": RandomForestRegressor(n_estimators=25, max_depth=6, random_state=42)
            }
            scoring = 'r2'
            metric_name = 'R² Score'
            
        best_model_name = ""
        best_score = -float('inf')
        best_model = None
        
        cv_folds = min(3, max(2, len(X)))
        for name, model in models.items():
            try:
                scores = cross_val_score(model, X_scaled, y, cv=cv_folds, scoring=scoring)
                mean_score = scores.mean()
                if mean_score > best_score or best_model is None:
                    best_score = mean_score
                    best_model_name = name
                    best_model = model
            except Exception:
                continue
                
        if best_model is None:
            raise ValueError("Unable to evaluate predictive model: insufficient target variation or sample size.")
            
        best_model.fit(X_scaled, y)
        
        importances = []
        if hasattr(best_model, 'feature_importances_'):
            importances = best_model.feature_importances_
        elif hasattr(best_model, 'coef_'):
            coef = best_model.coef_
            importances = np.abs(coef[0] if len(coef.shape) > 1 else coef)
            
        feature_importances = []
        if len(importances) == len(X.columns):
            total_importance = float(sum(importances))
            for i, col in enumerate(X.columns):
                val = float(importances[i]) / total_importance if total_importance > 0 else 0.0
                feature_importances.append({"feature": col, "importance": float(val)})
                
        feature_importances.sort(key=lambda x: x['importance'], reverse=True)
        top_features = feature_importances[:5]
        
        # Chart
        fig = go.Figure()
        if top_features:
            features = [f['feature'] for f in reversed(top_features)]
            imps = [f['importance'] for f in reversed(top_features)]
            
            fig.add_trace(go.Bar(y=features, x=imps, orientation='h', marker_color='#3b82f6'))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(255,255,255,0.03)',
                font=dict(color='#94a3b8', family='Inter, sans-serif'),
                title="Key Drivers",
                margin=dict(l=100, r=20, t=40, b=20)
            )
            
        # Build plain English summary
        score_display = max(0.0, min(1.0, best_score)) if not (np.isinf(best_score) or np.isnan(best_score)) else 0.0
        plain_english = (
            f"We can forecast {target_col.replace('_', ' ')} with "
            f"{score_display * 100:.0f}% confidence ({metric_name}) using {best_model_name}."
        )
        if len(top_features) >= 2:
            plain_english += (
                f" The strongest predictors are {top_features[0]['feature'].replace('_', ' ')} "
                f"and {top_features[1]['feature'].replace('_', ' ')}."
            )
        elif len(top_features) == 1:
            plain_english += f" The strongest predictor is {top_features[0]['feature'].replace('_', ' ')}."

        return {
            "task_type": task_type,
            "best_model": best_model_name,
            "metric_name": metric_name,
            "metric_value": float(score_display),
            "plain_english": plain_english,
            "feature_importances": top_features,
            "feature_chart": json.loads(fig.to_json()) if top_features else None
        }
