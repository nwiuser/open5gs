"""
Streamlit UI for 4G/5G Core Migration Dashboard
Beautiful visualization of migration logs and component status
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
import subprocess
import os
import random
import asyncio

# ============== Page Configuration ==============
st.set_page_config(
    page_title="4G/5G Core Migration Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== Custom CSS for Beautiful UI ==============
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Gradient Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 10px;
    }
    
    /* Component Cards */
    .component-card {
        background: linear-gradient(145deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .component-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .component-card.running {
        border-left-color: #00d98b;
    }
    
    .component-card.pending {
        border-left-color: #ffc107;
    }
    
    .component-card.error {
        border-left-color: #ff4757;
    }
    
    .component-card.migrating {
        border-left-color: #667eea;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-running {
        background: linear-gradient(135deg, #00d98b 0%, #00b377 100%);
        color: white;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
        color: #1a1a2e;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ff4757 0%, #e0303f 100%);
        color: white;
    }
    
    .status-migrating {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Log Entry Styles */
    .log-entry {
        background: #1e1e2e;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 8px 0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.85rem;
        border-left: 3px solid;
    }
    
    .log-info {
        border-left-color: #00d98b;
        color: #00d98b;
    }
    
    .log-warn {
        border-left-color: #ffc107;
        color: #ffc107;
    }
    
    .log-error {
        border-left-color: #ff4757;
        color: #ff4757;
    }
    
    .log-debug {
        border-left-color: #a0a0a0;
        color: #a0a0a0;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, transparent 100%);
        padding: 12px 20px;
        border-radius: 8px;
        margin: 25px 0 15px 0;
        font-weight: 600;
        font-size: 1.2rem;
        color: white;
    }
    
    /* Core Type Labels */
    .core-4g {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .core-5g {
        background: linear-gradient(135deg, #4ecdc4 0%, #3db9b1 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Migration Arrow */
    .migration-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #667eea;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Metrics Container */
    .metric-container {
        background: linear-gradient(145deg, #252540 0%, #1a1a2e 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Progress Bar Custom */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #2d2d44 0%, #1e1e2e 100%);
        border-radius: 8px;
    }
    
    /* Table Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============== API Configuration ==============
API_BASE_URL = "http://localhost:8000"

# ============== Helper Functions ==============

def fetch_data(endpoint: str):
    """Fetch data from the API or return mock data if API is down"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Fallback to local mock data
    return get_local_mock_data(endpoint)

# ============== Standalone Mock Data Logic ==============

COMPONENTS_4G = {
    "hss": {"full_name": "Home Subscriber Server", "description": "Subscriber database and authentication"},
    "mme": {"full_name": "Mobility Management Entity", "description": "Handles UE mobility and session management"},
    "sgwc": {"full_name": "Serving Gateway Control Plane", "description": "Routes and forwards user data packets"},
    "sgwu": {"full_name": "Serving Gateway User Plane", "description": "User plane traffic handling"},
    "pgwc": {"full_name": "PDN Gateway Control Plane", "description": "Connects to external networks"},
    "pgwu": {"full_name": "PDN Gateway User Plane", "description": "PDN user plane traffic"},
    "pcrf": {"full_name": "Policy and Charging Rules Function", "description": "Policy decisions and charging"},
    "mongodb": {"full_name": "MongoDB Database", "description": "Subscriber data storage"},
}

COMPONENTS_5G = {
    "amf": {"full_name": "Access and Mobility Management Function", "description": "Replaces MME functionality"},
    "smf": {"full_name": "Session Management Function", "description": "Session management and IP allocation"},
    "upf": {"full_name": "User Plane Function", "description": "Replaces SGW-U and PGW-U"},
    "nrf": {"full_name": "Network Repository Function", "description": "Service discovery and registration"},
    "udm": {"full_name": "Unified Data Management", "description": "Replaces HSS subscriber management"},
    "udr": {"full_name": "Unified Data Repository", "description": "Stores subscription data"},
    "ausf": {"full_name": "Authentication Server Function", "description": "Authentication procedures"},
    "nssf": {"full_name": "Network Slice Selection Function", "description": "Network slicing selection"},
    "pcf": {"full_name": "Policy Control Function", "description": "Replaces PCRF functionality"},
}

