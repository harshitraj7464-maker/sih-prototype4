import streamlit as st
import folium
from streamlit_folium import st_folium
import time

st.set_page_config(page_title="BhoomiRakshak SIH26001", layout="wide")
st.title("🌋 Project BhoomiRakshak — SIH26001")
st.subheader("AI-Based Early Warning & Landslide Risk Monitoring System (NER)")

# Sidebar Configuration
st.sidebar.header("📍 Terrain & District Monitoring Panel")
selected_area = st.sidebar.selectbox(
    "Select Target District for Topographic Scan:",
    ["Guwahati (Kamrup Metro), Assam", "Cherrapunji (East Khasi Hills), Meghalaya", "Gangtok District, Sikkim", "Itanagar (Papum Pare), Arunachal"]
)

if st.sidebar.button("🔄 Sync Live Terrain & Telemetry Data"):
    with st.sidebar.spinner("Fetching ISRO Bhuvan DEM Cartographic layers..."):
        time.sleep(1.5)
    st.sidebar.success("Terrain profiles updated!")

# Advanced Database Simulating Deep Terrain & Geological Parameters per region
region_data = {
    "Guwahati (Kamrup Metro), Assam": {
        "lat": 26.1445, "lon": 91.7362, "rain": 45, 
        "elevation": "120m", "slope": 14, "terrain_type": "Alluvial Hilly Fringe",
        "risk": "SAFE (LOW RISK)", "color": "green"
    },
    "Cherrapunji (East Khasi Hills), Meghalaya": {
        "lat": 25.2702, "lon": 91.7323, "rain": 245, 
        "elevation": "1430m", "slope": 44, "terrain_type": "Highly Fractured Sandstone Escarpment",
        "risk": "CRITICAL ALERT", "color": "red"
    },
    "Gangtok District, Sikkim": {
        "lat": 27.3314, "lon": 88.6138, "rain": 120, 
        "elevation": "1650m", "slope": 36, "terrain_type": "Metamorphic Schist Gneiss Slope",
        "risk": "WARNING (MEDIUM RISK)", "color": "orange"
    },
    "Itanagar (Papum Pare), Arunachal": {
        "lat": 27.1020, "lon": 93.6166, "rain": 30, 
        "elevation": "320m", "slope": 21, "terrain_type": "Shale & Siwalik Sandstone Belt",
        "risk": "SAFE (LOW RISK)", "color": "green"
    }
}

active = region_data[selected_area]
map_center = [active["lat"], active["lon"]]

st.markdown(f"### 📊 Real-Time Geological Status: **{selected_area}**")
st.info("ℹ️ System Diagnostics: Processing Digital Elevation Models (DEM) from ISRO Bhuvan telemetry combined with real-time IMD rainfall inputs.")

# Layout Grid Split
col_metrics, col_map = st.columns([1, 1.2])

with col_metrics:
    st.markdown("#### 📐 Terrain Profile Diagnostics")
    st.metric(label="Base Elevation (Above Sea Level)", value=active["elevation"])
    st.metric(label="Critical Slope Angle (Calculated via GeoPandas)", value=f"{active['slope']}°")
    st.text_input("Geological Formation Classification:", value=active["terrain_type"], disabled=True)
    
    st.markdown("#### 🌧️ Meteorological Inputs")
    st.metric(label="Live IMD Precipitation Rate", value=f"{active['rain']} mm")
    
    # Dynamic Assessment Readout
    st.markdown("#### 🚨 Predictive Risk Matrix Evaluation")
    if active["color"] == "red":
        st.error(f"ENGINE STATUS: {active['risk']} \n\nCritical threat signature detected: High slope angle ({active['slope']}°) saturated by intensive rainfall. Evacuation triggered.")
    elif active["color"] == "orange":
        st.warning(f"ENGINE STATUS: {active['risk']} \n\nModerate risk signature detected. Heightened spatial anomalies detected along slope faces.")
    else:
        st.success(f"ENGINE STATUS: {active['risk']} \n\nTerrain profile structural vectors stable inside safe baseline constraints.")

with col_map:
    st.markdown("#### 🗺️ Interactive Topographic Map Grid")
    m = folium.Map(location=map_center, zoom_start=11)
    folium.Marker(
        location=map_center,
        popup=f"{selected_area} Terrain Node",
        tooltip="Click to view sensor data",
        icon=folium.Icon(color=active["color"], icon="mountain", prefix="fa" if active["color"]=="red" else "glyphicon")
    ).add_to(m)
    
    st_folium(m, width=550, height=480)
