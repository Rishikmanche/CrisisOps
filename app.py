import streamlit as st
import pandas as pd
import datetime
from data.simulator import generate_fake_report
from components.map_view import render_map
from components.data_feed import render_data_sources # Import the new tab
from utils.gemini_brain import analyze_incident

# --- 🔐 CONFIGURATION ---
GEMINI_KEY = "REDACTED"  # <--- PASTE KEY HERE

# --- PAGE CONFIG ---
st.set_page_config(page_title="DisasterGuard AI", page_icon="🛡️", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
        .stApp {background-color: #0e1117;}
        div.stButton > button {
            background-color: #ff4b4b; color: white; border-radius: 8px; width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'reports' not in st.session_state:
    st.session_state['reports'] = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ DisasterGuard")
    st.caption("Status: 🟢 SYSTEM ONLINE")
    
    if st.button("📡 SCAN SATELLITE & SOCIAL FEED"):
        with st.spinner("AI Analyzing Stream..."):
            # 1. Get Fake Raw Data
            raw_data = generate_fake_report()
            
            # 2. AI Analysis
            ai_result = analyze_incident(GEMINI_KEY, raw_data['raw_text'])
            
            # 3. Merge AI result into raw data
            final_report = {**raw_data, **ai_result}
            
            # 4. Add Icon logic based on type
            icons = {
                "Fire": {"icon": "fire", "color": "red", "emoji": "🔥"},
                "Flood": {"icon": "tint", "color": "blue", "emoji": "🌊"},
                "Accident": {"icon": "car", "color": "orange", "emoji": "🚗"},
                "Medical": {"icon": "plus", "color": "green", "emoji": "🏥"},
                "Earthquake": {"icon": "globe", "color": "purple", "emoji": "🌍"},
                "Other": {"icon": "info-sign", "color": "gray", "emoji": "⚠️"}
            }
            style = icons.get(final_report['type'], icons["Other"])
            final_report.update(style)
            
            st.session_state['reports'].append(final_report)
            
            if final_report['is_real']:
                st.toast(f"🚨 {final_report['type']} Detected!", icon="🔥")
            else:
                st.toast("Filtered low priority message.", icon="🗑️")

    st.divider()
    st.markdown("### 📊 Live Metrics")
    st.metric("AI Latency", "124ms", "-12ms")
    st.metric("Source Reliability", "94%", "+2%")

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["🗺️ COMMAND CENTER", "🔌 DATA SOURCES"])

with tab1:
    # Top Stats
    c1, c2, c3 = st.columns(3)
    critical_count = len([r for r in st.session_state['reports'] if r['severity'] >= 8])
    c1.metric("Active Incidents", len(st.session_state['reports']))
    c2.metric("Critical Threats", critical_count, "High Risk", delta_color="inverse")
    c3.metric("AI Model", "Gemini 1.5 Flash", "Active")

    col_map, col_feed = st.columns([2, 1])
    
    with col_map:
        render_map(st.session_state['reports'])
    
    with col_feed:
        st.subheader("🚨 Priority Feed")
        if not st.session_state['reports']:
            st.info("System Ready. Waiting for input...")
        
        for report in reversed(st.session_state['reports'][-4:]):
            with st.container(border=True):
                st.markdown(f"**{report['emoji']} {report['type']}**")
                st.caption(f"📍 {report['location_name']} | 🕒 {report['timestamp']}")
                st.write(report['description'])
                st.progress(report['severity']/10, text=f"Severity: {report['severity']}/10")

with tab2:
    # Call the new Data Sources Component
    render_data_sources()