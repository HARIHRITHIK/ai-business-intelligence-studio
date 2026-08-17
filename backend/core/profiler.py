import pandas as pd
import numpy as np

class DataProfiler:
    def __init__(self):
        pass

    def detect_column_roles(self, df: pd.DataFrame) -> dict:
        roles = {}
        for col in df.columns:
            if df[col].dtype == 'object' or isinstance(df[col].dtype, pd.CategoricalDtype):
                # Check for datetime first
                try:
                    pd.to_datetime(df[col], errors='raise', format='mixed')
                    roles[col] = 'datetime'
                    continue
                except Exception:
                    pass
                
                # Check if id
                if df[col].nunique() == len(df) and df[col].nunique() > 0:
                    roles[col] = 'id'
                elif df[col].nunique() < 20 or df[col].nunique() / len(df) < 0.1:
                    roles[col] = 'categorical'
                else:
                    roles[col] = 'text'
            elif pd.api.types.is_numeric_dtype(df[col]):
                if df[col].nunique() == len(df) and len(df) > 100 and pd.api.types.is_integer_dtype(df[col]):
                    roles[col] = 'id'
                else:
                    roles[col] = 'numerical'
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                roles[col] = 'datetime'
            else:
                roles[col] = 'unknown'
        return roles

    def quality_score(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        # 1. Completeness: % of non-missing values
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = 100 * (1 - missing_cells / total_cells) if total_cells > 0 else 100
        
        # 2. Uniqueness: % of unique rows
        duplicate_rows = df.duplicated().sum()
        uniqueness = 100 * (1 - duplicate_rows / df.shape[0]) if df.shape[0] > 0 else 100
        
        # 3. Consistency: penalize mixed types
        inconsistent_cols = 0
        for col in df.columns:
            if df[col].apply(type).nunique() > 1:
                inconsistent_cols += 1
        consistency = 100 * (1 - inconsistent_cols / df.shape[1]) if df.shape[1] > 0 else 100
        
        # Weight them: 50% completeness, 30% uniqueness, 20% consistency
        score = (completeness * 0.5) + (uniqueness * 0.3) + (consistency * 0.2)
        return int(max(0, min(100, score)))

    def column_profile(self, df: pd.DataFrame, col: str, role: str) -> dict:
        profile = {}
        series = df[col].dropna()
        if series.empty:
            return {"empty": True}
        
        if role == 'numerical':
            profile = {
                'min': float(series.min()) if not pd.isna(series.min()) else None,
                'max': float(series.max()) if not pd.isna(series.max()) else None,
                'mean': float(series.mean()) if not pd.isna(series.mean()) else None,
                'median': float(series.median()) if not pd.isna(series.median()) else None,
                'std': float(series.std()) if not pd.isna(series.std()) else None,
                'skew': float(series.skew()) if not pd.isna(series.skew()) else None,
                'q1': float(series.quantile(0.25)) if not pd.isna(series.quantile(0.25)) else None,
                'q3': float(series.quantile(0.75)) if not pd.isna(series.quantile(0.75)) else None,
            }
        elif role == 'categorical':
            val_counts = series.value_counts()
            profile = {
                'top_values': val_counts.head(5).to_dict(),
                'n_unique': int(series.nunique())
            }
        elif role == 'datetime':
            try:
                datetime_series = pd.to_datetime(series)
                min_date = datetime_series.min()
                max_date = datetime_series.max()
                profile = {
                    'min_date': min_date.isoformat() if not pd.isna(min_date) else None,
                    'max_date': max_date.isoformat() if not pd.isna(max_date) else None,
                    'date_range_days': int((max_date - min_date).days) if not pd.isna(max_date) and not pd.isna(min_date) else None
                }
            except Exception:
                profile = {"error": "Could not parse datetime"}
        else:
            profile = {'n_unique': int(series.nunique())}
            
        return profile

    def profile(self, df: pd.DataFrame) -> dict:
        roles = self.detect_column_roles(df)
        
        missing_summary = []
        for col in df.columns:
            missing_count = int(df[col].isnull().sum())
            if missing_count > 0:
                missing_summary.append({
                    "column": col,
                    "missing_pct": round(missing_count / len(df) * 100, 2),
                    "missing_count": missing_count
                })
        
        column_profiles = {}
        for col in df.columns:
            column_profiles[col] = self.column_profile(df, col, roles[col])
            
        # Handle nan in preview
        preview_df = df.head(10).replace({np.nan: None})
            
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
            "quality_score": self.quality_score(df),
            "column_types": roles,
            "missing_summary": missing_summary,
            "column_profiles": column_profiles,
            "preview": preview_df.to_dict(orient='records')
        }
