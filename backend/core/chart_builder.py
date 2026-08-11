import pandas as pd
import plotly.graph_objects as go
import json
import uuid

class ChartBuilder:
    def __init__(self):
        self.dark_layout = dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.03)',
            font=dict(color='#94a3b8', family='Inter, sans-serif'),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', zerolinecolor='rgba(255,255,255,0.1)')
        )

    def build_charts(self, df: pd.DataFrame, profile: dict, insights: list) -> list:
        charts = []
        roles = profile.get('column_types', {})
        
        numerical_cols = [c for c, r in roles.items() if r == 'numerical']
        categorical_cols = [c for c, r in roles.items() if r == 'categorical']
        datetime_cols = [c for c, r in roles.items() if r == 'datetime']
        
        # 1. Time series
        if datetime_cols and numerical_cols:
            date_col = datetime_cols[0]
            num_col = numerical_cols[0]
            
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
            df_temp = df_temp.dropna(subset=[date_col])
            
            if not df_temp.empty:
                grouped = df_temp.groupby(pd.Grouper(key=date_col, freq='ME'))[num_col].sum().reset_index()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=grouped[date_col], y=grouped[num_col], mode='lines+markers', name=num_col, line=dict(color='#3b82f6', width=3)))
                fig.update_layout(**self.dark_layout, title=f"{num_col} Over Time")
                
                charts.append({
                    "id": f"ts_{uuid.uuid4().hex[:8]}",
                    "title": f"{num_col} Over Time",
                    "caption": f"Monthly trend showing changes in {num_col}.",
                    "figure": json.loads(fig.to_json())
                })
                
        # 2. Distribution
        for num_col in numerical_cols[:2]: # Max 2 distributions
            series = df[num_col].dropna()
            if not series.empty:
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=series, nbinsx=30, marker_color='#8b5cf6'))
                fig.update_layout(**self.dark_layout, title=f"Distribution of {num_col}", bargap=0.1)
                
                charts.append({
                    "id": f"dist_{uuid.uuid4().hex[:8]}",
                    "title": f"Distribution of {num_col}",
                    "caption": f"Spread and shape of {num_col} values.",
                    "figure": json.loads(fig.to_json())
                })
                
        # 3. Category bar
        if categorical_cols and numerical_cols:
            cat_col = categorical_cols[0]
            num_col = numerical_cols[0]
            
            grouped = df.groupby(cat_col)[num_col].sum().nlargest(10).reset_index()
            grouped = grouped.sort_values(by=num_col, ascending=True) # for horizontal bar
            
            fig = go.Figure()
            fig.add_trace(go.Bar(y=grouped[cat_col], x=grouped[num_col], orientation='h', marker_color='#10b981'))
            fig.update_layout(**self.dark_layout, title=f"Top {cat_col} by {num_col}")
            
            charts.append({
                "id": f"bar_{uuid.uuid4().hex[:8]}",
                "title": f"Top {cat_col} by {num_col}",
                "caption": f"Comparison of {cat_col} based on total {num_col}.",
                "figure": json.loads(fig.to_json())
            })
            
        # 4. Correlation heatmap
        if len(numerical_cols) >= 3:
            corr = df[numerical_cols].corr()
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu',
                zmin=-1, zmax=1
            ))
            fig.update_layout(**self.dark_layout, title="Correlation Matrix")
            
            charts.append({
                "id": f"corr_{uuid.uuid4().hex[:8]}",
                "title": "Correlation Matrix",
                "caption": "Shows how strongly different numerical metrics are related.",
                "figure": json.loads(fig.to_json())
            })
            
        # 5. Churn/Attrition Pie
        target_cols = [c for c in df.columns if c.lower() in ['churn', 'churned', 'attrition']]
        if target_cols:
            target_col = target_cols[0]
            counts = df[target_col].value_counts()
            
            fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts.values, hole=.4, 
                                        marker=dict(colors=['#f43f5e', '#2dd4bf']))])
            fig.update_layout(**self.dark_layout, title=f"{target_col} Rate")
            
            charts.append({
                "id": f"pie_{uuid.uuid4().hex[:8]}",
                "title": f"{target_col} Breakdown",
                "caption": f"Proportion of records by {target_col} status.",
                "figure": json.loads(fig.to_json())
            })

        return charts
