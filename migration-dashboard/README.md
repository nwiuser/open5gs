# 4G/5G Core Migration Dashboard

A beautiful Streamlit UI with FastAPI backend for visualizing the migration from 4G EPC to 5G Core network.

## 📡 Features

- **Overview Dashboard**: Real-time migration progress and component status
- **4G Core Details**: Detailed view of EPC components (HSS, MME, SGW, PGW, PCRF)
- **5G Core Details**: Detailed view of 5GC components (AMF, SMF, UPF, NRF, UDM, UDR, AUSF, NSSF, PCF)
- **Migration Mapping**: Visual mapping showing how 4G components transform to 5G
- **Live Logs**: Real-time combined log viewer with filtering capabilities

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (Port 8501)               │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐  │
│  │   Overview   │ │  Component   │ │     Migration Map      │  │
│  │  Dashboard   │ │   Details    │ │   & Live Logs View     │  │
│  └──────────────┘ └──────────────┘ └────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                    │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐  │
│  │ 4G Endpoints │ │ 5G Endpoints │ │   Migration Endpoints  │  │
│  │ /api/4g/*    │ │ /api/5g/*    │ │    /api/migration/*    │  │
│  └──────────────┘ └──────────────┘ └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd migration-dashboard
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend

```bash
# From migration-dashboard directory
uvicorn api.main:app --reload --port 8000
```

### 3. Start Streamlit Frontend (in a new terminal)

```bash
# From migration-dashboard directory
streamlit run streamlit_app.py
```

### 4. Access the Dashboard

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 📋 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/4g/components` | Get all 4G EPC components status |
| `GET /api/5g/components` | Get all 5G Core components status |
| `GET /api/4g/logs/{component}` | Get logs for a specific 4G component |
| `GET /api/5g/logs/{component}` | Get logs for a specific 5G component |
| `GET /api/4g/logs/all` | Get combined logs from all 4G components |
| `GET /api/5g/logs/all` | Get combined logs from all 5G components |
| `GET /api/migration/status` | Get current migration status |
| `GET /api/component-mapping` | Get 4G to 5G component mapping |

## 🔧 Component Mapping (4G → 5G)

| 4G Component | 5G Component(s) | Description |
|--------------|-----------------|-------------|
| HSS | UDM, UDR, AUSF | Split into multiple 5G functions |
| MME | AMF | Mobility management |
| SGW-C | SMF | Session management |
| SGW-U | UPF | User plane handling |
| PGW-C | SMF | Session management |
| PGW-U | UPF | User plane handling |
| PCRF | PCF | Policy control |
| - | NRF | New: Service discovery |
| - | NSSF | New: Network slicing |

## 📸 Dashboard Views

1. **Overview**: High-level migration progress with side-by-side component comparison
2. **4G Core Details**: Detailed status cards for all EPC components with logs
3. **5G Core Details**: Detailed status cards for all 5GC components with logs
4. **Migration Mapping**: Visual representation of component evolution
5. **Live Logs**: Combined log viewer with filtering by core type and log level

## 🎨 Color Coding

### Component Status
- 🟢 **Running**: Component is healthy and operational
- 🟡 **Pending**: Component is starting or waiting
- 🔴 **Error**: Component has issues
- 🟣 **Migrating**: Component is being migrated

### Log Levels
- 🟢 **INFO**: Informational messages
- 🟡 **WARN**: Warning messages
- 🔴 **ERROR**: Error messages
- ⚪ **DEBUG**: Debug messages

## 📝 License

Part of the Open5GS Migration Project
