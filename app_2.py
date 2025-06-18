import streamlit as st
import pandas as pd
import json
import openai
import os
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ---- Page Configuration ---- #
st.set_page_config(
    page_title="SLA Sentinel",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS ---- #
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .sla-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .breach-alert {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-alert {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    .stExpander > div:first-child {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---- OpenAI API Key ---- #
# SECURITY NOTE: Move this to environment variables or Streamlit secrets
# if 'OPENAI_API_KEY' not in st.secrets:
#     st.error("⚠️ OpenAI API key not found in secrets. Please add it to your Streamlit secrets.")
#     st.stop()

openai.api_key = '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'

# ---- Header ---- #
st.markdown("""
<div class="main-header">
    <h1>🚦 SLA Sentinel</h1>
    <h3>GenAI-Powered SLA Intelligence Platform</h3>
    <p>Real-time monitoring and analysis for MindGate + PayU operations</p>
</div>
""", unsafe_allow_html=True)

# ---- Sidebar Configuration ---- #
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Global settings
    st.subheader("Analysis Settings")
    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Real-time", "Batch Processing", "Historical Review"],
        help="Choose how you want to analyze the SLA data"
    )
    
    breach_threshold = st.slider(
        "Breach Sensitivity",
        min_value=0.1,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Adjust sensitivity for breach detection"
    )
    
    st.subheader("Notification Settings")
    enable_alerts = st.checkbox("Enable Real-time Alerts", value=True)
    alert_channels = st.multiselect(
        "Alert Channels",
        ["Email", "Slack", "Teams", "PagerDuty"],
        default=["Email"]
    )

# ---- Main Dashboard ---- #
col1, col2, col3, col4 = st.columns(4)

# Placeholder metrics (would be calculated from actual data)
with col1:
    st.metric(
        label="🎯 Overall SLA Health",
        value="94.2%",
        delta="2.1%",
        help="Overall SLA compliance across all services"
    )

with col2:
    st.metric(
        label="⚡ Active Breaches",
        value="3",
        delta="-2",
        delta_color="inverse",
        help="Current number of active SLA breaches"
    )

# with col3:
#     st.metric(
#         label="🔄 Avg Response Time",
#         value="145ms",
#         delta="-23ms",
#         help="Average API response time across all endpoints"
#     )

with col3:
    st.metric(
        label="📊 Services Monitored",
        value="12",
        delta="1",
        help="Total number of services under SLA monitoring"
    )

st.divider()

# ---- SLA Analysis Section ---- #
st.header("📊 SLA Analysis Dashboard")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📂 Upload & Analyze", "📈 Live Dashboard", "📋 Reports"])

with tab1:
    st.markdown("### 📂 Upload SLA Logs for Analysis")
    
    # Enhanced SLA options with descriptions
    sla_configs = {
        "Uptime SLA": {
            "icon": "🟢",
            "description": "Monitor service availability and uptime metrics",
            "threshold": "99.9%"
        },
        "Latency SLA": {
            "icon": "⚡",
            "description": "Track API response times and latency metrics",
            "threshold": "< 200ms"
        },
        "Settlement SLA": {
            "icon": "💳",
            "description": "Monitor payment settlement processing times",
            "threshold": "< 2 hours"
        },
        "Support SLA": {
            "icon": "🎧",
            "description": "Track customer support response times",
            "threshold": "< 4 hours"
        },
        "Reconciliation SLA": {
            "icon": "🔄",
            "description": "Monitor financial reconciliation processes",
            "threshold": "Daily"
        },
        "Dispute SLA": {
            "icon": "⚖️",
            "description": "Track dispute resolution timelines",
            "threshold": "< 7 days"
        },
        "Vendor SLA": {
            "icon": "🤝",
            "description": "Monitor third-party vendor performance",
            "threshold": "99.5%"
        }
    }

    # Create columns for better layout
    col_left, col_right = st.columns([2, 1])
    
    with col_right:
        st.markdown("### 🎯 Quick Stats")
        for sla, config in sla_configs.items():
            st.markdown(f"""
            <div class="metric-container">
                <strong>{config['icon']} {sla}</strong><br>
                <small>{config['description']}</small><br>
                <span style="color: #667eea;">Target: {config['threshold']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_left:
        for sla, config in sla_configs.items():
            with st.expander(f"{config['icon']} **{sla}** - {config['description']}", expanded=False):
                col_upload, col_settings = st.columns([2, 1])
                
                with col_upload:
                    uploaded_file = st.file_uploader(
                        f"Upload log file",
                        type=["json", "csv"],
                        key=sla,
                        help=f"Upload {sla} logs in JSON or CSV format"
                    )
                
                with col_settings:
                    timeline = st.selectbox(
                        "Analysis Period",
                        ["Last 1 hour", "Last 24 hours", "Last 7 days", "Last 30 days"],
                        key=f"{sla}_timeline",
                        index=1
                    )
                    
                    priority = st.selectbox(
                        "Priority Level",
                        ["Critical", "High", "Medium", "Low"],
                        key=f"{sla}_priority",
                        index=1
                    )

                if uploaded_file:
                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # ---- Read File ---- #
                    try:
                        status_text.text("📖 Reading file...")
                        progress_bar.progress(25)
                        
                        if uploaded_file.type == "application/json":
                            logs = json.load(uploaded_file)
                            df = pd.DataFrame(logs)
                        elif uploaded_file.type == "text/csv":
                            df = pd.read_csv(uploaded_file)
                        else:
                            st.error("❌ Unsupported file type.")
                            continue
                        
                        progress_bar.progress(50)
                        status_text.text("🔍 Processing data...")
                        
                        # ---- Enhanced Data Processing ---- #
                        # Add file info
                        st.info(f"📊 Loaded {len(df)} records from {uploaded_file.name}")
                        
                        # Show sample data in a more compact way
                        with st.expander("👀 Preview Data", expanded=False):
                            st.dataframe(df.head(), use_container_width=True)
                        
                        # ---- Detect SLA Breach ---- #
                        def detect_breach(row):
                            if row["sla_type"] == "response_time":
                                return "BREACH" if row["actual_value"] > row["expected_sla"] else "OK"
                            elif row["sla_type"] == "success_rate":
                                return "BREACH" if row["actual_value"] < row["expected_sla"] else "OK"
                            else:
                                return "UNKNOWN"

                        df["SLA_Status"] = df.apply(detect_breach, axis=1)
                        
                        progress_bar.progress(75)
                        status_text.text("🏷️ Adding context tags...")

                        # ---- Add Context Tags ---- #
                        def context_tags(row):
                            tags = []
                            if row.get("retry_count", 0) >= 2:
                                tags.append("high_retries")
                            if row.get("infra_status", "") == "high_load":
                                tags.append("infra_load")
                            if row.get("third_party_status", "") == "degraded":
                                tags.append("third_party_degraded")
                            return ", ".join(tags)

                        df["context"] = df.apply(context_tags, axis=1)
                        
                        # ---- Show Summary Stats ---- #
                        breach_count = len(df[df["SLA_Status"] == "BREACH"])
                        total_records = len(df)
                        breach_percentage = (breach_count / total_records * 100) if total_records > 0 else 0
                        
                        # Visual summary
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        
                        with col_stats1:
                            st.metric("Total Events", total_records)
                        with col_stats2:
                            st.metric("SLA Breaches", breach_count, delta=f"{breach_percentage:.1f}%")
                        with col_stats3:
                            compliance_rate = 100 - breach_percentage
                            st.metric("Compliance Rate", f"{compliance_rate:.1f}%")

                        # ---- GenAI Analysis ---- #
                        if breach_count > 0:
                            status_text.text("🤖 Running GenAI analysis...")
                            progress_bar.progress(90)
                            
                            def call_openai(row):
                                if row["SLA_Status"] != "BREACH":
                                    return "", "", ""

                                prompt = f"""
                                Here is an SLA breach event:

                                - Endpoint: {row['endpoint']}
                                - Partner: {row['partner']}
                                - SLA Type: {row['sla_type']}
                                - Expected SLA: {row['expected_sla']}
                                - Actual Value: {row['actual_value']}
                                - Retry Count: {row['retry_count']}
                                - Infra Status: {row['infra_status']}
                                - Third Party Status: {row['third_party_status']}
                                - Timestamp: {row['timestamp']}

                                Please provide:
                                1. A 1-line summary of what happened
                                2. The most likely cause (choose one: infra issue, third-party issue, time-based surge, unknown)
                                3. A suggested action for the DevOps team
                                """

                                try:
                                    response = openai.ChatCompletion.create(
                                        model="gpt-4o",
                                        messages=[{"role": "user", "content": prompt}],
                                        temperature=0.3,
                                    )
                                    output = response["choices"][0]["message"]["content"].strip()
                                    lines = output.split("\n")
                                    summary = lines[0].split("1.")[-1].strip() if len(lines) > 0 else ""
                                    cause = lines[1].split("2.")[-1].strip() if len(lines) > 1 else ""
                                    action = lines[2].split("3.")[-1].strip() if len(lines) > 2 else ""
                                    return summary, cause, action
                                except Exception as e:
                                    return "OpenAI Error", "N/A", str(e)

                            with st.spinner("🔍 Analyzing SLA breaches with GenAI..."):
                                df[["summary", "likely_cause", "suggested_action"]] = df.apply(
                                    lambda row: pd.Series(call_openai(row)), axis=1
                                )
                            
                            progress_bar.progress(100)
                            status_text.text("✅ Analysis complete!")
                            
                            # ---- Enhanced Results Display ---- #
                            if breach_count > 0:
                                st.markdown("### 🚨 SLA Breach Analysis")
                                
                                # Filter for breaches only
                                breach_df = df[df["SLA_Status"] == "BREACH"]
                                
                                # Group by cause for summary
                                if not breach_df.empty and "likely_cause" in breach_df.columns:
                                    cause_summary = breach_df["likely_cause"].value_counts()
                                    
                                    st.markdown("#### 📊 Breach Causes Distribution")
                                    fig = px.pie(
                                        values=cause_summary.values, 
                                        names=cause_summary.index,
                                        title="Distribution of Breach Causes"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                # Detailed breach table
                                st.markdown("#### 📋 Detailed Breach Report")
                                display_columns = [
                                    "timestamp", "endpoint", "partner", "SLA_Status", "context",
                                    "summary", "likely_cause", "suggested_action"
                                ]
                                available_columns = [col for col in display_columns if col in df.columns]
                                st.dataframe(df[available_columns], use_container_width=True, height=400)
                            else:
                                st.success("🎉 No SLA breaches detected! All systems are performing within expected parameters.")
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()

                        # ---- Enhanced Download Options ---- #
                        st.markdown("### 📥 Export Options")
                        col_download1, col_download2 = st.columns(2)
                        
                        with col_download1:
                            csv = df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                label=f"📊 Download Full Report (CSV)",
                                data=csv,
                                file_name=f"{sla.lower().replace(' ', '_')}_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                mime="text/csv",
                            )
                        
                        with col_download2:
                            if breach_count > 0:
                                breach_csv = df[df["SLA_Status"] == "BREACH"].to_csv(index=False).encode("utf-8")
                                st.download_button(
                                    label=f"🚨 Download Breaches Only (CSV)",
                                    data=breach_csv,
                                    file_name=f"{sla.lower().replace(' ', '_')}_breaches_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                    mime="text/csv",
                                )
                    
                    except Exception as e:
                        st.error(f"❌ Error processing file: {str(e)}")
                        progress_bar.empty()
                        status_text.empty()

with tab2:
    st.markdown("### 📈 Live SLA Dashboard")
    st.info("🚧 Live dashboard coming soon! This will show real-time SLA metrics and alerts.")
    
    # Placeholder for live dashboard
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔄 Real-time Metrics")
        st.line_chart([1, 2, 3, 4, 5])
    
    with col2:
        st.markdown("#### 🎯 SLA Targets vs Actual")
        st.bar_chart([0.95, 0.98, 0.94, 0.99])

with tab3:
    st.markdown("### 📋 Historical Reports")
    st.info("📊 Historical reporting features coming soon!")
    
    # Placeholder for reports
    report_type = st.selectbox(
        "Report Type",
        ["Daily Summary", "Weekly Trends", "Monthly Overview", "Custom Range"]
    )
    
    if st.button("Generate Report"):
        st.success("Report generation would start here!")

# ---- Footer ---- #
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🚦 SLA Sentinel v2.0 | Powered by GenAI | MindGate + PayU Operations</small>
</div>
""", unsafe_allow_html=True)