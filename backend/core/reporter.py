from jinja2 import Environment, BaseLoader
from fpdf import FPDF
import datetime
import plotly.graph_objects as go
import json
import base64
import io
import tempfile
import os


def _tojson_filter(value):
    """Custom Jinja2 filter to safely serialize Python objects to JSON strings."""
    return json.dumps(value, default=str)


# Jinja2 Environment with custom filters
_jinja_env = Environment(loader=BaseLoader(), autoescape=False)
_jinja_env.filters['tojson'] = _tojson_filter


class ReportGenerator:
    def __init__(self):
        self.html_template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BI Studio Report — {{ session.filename }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            color: #1e293b;
            background: #f8fafc;
            line-height: 1.6;
        }
        .report-header {
            background: linear-gradient(135deg, #080d1a 0%, #0f172a 60%, #1a1040 100%);
            color: white;
            padding: 48px 40px;
        }
        .header-inner { max-width: 1000px; margin: 0 auto; }
        .header-badge {
            display: inline-block;
            background: rgba(79,142,247,0.2);
            border: 1px solid rgba(79,142,247,0.4);
            color: #7db4fa;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        .header-title { font-size: 32px; font-weight: 700; margin-bottom: 8px; }
        .header-meta { color: #94a3b8; font-size: 14px; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px 60px; }
        .section { margin-bottom: 48px; }
        .section-title {
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 6px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e2e8f0;
        }
        .section-subtitle { font-size: 14px; color: #64748b; margin-bottom: 24px; }
        .stat-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
        .stat-pill {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 24px;
            flex: 1;
            min-width: 160px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .stat-pill-label { font-size: 12px; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
        .stat-pill-value { font-size: 28px; font-weight: 700; color: #0f172a; margin-top: 4px; }
        .quality-high { color: #16a34a; }
        .quality-mid  { color: #d97706; }
        .quality-low  { color: #dc2626; }
        .findings-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .finding-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }
        .finding-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
        }
        .finding-card.positive::before { background: linear-gradient(90deg, #22c55e, #16a34a); }
        .finding-card.warning::before  { background: linear-gradient(90deg, #f59e0b, #d97706); }
        .finding-card.critical::before { background: linear-gradient(90deg, #ef4444, #dc2626); }
        .finding-card.info::before     { background: linear-gradient(90deg, #06b6d4, #0891b2); }
        .finding-icon { font-size: 28px; margin-bottom: 12px; }
        .finding-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
        }
        .badge-positive { background: #dcfce7; color: #15803d; }
        .badge-warning  { background: #fef3c7; color: #92400e; }
        .badge-critical { background: #fee2e2; color: #b91c1c; }
        .badge-info     { background: #e0f2fe; color: #0369a1; }
        .finding-headline { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 10px; line-height: 1.4; }
        .finding-explanation { font-size: 14px; color: #64748b; line-height: 1.5; }
        .insight-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            border-left: 4px solid #e2e8f0;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
        .insight-item.positive { border-left-color: #22c55e; }
        .insight-item.warning  { border-left-color: #f59e0b; }
        .insight-item.critical { border-left-color: #ef4444; }
        .insight-item.info     { border-left-color: #06b6d4; }
        .insight-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .insight-headline { font-size: 15px; font-weight: 600; color: #0f172a; flex: 1; }
        .insight-explanation { font-size: 14px; color: #475569; margin-bottom: 8px; }
        .insight-implication { font-size: 13px; color: #64748b; font-style: italic; }
        .rec-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            display: flex;
            gap: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
        .rec-rank { font-size: 36px; font-weight: 800; color: #e2e8f0; line-height: 1; min-width: 40px; }
        .rec-content { flex: 1; }
        .rec-meta { display: flex; gap: 8px; margin-bottom: 8px; }
        .rec-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
        .impact-high   { background: #fee2e2; color: #b91c1c; }
        .impact-medium { background: #fef3c7; color: #92400e; }
        .impact-low    { background: #f0fdf4; color: #15803d; }
        .cat-badge     { background: #eff6ff; color: #1d4ed8; }
        .rec-action { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 6px; }
        .rec-rationale { font-size: 14px; color: #64748b; }
        .chart-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
        .chart-title { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 4px; }
        .chart-caption { font-size: 13px; color: #94a3b8; text-align: center; margin-top: 12px; }
        .chart-container { width: 100%; height: 380px; }
        .report-footer {
            text-align: center;
            color: #94a3b8;
            font-size: 13px;
            padding: 24px;
            border-top: 1px solid #e2e8f0;
            margin-top: 40px;
        }
    </style>
</head>
<body>

<div class="report-header">
    <div class="header-inner">
        <div class="header-badge">AI Business Intelligence Studio</div>
        <h1 class="header-title">Intelligence Report</h1>
        <p class="header-meta">
            Dataset: <strong style="color:#e2e8f0">{{ session.filename }}</strong>
            &nbsp;·&nbsp; Generated: {{ date }}
            &nbsp;·&nbsp; {{ session.profile.rows | default(0) }} records
        </p>
    </div>
</div>

<div class="container">
    <div class="section">
        <h2 class="section-title">Data Overview</h2>
        <p class="section-subtitle">Summary of the uploaded dataset</p>
        <div class="stat-row">
            <div class="stat-pill">
                <div class="stat-pill-label">Records</div>
                <div class="stat-pill-value">{{ "{:,}".format(session.profile.rows | default(0)) }}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">Columns</div>
                <div class="stat-pill-value">{{ session.profile.columns | default(0) }}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">Data Quality</div>
                <div class="stat-pill-value {% if session.profile.quality_score >= 80 %}quality-high{% elif session.profile.quality_score >= 60 %}quality-mid{% else %}quality-low{% endif %}">
                    {{ session.profile.quality_score | default(0) }}/100
                </div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">File Size</div>
                <div class="stat-pill-value" style="font-size:20px">{{ "%.1f"|format(session.profile.memory_mb | default(0)) }} MB</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2 class="section-title">Top Findings</h2>
        <p class="section-subtitle">The most important patterns identified in your data</p>
        <div class="findings-grid">
            {% for insight in session.top3 %}
            <div class="finding-card {{ insight.severity | default('info') }}">
                <div class="finding-icon">{{ insight.icon | default('💡') }}</div>
                <span class="finding-badge badge-{{ insight.severity | default('info') }}">{{ insight.category | default('Insight') }}</span>
                <div class="finding-headline">{{ insight.headline }}</div>
                <div class="finding-explanation">{{ insight.explanation }}</div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="section">
        <h2 class="section-title">Business Recommendations</h2>
        <p class="section-subtitle">Actionable steps based on data patterns</p>
        {% for rec in session.recommendations %}
        <div class="rec-item">
            <div class="rec-rank">{{ rec.rank }}</div>
            <div class="rec-content">
                <div class="rec-meta">
                    <span class="rec-badge impact-{{ rec.impact | lower }}">{{ rec.impact }} Impact</span>
                    <span class="rec-badge cat-badge">{{ rec.category }}</span>
                </div>
                <div class="rec-action">{{ rec.action }}</div>
                <div class="rec-rationale">{{ rec.rationale }}</div>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="section">
        <h2 class="section-title">Key Insights</h2>
        <p class="section-subtitle">Full ranked list of statistical findings</p>
        {% for insight in session.insights[:8] %}
        <div class="insight-item {{ insight.severity | default('info') }}">
            <div class="insight-header">
                <span>{{ insight.icon | default('💡') }}</span>
                <div class="insight-headline">{{ insight.headline }}</div>
                <span class="finding-badge badge-{{ insight.severity | default('info') }}" style="margin-bottom:0">{{ insight.category }}</span>
            </div>
            <div class="insight-explanation">{{ insight.explanation }}</div>
            <div class="insight-implication">→ {{ insight.business_implication }}</div>
        </div>
        {% endfor %}
    </div>

    {% if session.charts %}
    <div class="section">
        <h2 class="section-title">Supporting Evidence</h2>
        <p class="section-subtitle">Data visualisations supporting the insights above</p>
        {% for chart in session.charts %}
        <div class="chart-card">
            <div class="chart-title">{{ chart.title }}</div>
            <div id="chart-{{ loop.index }}" class="chart-container"></div>
            <div class="chart-caption">{{ chart.caption }}</div>
        </div>
        <script>
            (function() {
                var chartData = {{ chart.figure | tojson }};
                chartData.layout = chartData.layout || {};
                chartData.layout.paper_bgcolor = '#ffffff';
                chartData.layout.plot_bgcolor  = '#f8fafc';
                if (chartData.layout.font) { chartData.layout.font.color = '#1e293b'; }
                else { chartData.layout.font = { color: '#1e293b' }; }
                if (chartData.layout.xaxis) {
                    chartData.layout.xaxis.gridcolor = '#e2e8f0';
                    chartData.layout.xaxis.zerolinecolor = '#cbd5e1';
                }
                if (chartData.layout.yaxis) {
                    chartData.layout.yaxis.gridcolor = '#e2e8f0';
                    chartData.layout.yaxis.zerolinecolor = '#cbd5e1';
                }
                Plotly.newPlot('chart-{{ loop.index }}', chartData.data, chartData.layout, {responsive: true, displaylogo: false});
            })();
        </script>
        {% endfor %}
    </div>
    {% endif %}

    {% if session.prediction %}
    <div class="section">
        <h2 class="section-title">Prediction Studio Results</h2>
        <div class="chart-card">
            <div class="stat-row">
                <div class="stat-pill">
                    <div class="stat-pill-label">{{ session.prediction.metric_name }}</div>
                    <div class="stat-pill-value quality-high">{{ "%.0f"|format((session.prediction.metric_value | default(0)) * 100) }}%</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-pill-label">Analysis Method</div>
                    <div class="stat-pill-value" style="font-size:18px">{{ session.prediction.best_model }}</div>
                </div>
            </div>
            <p style="color:#475569; font-size:15px; margin-top:8px;">{{ session.prediction.plain_english }}</p>
        </div>
    </div>
    {% endif %}
</div>

<div class="report-footer">
    Generated by <strong>BI Studio</strong> &middot; {{ date }} &middot; Confidential
</div>
</body>
</html>"""

    def generate_html(self, session_data: dict) -> str:
        template = _jinja_env.from_string(self.html_template_str)
        return template.render(
            session=session_data,
            date=datetime.datetime.now().strftime("%d %B %Y, %H:%M")
        )

    def _render_chart_to_png(self, chart: dict) -> bytes | None:
        """Render Plotly figure data to a crisp PNG image using matplotlib in pure Python."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import numpy as np

            fig_data = chart.get('figure', {}).get('data', [])
            if not fig_data:
                return None

            trace = fig_data[0]
            ttype = trace.get('type', 'scatter')

            fig, ax = plt.subplots(figsize=(6.5, 3.0), dpi=120)
            ax.set_facecolor('#f8fafc')
            fig.patch.set_facecolor('#ffffff')

            fig_title = self._clean_txt(chart.get('title', 'Chart'))
            ax.set_title(fig_title, fontsize=9, fontweight='bold', color='#0f172a', pad=8)

            if ttype == 'scatter':
                x = [self._clean_txt(str(v)) for v in trace.get('x', [])]
                y = trace.get('y', [])
                if x and y and len(x) == len(y):
                    ax.plot(range(len(y)), y, color='#3b82f6', linewidth=2, marker='o', markersize=3)
                    ax.fill_between(range(len(y)), y, color='#3b82f6', alpha=0.15)
                    step = max(1, len(x) // 8)
                    ax.set_xticks(range(0, len(x), step))
                    ax.set_xticklabels([x[i] for i in range(0, len(x), step)], rotation=25, fontsize=7)
                    ax.tick_params(axis='y', labelsize=7)
                    ax.grid(True, linestyle='--', alpha=0.3)

            elif ttype == 'histogram':
                x = trace.get('x', [])
                if x:
                    ax.hist(x, bins=15, color='#8b5cf6', edgecolor='white', alpha=0.85)
                    ax.tick_params(axis='both', labelsize=7)
                    ax.grid(True, linestyle='--', alpha=0.3)

            elif ttype == 'bar':
                x = [self._clean_txt(str(v)) for v in trace.get('x', [])]
                y = trace.get('y', [])
                orientation = trace.get('orientation', 'v')
                if orientation == 'h' and x and y:
                    y_labels = [self._clean_txt(str(v)) for v in y]
                    ax.barh(range(len(x)), x, color='#10b981', height=0.55, alpha=0.85)
                    ax.set_yticks(range(len(y_labels)))
                    ax.set_yticklabels(y_labels, fontsize=7)
                    ax.invert_yaxis()
                    ax.tick_params(axis='x', labelsize=7)
                elif x and y:
                    ax.bar(range(len(y)), y, color='#10b981', width=0.55, alpha=0.85)
                    ax.set_xticks(range(len(x)))
                    ax.set_xticklabels(x, rotation=25, fontsize=7)
                    ax.tick_params(axis='y', labelsize=7)
                ax.grid(True, linestyle='--', alpha=0.3)

            elif ttype == 'heatmap':
                z = np.array(trace.get('z', [[]]))
                x_labels = [self._clean_txt(str(v)) for v in trace.get('x', [])]
                y_labels = [self._clean_txt(str(v)) for v in trace.get('y', [])]
                if z.size > 0:
                    cax = ax.imshow(z, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
                    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
                    if x_labels and len(x_labels) == z.shape[1]:
                        ax.set_xticks(range(len(x_labels)))
                        ax.set_xticklabels(x_labels, rotation=35, fontsize=6, ha='right')
                    if y_labels and len(y_labels) == z.shape[0]:
                        ax.set_yticks(range(len(y_labels)))
                        ax.set_yticklabels(y_labels, fontsize=6)

            elif ttype == 'pie':
                labels = [self._clean_txt(str(v)) for v in trace.get('labels', [])]
                values = trace.get('values', [])
                if values:
                    colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
                    ax.pie(values, labels=labels, autopct='%1.0f%%', colors=colors[:len(values)], textprops={'fontsize': 7})

            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=120)
            plt.close(fig)
            return buf.getvalue()
        except Exception:
            return None

    def _clean_txt(self, text: str) -> str:
        if not text:
            return ""
        replacements = {
            '—': '-',
            '–': '-',
            '→': '->',
            '’': "'",
            '‘': "'",
            '“': '"',
            '”': '"',
            '•': '*',
            '…': '...',
            '·': '|',
            '📈': '',
            '📉': '',
            '⚠️': '',
            '🔍': '',
            '👥': '',
            '🔗': '',
            '💡': '',
            '🗂️': ''
        }
        for orig, repl in replacements.items():
            text = text.replace(orig, repl)
        # Encode to latin-1 ignoring unrepresentable chars, then decode
        return text.encode('latin-1', 'ignore').decode('latin-1')

    def generate_pdf(self, session_data: dict) -> bytes:
        """Generate a clean, structured PDF report using fpdf2."""
        profile = session_data.get('profile', {})
        top3 = session_data.get('top3', [])
        recommendations = session_data.get('recommendations', [])
        insights = session_data.get('insights', [])
        charts = session_data.get('charts', [])
        prediction = session_data.get('prediction')
        filename = self._clean_txt(session_data.get('filename', 'dataset'))
        now = datetime.datetime.now().strftime("%d %B %Y, %H:%M")

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.set_margins(20, 20, 20)

        # Helper clean for all cell text
        c = self._clean_txt

        # ------------------------------------------------------------------
        # COVER PAGE
        # ------------------------------------------------------------------
        pdf.add_page()

        # Dark header band
        pdf.set_fill_color(8, 13, 26)
        pdf.rect(0, 0, 210, 70, style='F')

        from fpdf.enums import XPos, YPos

        pdf.set_y(18)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(125, 180, 250)
        pdf.cell(0, 6, 'AI BUSINESS INTELLIGENCE STUDIO', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_y(30)
        pdf.set_font('Helvetica', 'B', 24)
        pdf.set_text_color(241, 245, 249)
        pdf.cell(0, 10, 'Intelligence Report', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_y(46)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 6, f'Dataset: {filename}    |    Generated: {now}', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 5, f'{profile.get("rows", 0):,} records  |  {profile.get("columns", 0)} columns  |  Quality Score: {profile.get("quality_score", 0)}/100', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_y(78)

        # ------------------------------------------------------------------
        # SECTION HELPER
        # ------------------------------------------------------------------
        def section_title(title: str, subtitle: str = ''):
            pdf.set_font('Helvetica', 'B', 14)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_draw_color(226, 232, 240)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y())
            pdf.ln(3)
            if subtitle:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(100, 116, 139)
                pdf.cell(0, 5, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)

        def severity_color(sev: str):
            m = {'positive': (34, 197, 94), 'warning': (245, 158, 11), 'critical': (239, 68, 68), 'info': (6, 182, 212)}
            return m.get(sev, (79, 142, 247))

        def severity_label(sev: str):
            m = {'positive': 'POSITIVE', 'warning': 'WATCH', 'critical': 'CRITICAL', 'info': 'INFO'}
            return m.get(sev, 'INSIGHT')

        # ------------------------------------------------------------------
        # DATA OVERVIEW
        # ------------------------------------------------------------------
        section_title('Data Overview', 'Key statistics about the uploaded dataset')

        stats = [
            ('Records', f"{profile.get('rows', 0):,}"),
            ('Columns', str(profile.get('columns', 0))),
            ('Quality Score', f"{profile.get('quality_score', 0)}/100"),
            ('File Size', f"{profile.get('memory_mb', 0):.1f} MB"),
        ]

        col_w = 40
        for label, value in stats:
            x, y = pdf.get_x(), pdf.get_y()
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.rect(x, y, col_w - 3, 18, style='FD')
            pdf.set_xy(x + 2, y + 2)
            pdf.set_font('Helvetica', '', 7)
            pdf.set_text_color(148, 163, 184)
            pdf.cell(col_w - 7, 4, label.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_xy(x + 2, y + 7)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(col_w - 7, 6, value, new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_xy(x + col_w, y)

        pdf.ln(22)

        # ------------------------------------------------------------------
        # TOP 3 FINDINGS
        # ------------------------------------------------------------------
        section_title('Top Findings', 'The most important patterns identified in your data')

        for i, insight in enumerate(top3):
            sev = insight.get('severity', 'info')
            r, g, b = severity_color(sev)

            # Left border strip
            x, y = pdf.get_x(), pdf.get_y()
            pdf.set_fill_color(r, g, b)
            pdf.rect(x, y, 3, 28, style='F')

            # Card background
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.rect(x + 3, y, 167, 28, style='FD')

            # Icon + badge
            pdf.set_xy(x + 6, y + 3)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(r, g, b)
            badge_text = severity_label(sev)
            pdf.cell(30, 4, badge_text, new_x=XPos.RIGHT, new_y=YPos.TOP)

            # Headline
            pdf.set_xy(x + 6, y + 9)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(15, 23, 42)
            headline = c(insight.get('headline', ''))
            pdf.cell(160, 5, headline[:90] + ('...' if len(headline) > 90 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            # Explanation
            pdf.set_xy(x + 6, y + 16)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(71, 85, 105)
            explanation = c(insight.get('explanation', ''))
            pdf.multi_cell(160, 4, explanation[:150] + ('...' if len(explanation) > 150 else ''))

            pdf.set_y(y + 31)
            pdf.ln(1)

        pdf.ln(4)

        # ------------------------------------------------------------------
        # BUSINESS RECOMMENDATIONS
        # ------------------------------------------------------------------
        section_title('Business Recommendations', 'Actionable steps based on your data patterns')

        impact_colors = {'High': (239, 68, 68), 'Medium': (245, 158, 11), 'Low': (34, 197, 94)}

        for rec in recommendations:
            if pdf.get_y() > 240:
                pdf.add_page()
            x, y = pdf.get_x(), pdf.get_y()
            impact = rec.get('impact', 'Medium')
            ir, ig, ib = impact_colors.get(impact, (79, 142, 247))

            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.rect(x, y, 170, 26, style='FD')

            # Rank
            pdf.set_xy(x + 3, y + 3)
            pdf.set_font('Helvetica', 'B', 18)
            pdf.set_text_color(226, 232, 240)
            pdf.cell(10, 12, str(rec.get('rank', '')), new_x=XPos.RIGHT, new_y=YPos.TOP)

            # Impact badge
            pdf.set_xy(x + 17, y + 3)
            pdf.set_font('Helvetica', 'B', 7)
            pdf.set_text_color(ir, ig, ib)
            pdf.cell(25, 4, f"{impact.upper()} IMPACT", new_x=XPos.RIGHT, new_y=YPos.TOP)

            pdf.set_xy(x + 46, y + 3)
            pdf.set_text_color(29, 78, 216)
            pdf.cell(40, 4, c(rec.get('category', '')).upper(), new_x=XPos.RIGHT, new_y=YPos.TOP)

            # Action
            pdf.set_xy(x + 17, y + 9)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(15, 23, 42)
            action = c(rec.get('action', ''))
            pdf.cell(150, 5, action[:85] + ('...' if len(action) > 85 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            # Rationale
            pdf.set_xy(x + 17, y + 16)
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(100, 116, 139)
            rationale = c(rec.get('rationale', ''))
            pdf.cell(150, 4, rationale[:100] + ('...' if len(rationale) > 100 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            pdf.set_y(y + 29)
            pdf.ln(1)

        pdf.ln(4)

        # ------------------------------------------------------------------
        # KEY INSIGHTS
        # ------------------------------------------------------------------
        if pdf.get_y() > 200:
            pdf.add_page()

        section_title('Key Insights', 'Full ranked list of statistical findings')

        for insight in insights[:6]:
            if pdf.get_y() > 250:
                pdf.add_page()
            sev = insight.get('severity', 'info')
            r, g, b = severity_color(sev)

            x, y = pdf.get_x(), pdf.get_y()
            pdf.set_fill_color(r, g, b)
            pdf.rect(x, y, 3, 22, style='F')
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.rect(x + 3, y, 167, 22, style='FD')

            pdf.set_xy(x + 6, y + 2)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(15, 23, 42)
            headline = c(insight.get('headline', ''))
            pdf.cell(160, 5, headline[:85] + ('...' if len(headline) > 85 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            pdf.set_xy(x + 6, y + 9)
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(71, 85, 105)
            explanation = c(insight.get('explanation', ''))
            pdf.cell(160, 4, explanation[:120] + ('...' if len(explanation) > 120 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            pdf.set_xy(x + 6, y + 15)
            pdf.set_font('Helvetica', 'I', 8)
            pdf.set_text_color(100, 116, 139)
            implication = c(insight.get('business_implication', ''))
            pdf.cell(160, 4, '-> ' + implication[:110] + ('...' if len(implication) > 110 else ''), new_x=XPos.RIGHT, new_y=YPos.TOP)

            pdf.set_y(y + 25)
            pdf.ln(1)

        pdf.ln(4)

        # ------------------------------------------------------------------
        # SUPPORTING EVIDENCE (Charts)
        # ------------------------------------------------------------------
        if charts:
            if pdf.get_y() > 200:
                pdf.add_page()
            section_title('Supporting Evidence', 'Data visualisations supporting the insights above')

            for chart in charts[:4]:  # Max 4 charts in PDF
                if pdf.get_y() > 200:
                    pdf.add_page()
                png_bytes = self._render_chart_to_png(chart)
                if png_bytes:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        tmp.write(png_bytes)
                        tmp_path = tmp.name
                    try:
                        pdf.set_font('Helvetica', 'B', 10)
                        pdf.set_text_color(15, 23, 42)
                        pdf.cell(0, 5, c(chart.get('title', '')), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        pdf.ln(2)
                        pdf.image(tmp_path, x=pdf.get_x(), y=pdf.get_y(), w=170)
                        pdf.ln(90)
                        pdf.set_font('Helvetica', 'I', 8)
                        pdf.set_text_color(148, 163, 184)
                        pdf.cell(0, 4, c(chart.get('caption', '')), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                        pdf.ln(6)
                    finally:
                        try:
                            os.unlink(tmp_path)
                        except Exception:
                            pass

        # ------------------------------------------------------------------
        # PREDICTION STUDIO (if used)
        # ------------------------------------------------------------------
        if prediction:
            if pdf.get_y() > 200:
                pdf.add_page()
            section_title('Prediction Studio Results')
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 6, c(prediction.get('plain_english', '')), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(0, 5, f"Analysis method: {c(prediction.get('best_model', ''))}   |   {c(prediction.get('metric_name', ''))}: {prediction.get('metric_value', 0) * 100:.0f}%", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # ------------------------------------------------------------------
        # FOOTER ON LAST PAGE
        # ------------------------------------------------------------------
        pdf.ln(10)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(4)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(0, 4, f'Generated by BI Studio  |  {now}  |  Confidential', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        return bytes(pdf.output())
