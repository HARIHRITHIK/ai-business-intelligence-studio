class NLGEngine:
    def __init__(self):
        pass

    def insight_to_text(self, insight: dict) -> str:
        """Generate a short, punchy headline for an insight."""
        itype = insight.get('type')
        if itype == 'trend_up':
            col = insight['col'].replace('_', ' ')
            return f"{col} increased {insight['pct']:.1f}% in the latest period — a strong positive signal."
        elif itype == 'trend_down':
            col = insight['col'].replace('_', ' ')
            return f"{col} declined {insight['pct']:.1f}% in the latest period — this warrants immediate attention."
        elif itype == 'segment_dominance':
            cat = insight['category']
            metric = insight['metric'].replace('_', ' ')
            return (f"'{cat}' accounts for {insight['metric_pct']:.0f}% of {metric} "
                    f"despite representing only {insight['record_pct']:.0f}% of records.")
        elif itype == 'correlation':
            c1 = insight['col1'].replace('_', ' ')
            c2 = insight['col2'].replace('_', ' ')
            return f"{c1} and {c2} are strongly linked (relationship strength: {insight['strength']:.2f})."
        elif itype == 'anomaly':
            col = insight['col'].replace('_', ' ')
            return f"{insight['count']} records show unusually extreme {col} values — potential data anomalies detected."
        elif itype == 'skew':
            col = insight['col'].replace('_', ' ')
            direction = "right" if insight['skew_val'] > 0 else "left"
            return f"{col} has a {direction}-skewed distribution — a small number of records dominate the total."
        elif itype == 'missing':
            col = insight['col'].replace('_', ' ')
            return f"{col} is missing {insight['pct']:.1f}% of its values, which may affect analysis reliability."
        elif itype == 'top_performer':
            return f"'{insight['category']}' is the top-performing segment for {insight['metric'].replace('_', ' ')}."
        elif itype == 'imbalance':
            col = insight['col'].replace('_', ' ')
            return f"{col} is highly imbalanced — the dominant class represents {insight['dominant_pct']:.0f}% of records."
        else:
            return "An interesting pattern was detected in the data."

    def insight_explanation(self, insight: dict) -> str:
        """Generate a fuller explanation paragraph for each insight."""
        itype = insight.get('type')
        if itype == 'trend_up':
            col = insight['col'].replace('_', ' ')
            return (f"Statistical analysis of the time series shows a {insight['pct']:.1f}% increase in {col} "
                    f"from the previous period to the most recent period. This consistent upward movement "
                    f"suggests underlying growth rather than a one-off spike.")
        elif itype == 'trend_down':
            col = insight['col'].replace('_', ' ')
            return (f"{col} has decreased by {insight['pct']:.1f}% compared to the prior period. "
                    f"A sustained decline like this typically signals a structural issue rather than "
                    f"seasonal variation, and should be investigated promptly.")
        elif itype == 'segment_dominance':
            cat = insight['category']
            cat_col = insight['category_col'].replace('_', ' ')
            metric = insight['metric'].replace('_', ' ')
            return (f"When grouping by {cat_col}, the segment '{cat}' contributes {insight['metric_pct']:.0f}% "
                    f"of total {metric} while accounting for only {insight['record_pct']:.0f}% of all records. "
                    f"This concentration suggests either a highly profitable niche or a dependency risk.")
        elif itype == 'correlation':
            c1 = insight['col1'].replace('_', ' ')
            c2 = insight['col2'].replace('_', ' ')
            strength_label = "very strong" if insight['strength'] > 0.9 else "strong" if insight['strength'] > 0.7 else "moderate"
            return (f"A {strength_label} statistical relationship (r = {insight['strength']:.2f}) exists between "
                    f"{c1} and {c2}. This means changes in one metric reliably correspond to changes in the other, "
                    f"which can be leveraged for forecasting and planning.")
        elif itype == 'anomaly':
            col = insight['col'].replace('_', ' ')
            return (f"Using z-score analysis (threshold: 3 standard deviations), {insight['count']} records were "
                    f"identified as statistical outliers in {col}. These records fall far outside the normal range "
                    f"and may represent errors, fraud, or genuinely exceptional business events.")
        elif itype == 'skew':
            col = insight['col'].replace('_', ' ')
            direction = "right" if insight['skew_val'] > 0 else "left"
            return (f"{col} has a skewness of {insight['skew_val']:.1f}, indicating a {direction}-skewed distribution. "
                    f"This means the average is pulled by extreme values and the median is a more reliable "
                    f"central measure. A Pareto analysis may reveal the top contributors.")
        elif itype == 'missing':
            col = insight['col'].replace('_', ' ')
            return (f"Data completeness check found {insight['pct']:.1f}% of values missing in {col}. "
                    f"Depending on whether data is missing at random or systematically, this could introduce "
                    f"bias into downstream analysis and models.")
        elif itype == 'imbalance':
            col = insight['col'].replace('_', ' ')
            return (f"The column {col} shows a significant class imbalance, with one category appearing in "
                    f"{insight['dominant_pct']:.0f}% of records. This is important context when interpreting "
                    f"rates and percentages derived from this field.")
        else:
            return "This pattern was identified through automated statistical analysis of the dataset."

    def insight_business_implication(self, insight: dict) -> str:
        """Generate a business implication sentence."""
        itype = insight.get('type')
        if itype == 'trend_up':
            col = insight['col'].replace('_', ' ')
            return f"Consider scaling the strategies driving {col} growth while monitoring for sustainability."
        elif itype == 'trend_down':
            col = insight['col'].replace('_', ' ')
            return f"Urgently review the factors behind the {col} decline to prevent further deterioration."
        elif itype == 'segment_dominance':
            cat = insight['category']
            return f"Evaluate whether over-reliance on '{cat}' presents a concentration risk to the business."
        elif itype == 'correlation':
            c1 = insight['col1'].replace('_', ' ')
            c2 = insight['col2'].replace('_', ' ')
            return f"This relationship can be used to forecast {c2} based on changes in {c1}."
        elif itype == 'anomaly':
            return "Flag these records for manual review to determine whether they are errors or valid exceptions."
        elif itype == 'skew':
            col = insight['col'].replace('_', ' ')
            return f"Apply a Pareto (80/20) lens to {col} — the top contributors likely drive disproportionate value."
        elif itype == 'missing':
            col = insight['col'].replace('_', ' ')
            return f"Investigate data collection processes for {col} to improve completeness going forward."
        elif itype == 'imbalance':
            return "Use caution when reporting percentages for this field — consider absolute numbers alongside rates."
        else:
            return "Review this pattern with domain experts to determine if action is required."

    def recommendation_from_insights(self, insights: list, profile: dict) -> list:
        """Generate 3-5 actionable business recommendations from top insights."""
        recs = []
        rank = 1

        for ins in insights[:5]:
            itype = ins.get('type')

            action = "Investigate this data pattern"
            rationale = self.insight_to_text(ins)
            impact = "Medium"
            category = "Operations"

            if itype == 'trend_down':
                col = ins.get('col', 'the key metric').replace('_', ' ')
                action = f"Investigate and address the decline in {col}"
                impact = "High"
                category = "Performance"
            elif itype == 'trend_up':
                col = ins.get('col', 'the key metric').replace('_', ' ')
                action = f"Scale and sustain the growth momentum in {col}"
                impact = "Medium"
                category = "Opportunity"
            elif itype == 'segment_dominance':
                cat = ins.get('category', 'the top segment')
                metric = ins.get('metric', 'the key metric').replace('_', ' ')
                action = f"Develop a focused strategy around '{cat}' — your highest-value segment for {metric}"
                impact = "High"
                category = "Strategy"
            elif itype == 'correlation':
                c1 = ins.get('col1', '').replace('_', ' ')
                c2 = ins.get('col2', '').replace('_', ' ')
                action = f"Build a forecasting model using {c1} to predict {c2}"
                impact = "Medium"
                category = "Analytics"
            elif itype == 'anomaly':
                col = ins.get('col', 'the affected column').replace('_', ' ')
                action = f"Audit the {ins.get('count', 'anomalous')} anomalous {col} records for data quality or fraud signals"
                impact = "Medium"
                category = "Data Quality"
            elif itype == 'missing':
                col = ins.get('col', '').replace('_', ' ')
                action = f"Resolve data gaps in {col} to improve analytical confidence"
                impact = "Low"
                category = "Data Quality"
            elif itype == 'imbalance':
                col = ins.get('col', '').replace('_', ' ')
                action = f"Review {col} distribution — the class imbalance may skew reporting"
                impact = "Medium"
                category = "Data Quality"
            elif itype == 'skew':
                col = ins.get('col', '').replace('_', ' ')
                action = f"Apply Pareto analysis to {col} to identify the top 20% driving 80% of the value"
                impact = "Medium"
                category = "Strategy"

            recs.append({
                "rank": rank,
                "action": action,
                "rationale": rationale,
                "impact": impact,
                "category": category
            })
            rank += 1

        return recs
