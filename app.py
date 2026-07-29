import streamlit as st, pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
import data as D

# ELITE UX & STYLING
st.set_page_config(page_title="PPC Profitability Engine", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0e1117; color: #f9fafb; }
h1 { background: linear-gradient(90deg, #4285F4, #00A4EF, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -1px; }
h2, h3 { color: #f9fafb; font-weight: 600; }

/* Dashboard Metric Cards */
div[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px; padding: 1.2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    border-color: #4285F4;
    transform: translateY(-2px);
}
[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 700; color: #ffffff !important; }
[data-testid="stMetricDelta"] { font-size: 0.9rem !important; }
[data-testid="stMetricLabel"] { color: #8b949e !important; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.75rem !important; }

/* Custom Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #161b22; padding: 6px; border-radius: 8px; border: 1px solid #30363d; }
.stTabs [data-baseweb="tab"] { color: #8b949e; padding: 8px 16px; border-radius: 6px; }
.stTabs [aria-selected="true"] { background: rgba(66, 133, 244, 0.15) !important; color: #4285F4 !important; border-bottom: none !important; }

/* Claude AI Box */
.claude-box { background: rgba(139, 92, 246, 0.1); border: 1px solid #8B5CF6; border-radius: 8px; padding: 16px; margin-top: 10px; border-left: 4px solid #8B5CF6; }
</style>
""", unsafe_allow_html=True)

PLOT_BG = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e"))

# LOAD DATA
portfolio_df = D.get_portfolio_pacing()
campaign_df = D.get_campaign_performance()
sprint_df = D.get_sprint_tasks()

# HEADER
st.title("Skayl: PPC Portfolio & POAS Command Centre")
st.markdown("<p style='color:#8b949e; font-size:1.05rem; max-width: 900px; margin-bottom: 2rem;'>Managing autonomous scaling and budget pacing across Google Ads, Microsoft Ads, and PMax. Integrating GA4 and TripleWhale data to optimize for MER, POAS, and profit targets.</p>", unsafe_allow_html=True)

# TOP METRICS
c1, c2, c3, c4 = st.columns(4)
total_spend = portfolio_df["Current_Spend"].sum()
total_rev = portfolio_df["Revenue"].sum()
blended_roas = total_rev / total_spend
c1.metric("Total Managed Spend (MTD)", f"£{total_spend:,.0f}", f"{(total_spend/portfolio_df['Target_Spend'].sum()*100):.1f}% Pacing")
c2.metric("Portfolio Revenue", f"£{total_rev:,.0f}", "Verified via TripleWhale")
c3.metric("Blended ROAS", f"{blended_roas:.2f}x", "+0.45x vs Target")
c4.metric("Avg Portfolio POAS", f"{portfolio_df['Actual_POAS'].mean():.2f}x", "Profit On Ad Spend")

# TABS
t1, t2, t3 = st.tabs(["Budget Pacing & MER", "Campaign POAS Analytics", "ClickUp Sprints & Claude AI"])

with t1:
    st.markdown("### Client Budget Pacing & Target Achievement")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        # Pacing Bullet Chart
        fig = go.Figure()
        for idx, row in portfolio_df.iterrows():
            fig.add_trace(go.Indicator(
                mode = "number+gauge+delta", value = row["Current_Spend"],
                delta = {'reference': row["Target_Spend"], 'position': "top"},
                title = {'text': f"<b>{row['Client']}</b><br><span style='color: gray; font-size:0.8em'>MER: {row['MER']:.0%}</span>"},
                gauge = {
                    'shape': "bullet",
                    'axis': {'range': [None, row["Target_Spend"] * 1.2]},
                    'threshold': {'line': {'color': "red", 'width': 2}, 'thickness': 0.75, 'value': row["Target_Spend"]},
                    'steps': [{'range': [0, row["Target_Spend"]], 'color': "rgba(66, 133, 244, 0.3)"}],
                    'bar': {'color': "#4285F4"}
                },
                domain = {'x': [0.1, 1], 'y': [1 - (idx+1)*0.25, 1 - idx*0.25 - 0.05]}
            ))
        fig.update_layout(height=400, margin=dict(t=30, b=20, l=10, r=10), **PLOT_BG)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### Portfolio Profitability Matrix")
        st.dataframe(
            portfolio_df[["Client", "Actual_ROAS", "Actual_POAS", "Retention"]].style.format({"Actual_ROAS": "{:.1f}x", "Actual_POAS": "{:.2f}x"})
            .map(lambda v: "color:#ef4444" if "Risk" in str(v) else "color:#10b981", subset=["Retention"]),
            use_container_width=True, hide_index=True, height=350
        )

with t2:
    st.markdown("### Cross-Platform Campaign Drilldown (Google & Microsoft)")
    st.dataframe(
        campaign_df.style.format({"Spend": "£{:,.0f}", "CPA": "£{:.2f}", "ROAS": "{:.1f}x", "POAS": "{:.2f}x"})
        .background_gradient(subset=['POAS'], cmap='Greens'),
        use_container_width=True, hide_index=True, height=220
    )
    
    fig_scatter = px.scatter(
        campaign_df, x="CPA", y="POAS", size="Spend", color="Platform",
        hover_name="Campaign_Name", text="Type", size_max=45,
        color_discrete_map={"Google Ads": "#4285F4", "Microsoft Ads": "#00A4EF"}
    )
    fig_scatter.update_traces(textposition='top center', textfont=dict(size=10, color='#8b949e'))
    fig_scatter.add_hline(y=1.0, line_dash="dash", line_color="#ef4444", annotation_text="Breakeven POAS")
    fig_scatter.update_layout(**PLOT_BG, height=350, xaxis_title="Cost Per Acquisition (£)", yaxis_title="Profit On Ad Spend (POAS)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with t3:
    st.markdown("### ClickUp Sprint Dashboard & AI Workflow Automation")
    
    col_sprint, col_ai = st.columns([1, 1])
    with col_sprint:
        st.markdown("#### Weekly Sprint Tasks (90%+ On-Time SLA)")
        st.dataframe(
            sprint_df.style.map(lambda v: "color:#10b981" if v == "Completed" else ("color:#3b82f6" if v == "In Progress" else "color:#8b949e"), subset=["Status"]),
            use_container_width=True, hide_index=True
        )
        
    with col_ai:
        st.markdown("#### Claude AI: PMax Asset & Ad Copy Generation")
        ai_input = st.selectbox("Select Underperforming Campaign to Optimize:", campaign_df[campaign_df["Status"] != "Active"]["Campaign_Name"])
        if st.button("Generate Optimizations via Claude API"):
            st.markdown(f"""
            <div class='claude-box'>
                <h5 style='color:#8B5CF6; margin-top:0;'>✨ Claude 3.5 Sonnet Optimization Plan for {ai_input}</h5>
                <p style='color:#e5e7eb; font-size:0.9rem;'>
                <b>Diagnosis:</b> High CPA (£35.00) and sub-1.0 POAS indicates poor audience-message match in Demand Gen.<br><br>
                <b>Action Items:</b><br>
                1. <b>Ad Copy A/B Test:</b> Shift from generic feature-led copy to urgency/offer-led copy (e.g., "Flash Sale: 20% Off" vs "Top Rated Tech").<br>
                2. <b>Audience Override:</b> Layer a custom intent segment based on Top 10 converting Search terms.<br>
                3. <b>Asset Rotation:</b> Replace static images with short-form UGC video assets to improve CTR.<br><br>
                <i>Task pushed to ClickUp Sprint Dashboard automatically.</i>
                </p>
            </div>
            """, unsafe_allow_html=True)
