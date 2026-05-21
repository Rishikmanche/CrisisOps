import streamlit as st
import feedparser
import requests
import pandas as pd
import random
import datetime
import urllib.parse 

# --- OPEN-METEO API (Dynamic) ---
def get_live_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,rain,relative_humidity_2m&timezone=auto"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data['current']
        return {
            "temp": f"{current['temperature_2m']}°C",
            "wind": f"{current['wind_speed_10m']} km/h",
            "rain": f"{current['rain']} mm",
            "humidity": f"{current['relative_humidity_2m']}%",
            "is_raining": current['rain'] > 0,
            "status": "Success"
        }
    except Exception as e:
        # FIX: Added 'is_raining' and 'status' to the fallback dictionary 
        return {
            "temp": "--", 
            "wind": "--", 
            "rain": "--", 
            "humidity": "--", 
            "is_raining": False, 
            "status": "Error"
        }

def render_data_sources():
    st.subheader("🔌 Context-Aware Data Connectors")
    
    # 1. IDENTIFY THE ACTIVE LOCATION
    if st.session_state.get('reports'):
        latest_report = st.session_state['reports'][-1]
        target_lat = latest_report['lat']
        target_lon = latest_report['lon']
        target_name = latest_report.get('location_name', 'Unknown Location')
        is_live = True
    else:
        target_lat = 17.3850
        target_lon = 78.4867
        target_name = "Hyderabad"
        is_live = False

    if is_live:
        st.success(f"📍 Targeting Active Incident: **{target_name}**")
    else:
        st.info("System Standby: Monitoring Default Region (Hyderabad)")

    # --- LAYOUT: 3 Columns ---
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # ==========================
    # COLUMN 1: DYNAMIC WEATHER
    # ==========================
    with col1:
        st.markdown(f"### 🌤️ Local Weather")
        st.caption(f"Real-time conditions at **{target_name}**")
        
        weather = get_live_weather(target_lat, target_lon)
        
        with st.container(border=True):
            c_temp, c_icon = st.columns([2, 1])
            with c_temp:
                st.metric("Temperature", weather['temp'])
            with c_icon:
                # This line no longer causes a KeyError 
                if weather['is_raining']:
                    st.write("🌧️ **RAIN**")
                else:
                    st.write("☀️ **CLEAR**")
            
            st.divider()
            c_wind, c_rain, c_hum = st.columns(3)
            c_wind.metric("Wind", weather['wind'])
            c_rain.metric("Rain", weather['rain'])
            c_hum.metric("Humidity", weather['humidity'])

    # ==========================
    # COLUMN 2: NEWS (Contextual)
    # ==========================
    with col2:
        st.markdown("### 📰 Related News")
        st.caption(f"Searching for disaster news near **{target_name}**...")
        
        try:
            raw_query = f"{target_name} disaster flood fire accident"
            encoded_query = urllib.parse.quote(raw_query)
            
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
            
            feed = feedparser.parse(rss_url)
            
            if feed.entries:
                with st.container(height=300):
                    for entry in feed.entries[:6]:
                        with st.container(border=True):
                            st.caption(f"📢 {entry.source.title}")
                            st.markdown(f"[{entry.title}]({entry.link})")
                            st.text(f"Posted: {entry.published[:17]}")
            else:
                st.warning(f"No specific news found for {target_name}.")
                
        except Exception as e:
            st.error(f"RSS Error: {e}")

    # ==========================
    # COLUMN 3: RAW DATA INSPECTOR
    # ==========================
    with col3:
        st.markdown("### 🕵️ Data Inspector")
        st.caption("Verifying JSON payload for this alert")
        
        if is_live:
            st.code(f"""
{{
  "incident_id": "{latest_report.get('id', 'N/A')}",
  "timestamp": "{latest_report.get('timestamp')}",
  "type": "{latest_report.get('type')}",
  "location": {{
    "name": "{target_name}",
    "lat": {target_lat:.4f},
    "lon": {target_lon:.4f}
  }},
  "weather_context": {{
    "temp": "{weather['temp']}",
    "condition": "{'RAIN' if weather['is_raining'] else 'CLEAR'}"
  }}
}}
            """, language="json")
            
            st.success("✅ Data Integrity Verified")
        else:
            st.warning("No active alert selected.")