def generate_local_component_status(name, info):
    statuses = ["running", "running", "running", "pending", "error"]
    return {
        **info,
        "status": random.choice(statuses),
        "pod_count": random.randint(1, 3),
        "cpu_usage": round(random.uniform(5, 85), 2),
        "memory_usage": round(random.uniform(10, 70), 2),
        "last_updated": datetime.now().isoformat()
    }

def get_local_mock_data(endpoint: str):
    """Handle mock data for standalone mode"""
    if endpoint == "/api/4g/components":
        return {name: generate_local_component_status(name, info) for name, info in COMPONENTS_4G.items()}
    
    if endpoint == "/api/5g/components":
        return {name: generate_local_component_status(name, info) for name, info in COMPONENTS_5G.items()}
    
    if endpoint == "/api/migration/status":
        return {
            "phase": "Standalone Mode",
            "progress": 45.0,
            "active_subscribers_migrated": 15000,
            "total_subscribers": 50000
        }
    
    if endpoint == "/api/component-mapping":
        return {
            "mappings": [
                {"4g": "hss", "5g": ["udm", "udr", "ausf"], "description": "HSS splits into UDM, UDR, and AUSF"},
                {"4g": "mme", "5g": ["amf"], "description": "MME becomes AMF in 5G"},
                {"4g": "sgwc", "5g": ["smf"], "description": "SGW-C merges into SMF"},
                {"4g": "sgwu", "5g": ["upf"], "description": "SGW-U becomes part of UPF"},
                {"4g": "pgwc", "5g": ["smf"], "description": "PGW-C merges into SMF"},
                {"4g": "pgwu", "5g": ["upf"], "description": "PGW-U becomes part of UPF"},
                {"4g": "pcrf", "5g": ["pcf"], "description": "PCRF becomes PCF"},
                {"4g": None, "5g": ["nrf"], "description": "NRF is new in 5G (service discovery)"},
                {"4g": None, "5g": ["nssf"], "description": "NSSF is new in 5G (network slicing)"},
            ]
        }
    
    if "logs" in endpoint:
        # Mock logs
        core_type = "4G" if "4g" in endpoint else "5G"
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "component": endpoint.split("/")[-1] if "all" not in endpoint else "system",
                "level": random.choice(["INFO", "WARN", "DEBUG"]),
                "message": f"Simulated log message for {endpoint}",
                "core_type": core_type
            } for _ in range(10)
        ]
    
    return None

def get_status_color(status: str) -> str:
    """Get color based on status"""
    colors = {
        "running": "#00d98b",
        "pending": "#ffc107",
        "error": "#ff4757",
        "migrating": "#667eea"
    }
    return colors.get(status, "#a0a0a0")

def get_log_color(level: str) -> str:
    """Get color based on log level"""
    colors = {
        "INFO": "#00d98b",
        "WARN": "#ffc107",
        "ERROR": "#ff4757",
        "DEBUG": "#a0a0a0"
    }
    return colors.get(level, "#a0a0a0")

