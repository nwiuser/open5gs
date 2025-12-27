"""
FastAPI Backend for 4G/5G Core Migration Dashboard
Provides endpoints to fetch logs and status of core network components
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import random
import asyncio

app = FastAPI(
    title="4G/5G Core Migration API",
    description="API for monitoring 4G to 5G core network migration",
    version="1.0.0"
)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== Data Models ==============

class ComponentStatus(BaseModel):
    name: str
    status: str  # "running", "pending", "error", "migrating"
    pod_count: int
    cpu_usage: float
    memory_usage: float
    last_updated: datetime

class LogEntry(BaseModel):
    timestamp: datetime
    component: str
    level: str  # "INFO", "WARN", "ERROR", "DEBUG"
    message: str
    core_type: str  # "4G" or "5G"

class MigrationStatus(BaseModel):
    phase: str
    progress: float
    started_at: Optional[datetime]
    estimated_completion: Optional[datetime]
    active_subscribers_migrated: int
    total_subscribers: int

# ============== 4G Core Components ==============
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

# ============== 5G Core Components ==============
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

# ============== Simulated Data Generators ==============

def generate_component_status(name: str, core_type: str) -> ComponentStatus:
    """Generate simulated component status"""
    statuses = ["running", "running", "running", "pending", "migrating"]
    return ComponentStatus(
        name=name,
        status=random.choice(statuses),
        pod_count=random.randint(1, 3),
        cpu_usage=round(random.uniform(5, 85), 2),
        memory_usage=round(random.uniform(10, 70), 2),
        last_updated=datetime.now()
    )

def generate_log_entries(component: str, core_type: str, count: int = 10) -> List[LogEntry]:
    """Generate simulated log entries for a component"""
    levels = ["INFO", "INFO", "INFO", "WARN", "DEBUG", "ERROR"]
    
    log_messages = {
        "4G": {
            "hss": [
                "Diameter connection established",
                "Processing authentication request for IMSI",
                "Subscriber profile updated successfully",
                "HSS binding to S6a interface",
                "Authentication vector generated",
            ],
            "mme": [
                "S1AP connection from eNodeB accepted",
                "UE attach request received",
                "Initial context setup completed",
                "Handover procedure initiated",
                "Tracking area update processed",
            ],
            "sgwc": [
                "GTP-C tunnel created",
                "Bearer context modification completed",
                "Session created for UE",
                "S11 interface message received",
                "Path management timer reset",
            ],
            "sgwu": [
                "GTP-U tunnel established",
                "User plane packet forwarding active",
                "Downlink data notification sent",
                "Buffer size threshold reached",
                "PFCP session established",
            ],
            "pgwc": [
                "PDN connection request processed",
                "IP address allocated from pool",
                "Default bearer created",
                "QoS policy applied",
                "S5/S8 session established",
            ],
            "pgwu": [
                "User plane rules installed",
                "NAT translation configured",
                "Traffic shaping policy active",
                "Packet inspection completed",
                "Data volume report generated",
            ],
            "pcrf": [
                "Policy decision for session",
                "Diameter Gx message processed",
                "Charging rules updated",
                "QoS modification request",
                "Session binding created",
            ],
            "mongodb": [
                "Connection pool active",
                "Collection query executed",
                "Document indexed successfully",
                "Replica set heartbeat",
                "Write operation completed",
            ],
        },
        "5G": {
            "amf": [
                "NAS registration request received",
                "NGAP connection from gNodeB",
                "5G-GUTI assigned to UE",
                "N2 handover procedure started",
                "PDU session establishment initiated",
            ],
            "smf": [
                "PDU session created for UE",
                "N4 session established with UPF",
                "IP address allocated from DNN pool",
                "QoS flow created",
                "Session modification completed",
            ],
            "upf": [
                "PFCP association established",
                "PDR/FAR rules installed",
                "N3/N9 tunnel created",
                "User plane packet processing active",
                "Usage reporting threshold reached",
            ],
            "nrf": [
                "NF registration accepted",
                "Service discovery response sent",
                "NF profile updated",
                "Subscription notification triggered",
                "NF heartbeat received",
            ],
            "udm": [
                "Subscription retrieval completed",
                "Authentication credential fetched",
                "Access management info updated",
                "SDM subscription created",
                "SUPI-SUCI mapping processed",
            ],
            "udr": [
                "Data storage operation completed",
                "Subscription data retrieved",
                "Policy data updated",
                "Application context stored",
                "Exposure data accessed",
            ],
            "ausf": [
                "5G-AKA authentication initiated",
                "Auth vector request to UDM",
                "SUCI de-concealment completed",
                "EAP-AKA' procedure started",
                "Authentication result confirmed",
            ],
            "nssf": [
                "Slice selection completed",
                "NSI information retrieved",
                "S-NSSAI mapped to NRF",
                "Allowed NSSAI configured",
                "Network slice availability checked",
            ],
            "pcf": [
                "AM policy association created",
                "SM policy decision sent",
                "UE policy container updated",
                "Access and mobility policy applied",
                "Session binding information updated",
            ],
        }
    }
    
    entries = []
    base_messages = log_messages.get(core_type, {}).get(component, ["Generic log entry"])
    
    for i in range(count):
        entries.append(LogEntry(
            timestamp=datetime.now(),
            component=component,
            level=random.choice(levels),
            message=random.choice(base_messages),
            core_type=core_type
        ))
    
    return entries

# ============== API Endpoints ==============

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "4G/5G Core Migration Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "4g_components": "/api/4g/components",
            "5g_components": "/api/5g/components",
            "4g_logs": "/api/4g/logs/{component}",
            "5g_logs": "/api/5g/logs/{component}",
            "migration_status": "/api/migration/status",
        }
    }

@app.get("/api/4g/components", response_model=Dict[str, dict])
async def get_4g_components():
    """Get all 4G core components information"""
    result = {}
    for name, info in COMPONENTS_4G.items():
        status = generate_component_status(name, "4G")
        result[name] = {
            **info,
            "status": status.status,
            "pod_count": status.pod_count,
            "cpu_usage": status.cpu_usage,
            "memory_usage": status.memory_usage,
            "last_updated": status.last_updated.isoformat()
        }
    return result

@app.get("/api/5g/components", response_model=Dict[str, dict])
async def get_5g_components():
    """Get all 5G core components information"""
    result = {}
    for name, info in COMPONENTS_5G.items():
        status = generate_component_status(name, "5G")
        result[name] = {
            **info,
            "status": status.status,
            "pod_count": status.pod_count,
            "cpu_usage": status.cpu_usage,
            "memory_usage": status.memory_usage,
            "last_updated": status.last_updated.isoformat()
        }
    return result

@app.get("/api/4g/logs/{component}", response_model=List[LogEntry])
async def get_4g_logs(component: str, count: int = 20):
    """Get logs for a specific 4G component"""
    if component not in COMPONENTS_4G:
        raise HTTPException(status_code=404, detail=f"Component '{component}' not found in 4G core")
    return generate_log_entries(component, "4G", count)

@app.get("/api/5g/logs/{component}", response_model=List[LogEntry])
async def get_5g_logs(component: str, count: int = 20):
    """Get logs for a specific 5G component"""
    if component not in COMPONENTS_5G:
        raise HTTPException(status_code=404, detail=f"Component '{component}' not found in 5G core")
    return generate_log_entries(component, "5G", count)

@app.get("/api/migration/status", response_model=MigrationStatus)
async def get_migration_status():
    """Get current migration status"""
    phases = ["Preparation", "Data Sync", "Testing", "Cutover", "Validation"]
    return MigrationStatus(
        phase=random.choice(phases),
        progress=round(random.uniform(0, 100), 2),
        started_at=datetime.now(),
        estimated_completion=datetime.now(),
        active_subscribers_migrated=random.randint(1000, 50000),
        total_subscribers=50000
    )

@app.get("/api/4g/logs/all", response_model=List[LogEntry])
async def get_all_4g_logs(count: int = 50):
    """Get combined logs from all 4G components"""
    all_logs = []
    per_component = max(1, count // len(COMPONENTS_4G))
    for component in COMPONENTS_4G.keys():
        all_logs.extend(generate_log_entries(component, "4G", per_component))
    return sorted(all_logs, key=lambda x: x.timestamp, reverse=True)[:count]

@app.get("/api/5g/logs/all", response_model=List[LogEntry])
async def get_all_5g_logs(count: int = 50):
    """Get combined logs from all 5G components"""
    all_logs = []
    per_component = max(1, count // len(COMPONENTS_5G))
    for component in COMPONENTS_5G.keys():
        all_logs.extend(generate_log_entries(component, "5G", per_component))
    return sorted(all_logs, key=lambda x: x.timestamp, reverse=True)[:count]

@app.get("/api/component-mapping")
async def get_component_mapping():
    """Get mapping between 4G and 5G components for migration visualization"""
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
