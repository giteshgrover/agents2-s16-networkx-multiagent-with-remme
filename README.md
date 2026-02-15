# Arcturus Session 16 Backend Share

This directory contains the backend code for the Arcturus platform, snapshot for Session 16.

## Contents

- `app.py`: Main FastAPI application entry point.
- `api.py`: API routes definition.
- `core/`: Core logic including the `Loop`, `AgentRunner`, `Memory`, and `CircuitBreaker`.
- `agents/`: Agent definitions (`Planner`, `Coder`, `Distiller`, etc.).
- `remme/`: The REMME (Re-Member-Me) user modeling and personalization system (5-Hub Architecture).
- `config/`: Configuration files (settings, defaults).
- `mcp_servers/`: Model Context Protocol servers.
- `routers/`: FastAPI routers for different endpoints.
- `tools/`: Utility tools and sandbox implementation.
- `prompts/`: System prompts for agents.
- `benchmarks/`: GAIA benchmarks and runners.
- `scripts/`: Utility scripts.
- `shared/`: Shared state and utilities.
- `memory/`: Memory context and store implementations.
- `ui/`: Backend visualization utilities (e.g., `visualizer.py` using Rich).
- `tests/`: Unit and integration tests.

## Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or follow instructions at: https://github.com/astral-sh/uv

2. **Install dependencies**:
   ```bash
   uv sync
   ```
   
   **What this does:**
   - Reads `pyproject.toml` to determine dependencies
   - Creates a virtual environment (if needed)
   - Installs all required packages (Gradio, FastAPI, NetworkX, etc.)
   - Uses `uv.lock` for reproducible installs

3. **Verify installation**:
   ```bash
   uv run python --version  # Should show Python 3.11+
   ```

## Usage

### Running the System

The system has two main components that need to run:

1. **API Server** (Backend) - Handles agent execution, MCP servers, and provides REST API
2. **UI Server** (Frontend) - Provides the web interface for interacting with the system

#### Option 1: CLI Mode (No UI)

Run the backend in command-line mode:

```bash
uv run python app.py
```

**What this does:**
- Starts MCP servers (Browser, RAG, Sandbox)
- Provides an interactive CLI for running queries
- No web interface - all interaction is through the terminal

#### Option 2: Web UI Mode (Recommended)

For the best experience, run both the API server and the UI:

**Terminal 1 - Start the API Server:**
```bash
uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**What this command does:**
- `uv run` - Runs the command using uv's managed Python environment
- `uvicorn` - ASGI server for FastAPI applications
- `api:app` - Points to the `app` object in `api.py`
- `--reload` - Enables auto-reload on code changes (development mode)
- `--host 0.0.0.0` - Makes the server accessible from any network interface
- `--port 8000` - Runs the API on port 8000

**Terminal 2 - Start the UI:**
```bash
uv run python app.py --ui
```

**What this command does:**
- `uv run` - Runs using uv's managed Python environment
- `python app.py` - Executes the main application file
- `--ui` - Launches the web UI instead of CLI mode

**For Development (with auto-reload):**

Option 1: Using the development script (Recommended):
```bash
uv run python scripts/dev_ui.py
```

**What this does:**
- Watches all Python files in the `ui/` directory
- Automatically restarts the UI server when files change
- Full process restart ensures all changes are applied

Option 2: Using the --reload flag:
```bash
uv run python app.py --ui --reload
```

**What `--reload` does:**
- Attempts to use Gradio's built-in file watching
- May require manual browser refresh for some changes
- Less reliable than the dev script approach

### Accessing the UI

Once both servers are running:
- **UI**: Open `http://localhost:7860` in your browser
- **API**: Available at `http://localhost:8000`
- **API Docs**: Available at `http://localhost:8000/docs` (Swagger UI)

### UI Features

The advanced UI provides:

1. **Chat Panel** - Run queries and see real-time execution graphs
2. **Chat History** - View past queries and their execution graphs
3. **Remme Panel** - View stored memories and user preferences
4. **MCP Servers Panel** - View configured MCP servers and their tools
5. **Settings Panel** - View and manage system configuration

**Graph Visualization:**
- Color-coded nodes: 🟢 Green (completed), 🟡 Yellow (running), 🔴 Red (failed), ⚪ Gray (pending)
- Hierarchical layout showing execution flow
- Node selection to view detailed information

### Quick Start Commands Summary

```bash
# Terminal 1: Start API server with auto-reload
uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start UI with auto-reload (development)
uv run python app.py --ui --reload

# Terminal 2: Start UI without auto-reload (production)
uv run python app.py --ui
```

### Troubleshooting

**UI not connecting to API:**
- Ensure API server is running on port 8000
- Check that you see "🚀 API Starting up..." in the API server terminal
- Verify no firewall is blocking port 8000

**Port already in use:**
- Change the port: `uv run uvicorn api:app --reload --host 0.0.0.0 --port 8001`
- Update `API_BASE` in `ui/advanced_ui.py` if you change the API port

**Graph not displaying:**
- Check browser console (F12) for JavaScript errors
- Ensure graph data is being retrieved (check terminal logs)
- Try clicking the "🔄 Refresh" button

**Auto-reload not working:**
- Make sure you used `--reload` flag
- Only `ui/advanced_ui.py` is watched for changes
- Other files require manual restart

## Notes

- This package excludes UI frontend code (`platform-frontend`) and user data (`data/`, `Notes/`).
- `config/settings.json` serves as the primary configuration.
- The UI requires the API server to be running on port 8000.
- For production, remove `--reload` flags to disable auto-reload.
- MCP servers are automatically started by the API server on startup.