def render_component_card(name: str, info: dict, core_type: str):
    """Render a component status card"""
    status = info.get("status", "unknown")
    color = get_status_color(status)
    core_label = "4G" if core_type == "4G" else "5G"
    core_class = "core-4g" if core_type == "4G" else "core-5g"
    
    st.markdown(f"""
    <div class="component-card {status}" style="border-left-color: {color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div>
                <span class="{core_class}">{core_label}</span>
                <strong style="color: white; margin-left: 10px; font-size: 1.1rem;">{name.upper()}</strong>
            </div>
            <span class="status-badge status-{status}">{status}</span>
        </div>
        <p style="color: #a0a0a0; margin: 5px 0; font-size: 0.9rem;">{info.get('full_name', '')}</p>
        <p style="color: #707070; margin: 5px 0; font-size: 0.8rem;">{info.get('description', '')}</p>
        <div style="display: flex; gap: 20px; margin-top: 15px;">
            <div>
                <span style="color: #667eea; font-weight: 600;">{info.get('pod_count', 0)}</span>
                <span style="color: #707070; font-size: 0.8rem;"> Pods</span>
            </div>
            <div>
                <span style="color: #00d98b; font-weight: 600;">{info.get('cpu_usage', 0):.1f}%</span>
                <span style="color: #707070; font-size: 0.8rem;"> CPU</span>
            </div>
            <div>
                <span style="color: #ffc107; font-weight: 600;">{info.get('memory_usage', 0):.1f}%</span>
                <span style="color: #707070; font-size: 0.8rem;"> Memory</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_log_entry(log: dict):
    """Render a single log entry"""
    level = log.get("level", "INFO")
    color = get_log_color(level)
    timestamp = log.get("timestamp", "")[:19]
    component = log.get("component", "").upper()
    message = log.get("message", "")
    core_type = log.get("core_type", "")
    
    st.markdown(f"""
    <div class="log-entry log-{level.lower()}">
        <span style="color: #707070;">[{timestamp}]</span>
        <span style="color: {color}; font-weight: 600;"> [{level}]</span>
        <span style="color: #667eea;"> [{core_type}:{component}]</span>
        <span style="color: white;"> {message}</span>
    </div>
    """, unsafe_allow_html=True)

# ============== Main UI ==============

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📡 4G/5G Core Migration</h1>
        <p>Simplified Control Center for Network Core Transition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        
        view_mode = st.radio(
            "Select View",
            ["Migration Center", "System Logs", "Network Overview"],
            index=0
        )
        
        st.markdown("---")
        
        auto_refresh = st.checkbox("🔄 Auto Refresh Status", value=True)
        refresh_interval = st.slider("Interval (sec)", 2, 30, 5)
        
        if st.button("🔃 Refresh Now", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔌 Connection")
        st.success("Kubernetes Connected")
        st.info("Namespace: open5gs")
    
    # Main Content Area
    if view_mode == "Migration Center":
        render_migration_console()
    elif view_mode == "System Logs":
        render_live_logs()
    elif view_mode == "Network Overview":
        render_overview()
    
    # Auto refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

def render_overview():
    """Render the overview dashboard"""
    st.markdown('<div class="section-header">📈 Migration Overview</div>', unsafe_allow_html=True)
    
    # Migration Progress
    col1, col2, col3, col4 = st.columns(4)
    
    migration_status = fetch_data("/api/migration/status") or {
        "phase": "Testing",
        "progress": 65.5,
        "active_subscribers_migrated": 32750,
        "total_subscribers": 50000
    }
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{migration_status['progress']:.1f}%</div>
            <div class="metric-label">Migration Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{migration_status['phase']}</div>
            <div class="metric-label">Current Phase</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{migration_status['active_subscribers_migrated']:,}</div>
            <div class="metric-label">Subscribers Migrated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{migration_status['total_subscribers']:,}</div>
            <div class="metric-label">Total Subscribers</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress bar
    st.progress(migration_status['progress'] / 100)
    
    # Component Status Side by Side
    col_4g, col_arrow, col_5g = st.columns([5, 1, 5])
    
    with col_4g:
        st.markdown('<div class="section-header">📱 4G EPC Core</div>', unsafe_allow_html=True)
        components_4g = fetch_data("/api/4g/components")
        if components_4g:
            for name, info in list(components_4g.items())[:4]:
                render_component_card(name, info, "4G")
    
    with col_arrow:
        st.markdown("""
        <div style="height: 100%; display: flex; align-items: center; justify-content: center;">
            <div class="migration-arrow">➡️</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_5g:
        st.markdown('<div class="section-header">📶 5G Core (5GC)</div>', unsafe_allow_html=True)
        components_5g = fetch_data("/api/5g/components")
        if components_5g:
            for name, info in list(components_5g.items())[:4]:
                render_component_card(name, info, "5G")

def render_4g_details():
    """Render 4G core details"""
    st.markdown('<div class="section-header">📱 4G EPC Core Components</div>', unsafe_allow_html=True)
    
    components = fetch_data("/api/4g/components")
    
    if components:
        # Create 2-column layout
        cols = st.columns(2)
        for i, (name, info) in enumerate(components.items()):
            with cols[i % 2]:
                render_component_card(name, info, "4G")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 4G Core Recent Logs</div>', unsafe_allow_html=True)
        
        selected_component = st.selectbox(
            "Select Component",
            options=list(components.keys()),
            format_func=lambda x: f"{x.upper()} - {components[x]['full_name']}"
        )
        
        logs = fetch_data(f"/api/4g/logs/{selected_component}") or []
        for log in logs[:15]:
            render_log_entry(log)
    else:
        st.warning("⚠️ Unable to connect to API. Make sure the FastAPI server is running on port 8000.")
        st.code("uvicorn api.main:app --reload --port 8000")

def render_5g_details():
    """Render 5G core details"""
    st.markdown('<div class="section-header">📶 5G Core (5GC) Components</div>', unsafe_allow_html=True)
    
    components = fetch_data("/api/5g/components")
    
    if components:
        # Create 2-column layout
        cols = st.columns(2)
        for i, (name, info) in enumerate(components.items()):
            with cols[i % 2]:
                render_component_card(name, info, "5G")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 5G Core Recent Logs</div>', unsafe_allow_html=True)
        
        selected_component = st.selectbox(
            "Select Component",
            options=list(components.keys()),
            format_func=lambda x: f"{x.upper()} - {components[x]['full_name']}"
        )
        
        logs = fetch_data(f"/api/5g/logs/{selected_component}") or []
        for log in logs[:15]:
            render_log_entry(log)
    else:
        st.warning("⚠️ Unable to connect to API. Make sure the FastAPI server is running on port 8000.")
        st.code("uvicorn api.main:app --reload --port 8000")

def render_migration_mapping():
    """Render the migration mapping between 4G and 5G components"""
    st.markdown('<div class="section-header">🔄 4G to 5G Component Migration Mapping</div>', unsafe_allow_html=True)
    
    mappings = fetch_data("/api/component-mapping")
    
    if mappings:
        for mapping in mappings.get("mappings", []):
            col1, col2, col3 = st.columns([3, 1, 3])
            
            with col1:
                if mapping.get("4g"):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%); 
                                padding: 20px; border-radius: 12px; text-align: center; color: white;">
                        <strong style="font-size: 1.3rem;">{mapping['4g'].upper()}</strong>
                        <p style="margin-top: 5px; font-size: 0.9rem;">4G Component</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: #2d2d44; padding: 20px; border-radius: 12px; 
                                text-align: center; color: #707070;">
                        <strong style="font-size: 1.3rem;">N/A</strong>
                        <p style="margin-top: 5px; font-size: 0.9rem;">No 4G equivalent</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <span style="font-size: 2rem; color: #667eea;">➡️</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                components_5g = mapping.get("5g", [])
                components_str = ", ".join([c.upper() for c in components_5g])
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ecdc4 0%, #3db9b1 100%); 
                            padding: 20px; border-radius: 12px; text-align: center; color: white;">
                    <strong style="font-size: 1.3rem;">{components_str}</strong>
                    <p style="margin-top: 5px; font-size: 0.9rem;">5G Component(s)</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <p style="text-align: center; color: #a0a0a0; margin: 10px 0 25px 0;">
                {mapping.get('description', '')}
            </p>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Unable to connect to API. Make sure the FastAPI server is running on port 8000.")

