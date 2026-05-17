# City Info MCP Server

A Python Model Context Protocol (MCP) server that provides city data from the free [Open-Meteo API](https://open-meteo.com). Uses FastMCP with HTTP/SSE transport for easy local deployment and testing.

## Features

- Provide City information like:
  City Name
  City Admin Area
  City Longitue etc.

## Prerequisites

- Python 3.10 or higher
- Node.js (for MCP Inspector, optional)
- pip (Python package manager)

## Local Deployment Guide

### Step 1: Setup Python Environment

```bash
# Navigate to project directory
cd /path/to/city-info

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start the MCP Server

```bash
# Make sure venv is activated
source venv/bin/activate

# Run the server
python server.py
```

**Expected output:**
```
Starting Weather MCP Server...
HTTP/SSE endpoint: http://localhost:8000

Connect with MCP Inspector:
  npx @modelcontextprotocol/inspector http://localhost:8000

INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Connect with MCP Inspector

In a **new terminal**, run:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000
```

The MCP Inspector UI will open in your browser. Check the terminal output for the port number (usually `http://localhost:3000` or `http://localhost:6274`)

## Testing the Server

### Using MCP Inspector UI

**Option 1: Test Tools**
1. Open MCP Inspector in browser
2. Go to **Tools** tab
3. Select `get_city_info`
4. Enter city name (e.g., "New York")
5. Click **Call tool**


### Using curl (Command Line)

```bash
# Test server is running
curl http://localhost:8000/

# The actual MCP communication happens via SSE on /messages/ endpoint
# This is handled by MCP clients like Inspector automatically
```

## What It Does

### Tools (Callable Functions)
- **`get_current_weather(city)`** - Get real-time weather conditions
  - Temperature, "feels like" temperature
  - Weather condition description
  - Wind speed, humidity, timezone
  
- **`get_forecast(city)`** - Get 7-day weather forecast
  - Daily min/max temperatures
  - Weather conditions
  - Precipitation amounts


## Architecture

```
HTTP Server (localhost:8000)
│
└── FastMCP Server
    ├── SSE Endpoint (/messages/)
    │   └── Bidirectional communication with MCP Inspector
    │
    ├── Tools
    │   ├── get_city_info(city)
    │
    └── HTTP Client (httpx)
        └── Open-Meteo API (geocoding-api.open-meteo.com)
```

## Technical Details

### Transport Protocol
- **Type**: HTTP/SSE (Server-Sent Events)
- **Port**: 8000
- **Endpoint**: http://localhost:8000
- **Implementation**: FastMCP's built-in SSE support with Uvicorn

### Why HTTP/SSE?
- ✅ Network-accessible (not limited to stdio)
- ✅ Works with remote machines and cloud deployments
- ✅ Native browser support (used by MCP Inspector)
- ✅ Handles multiple concurrent connections
- ✅ Cleaner code (FastMCP manages complexity)

## Troubleshooting

### "Address already in use" Error
Port 8000 is already in use. Kill the existing process:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Server won't start
1. Verify Python 3.10+ is installed: `python --version`
2. Check all dependencies installed: `pip list | grep mcp`
3. Check port 8000 is free
4. Review error message in console

### MCP Inspector won't connect
1. Verify server is running (see startup message)
2. Check http://localhost:8000 in browser (should show connection)
3. Ensure Node.js is installed: `node --version`
4. Try clearing MCP Inspector cache and refreshing


## Project Files

| File | Purpose |
|------|---------|
| `server.py` | Entry point - starts HTTP/SSE server with Uvicorn |
| `city_info_http.py` | FastMCP server definition with tools and resources |
| `requirements.txt` | Python dependencies (mcp, httpx, uvicorn, starlette) |
| `EXAMPLES.md` | Detailed usage examples and integration guide |
| `README.md` | This file |
| `.gitignore` | Git ignore rules |

## Development

### Adding a New Tool

Edit `city_info_http.py`:
```python
@mcp.tool()
async def get_new_tool(parameter: str) -> str:
    """Tool description"""
    # Implementation
    return "result"
```


Restart the server to see changes.


## Docker Deployment

Run the server as a Docker container and test it with MCP Inspector on your host machine.


### Step 1: Build the Docker Image

```bash
# From the project root directory
docker build -t weather-mcp-server .
```

### Step 2: Run the Container

```bash
docker run -d \
  --name weather-mcp \
  -p 8000:8000 \
  weather-mcp-server
```

**Verify the container is running:**
```bash
docker ps
docker logs weather-mcp
```

### Step 3: Test with MCP Inspector (on Host)

In a terminal on your host machine, run:

```bash
npx @modelcontextprotocol/inspector http://localhost:8000
```

The MCP Inspector connects to the container via the mapped port. Open the URL shown in the terminal output (typically `http://localhost:6274`) and use the **Tools** and **Resources** tabs to interact with the server.

### Troubleshooting Docker

**Container exits immediately:**
```bash
docker logs weather-mcp
```
Check the logs for Python errors or missing dependencies.

**MCP Inspector can't connect:**
- Confirm the container is running: `docker ps`
- Confirm port mapping is active: `docker port weather-mcp`
- Test the endpoint directly: `curl http://localhost:8000/`

**Port 8000 already in use on the host:**
Map to a different host port — update both the `docker run` flag and the Inspector URL:
```bash
docker run -d --name weather-mcp -p 8080:8000 weather-mcp-server
npx @modelcontextprotocol/inspector http://localhost:8080
```