def render_live_logs():
    """Render live combined logs view"""
    st.markdown('<div class="section-header">📋 Live Combined Logs</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        core_filter = st.selectbox("Core Type", ["All", "4G", "5G"])
    with col2:
        level_filter = st.selectbox("Log Level", ["All", "INFO", "WARN", "ERROR", "DEBUG"])
    with col3:
        log_count = st.slider("Number of Logs", 10, 100, 30)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch logs
    all_logs = []
    
    if core_filter in ["All", "4G"]:
        logs_4g = fetch_data(f"/api/4g/logs/all?count={log_count}") or []
        all_logs.extend(logs_4g)
    
    if core_filter in ["All", "5G"]:
        logs_5g = fetch_data(f"/api/5g/logs/all?count={log_count}") or []
        all_logs.extend(logs_5g)
    
    # Filter by level
    if level_filter != "All":
        all_logs = [log for log in all_logs if log.get("level") == level_filter]
    
    # Sort by timestamp
    all_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Log stats
    col1, col2, col3, col4 = st.columns(4)
    info_count = len([l for l in all_logs if l.get("level") == "INFO"])
    warn_count = len([l for l in all_logs if l.get("level") == "WARN"])
    error_count = len([l for l in all_logs if l.get("level") == "ERROR"])
    debug_count = len([l for l in all_logs if l.get("level") == "DEBUG"])
    
    with col1:
        st.markdown(f'<div style="background: #00d98b22; padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #00d98b; font-weight: 600;">{info_count}</span> INFO</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background: #ffc10722; padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #ffc107; font-weight: 600;">{warn_count}</span> WARN</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background: #ff475722; padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #ff4757; font-weight: 600;">{error_count}</span> ERROR</div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div style="background: #a0a0a022; padding: 10px; border-radius: 8px; text-align: center;"><span style="color: #a0a0a0; font-weight: 600;">{debug_count}</span> DEBUG</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render logs
    for log in all_logs[:log_count]:
        render_log_entry(log)
    
    if not all_logs:
        st.warning("⚠️ Unable to connect to API. Make sure the FastAPI server is running on port 8000.")
        st.code("uvicorn api.main:app --reload --port 8000")

def execute_script(script_name: str, status_label: str):
    """Helper to execute a migration/rollback script and display output"""
    st.session_state.migration_running = True
    
    with st.status(status_label, expanded=True) as status:
        st.write("Initializing PowerShell environment...")
        
        try:
            # Path to the script relative to this app
            script_path = os.path.abspath(os.path.join(os.getcwd(), "..", "scripts", script_name))
            
            if not os.path.exists(script_path):
                st.error(f"Script not found at: {script_path}")
                status.update(label="Process Failed: Script Not Found", state="error")
            else:
                # Use subprocess to run the PowerShell script
                cmd_str = f'powershell.exe -ExecutionPolicy Bypass -File "{script_path}"'
                process = subprocess.Popen(
                    cmd_str,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True
                )
                
                output_container = st.empty()
                captured_output = ""
                
                for line in process.stdout:
                    captured_output += line
                    output_container.code(captured_output, language="powershell")
                
                process.wait()
                
                if process.returncode == 0:
                    status.update(label="Process Successful!", state="complete", expanded=False)
                    st.success(f"✅ Operations in {script_name} completed successfully.")
                else:
                    status.update(label=f"Process Failed (Exit Code: {process.returncode})", state="error")
                    st.error(f"Script exited with error code {process.returncode}")
        
        except Exception as e:
            st.error(f"⚠️ Error executing script: {str(e)}")
            status.update(label="System Error", state="error")
    
    st.session_state.migration_running = False

def render_migration_console():
    """Simplified Migration Control Center"""
    st.markdown('<div class="section-header">🚀 Core Migration Controls</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### ⚡ Actions")
        if st.button("� MIGRATE TO 5G", type="primary", use_container_width=True):
            execute_script("migrate.ps1", "🚀 Running Migration Script...")
        
        st.write("")
        if st.button("⏪ ROLLBACK TO 4G", use_container_width=True):
            execute_script("rollback_4g.ps1", "⏪ Running Rollback Script...")
        
        st.write("")
        if st.button("🗑️ PURGE ALL RESOURCES", use_container_width=True, help="Executes: kubectl delete all --all -n open5gs"):
            with st.status("🗑️ Purging all resources in open5gs namespace...", expanded=True) as status:
                try:
                    cmd = "kubectl delete all --all -n open5gs"
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        st.code(result.stdout)
                        st.success("✅ Namespace purged successfully.")
                        status.update(label="Purge Complete", state="complete")
                    else:
                        st.error(f"Error purging: {result.stderr}")
                        status.update(label="Purge Failed", state="error")
                except Exception as e:
                    st.error(f"System error: {str(e)}")
                    status.update(label="System Error", state="error")
        
        st.markdown("---")
        st.write("### 📊 Status Overview")
        # Quick summary metrics
        try:
            cmd = "kubectl get pods -n open5gs --no-headers"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                pods = result.stdout.strip().split("\n")
                if pods and pods[0]:
                    running = len([p for p in pods if "Running" in p])
                    total = len(pods)
                    st.metric("Running Pods", f"{running}/{total}")
                else:
                    st.metric("Running Pods", "0/0")
        except:
            pass

    with col2:
        st.write("### 📦 Kubernetes Pods")
        # Execute kubectl get pods
        try:
            cmd = "kubectl get pods -n open5gs -o wide"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                if not result.stdout.strip():
                    st.info("No pods found in 'open5gs' namespace.")
                else:
                    st.code(result.stdout, language="bash")
            else:
                st.error(f"Kubectl error: {result.stderr}")
        except Exception as e:
            st.warning(f"Failed to run kubectl: {str(e)}")

    # Mapping reference hidden in a small expander at the very bottom
    with st.expander("ℹ️ Help & Mapping Reference"):
        mappings = fetch_data("/api/component-mapping")
        if mappings:
            df = []
            for m in mappings.get("mappings", []):
                df.append({
                    "4G Source": m.get("4g") or "N/A",
                    "5G Destination": ", ".join(m.get("5g", [])),
                    "Function": m.get("description")
                })
            st.table(pd.DataFrame(df))


if __name__ == "__main__":
    main()
