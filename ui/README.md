# Advanced UI for S16 NetworkX Multi-Agent System

## Overview

This is a modern, feature-rich UI for the S16 NetworkX Multi-Agent System. It provides a comprehensive interface for interacting with the agent system, viewing execution graphs, managing memories, and configuring settings.

## Features

### 1. Chat Panel (Default)
- **Query Input**: Enter queries to execute agent workflows
- **Real-time Graph Visualization**: Interactive graph showing agent execution flow
  - **Color-coded nodes**:
    - 🟢 Green: Completed nodes
    - 🟡 Yellow: Running nodes
    - 🔴 Red: Failed nodes
    - ⚪ Gray: Pending nodes
  - **Node Selection**: Use the dropdown to select nodes and view details
- **Node Details Panel**: Shows agent prompt, input/output snippets, execution time, cost, etc.
- **Final Output Panel**: Displays the formatted markdown output with maximize option
- **Auto-refresh**: Graph updates every 2 seconds during execution

### 2. Chat History Panel
- **Past Queries List**: View all previous execution sessions
- **Graph Visualization**: Click on any past query to view its execution graph
- **Node Details**: Select nodes from historical runs to view their details
- **Final Output**: View the output from any past execution

### 3. Remme Panel
- **Memories Tab**: View all stored memories with categories and sources
- **Preferences Tab**: View user preferences extracted from conversations

### 4. MCP Servers Panel
- **Server Information**: View all configured MCP servers
- **Tool Details**: See available tools for each server
- **Connection Status**: Check which servers are connected

### 5. Settings Panel
- **System Configuration**: View and manage system settings
- **Agent Configuration**: View agent-related settings

## Usage

### Prerequisites

1. **API Server**: The UI requires the FastAPI server to be running on `http://localhost:8000`

   ```bash
   # Using uv (recommended)
   uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000

   # Or using uv with Python directly
   uv run python api.py
   ```

2. **MCP Servers**: Ensure MCP servers are configured and running (handled by the API server)

### Launching the UI

```bash
# Launch the advanced UI using uv
uv run python app.py --ui
```

The UI will be available at `http://localhost:7860`

### Using the UI

1. **Running a Query**:
   - Navigate to the Chat panel (default)
   - Enter your query in the text box
   - Click "🚀 Run Query"
   - Watch the graph update in real-time as agents execute
   - Select nodes from the dropdown to view details
   - View the final output in the output panel

2. **Viewing History**:
   - Click "📜 Chat History" in the sidebar
   - Click on any query in the list to view its graph
   - Select nodes to view their details

3. **Managing Remme**:
   - Click "🧠 Remme" in the sidebar
   - View memories and preferences
   - Refresh to get latest data

4. **MCP Servers**:
   - Click "🔌 MCP Servers" in the sidebar
   - View server status and available tools

5. **Settings**:
   - Click "⚙️ Settings" in the sidebar
   - View system configuration

## Architecture

The UI is built using:
- **Gradio**: For the web interface framework
- **vis.js Network**: For graph visualization
- **FastAPI**: Backend API for data access
- **Real-time Polling**: Updates graph every 2 seconds during execution

## API Endpoints Used

- `POST /runs` - Create new execution
- `GET /runs` - List all runs
- `GET /runs/{run_id}` - Get run graph data
- `GET /remme/memories` - Get Remme memories
- `GET /remme/preferences` - Get Remme preferences
- `GET /mcp/servers` - Get MCP server information
- `GET /settings` - Get system settings

## Troubleshooting

1. **UI not connecting to API**:
   - Ensure API server is running on port 8000
   - Check API_BASE URL in `ui/advanced_ui.py` if using different port

2. **Graph not updating**:
   - Check browser console for JavaScript errors
   - Ensure vis.js is loading (check network tab)
   - Try refreshing the graph manually

3. **Node selection not working**:
   - Use the dropdown selector instead of clicking directly on graph
   - Ensure graph data has loaded (check if nodes appear)

4. **No data in panels**:
   - Click refresh buttons to reload data
   - Check API server logs for errors
   - Ensure MCP servers are running

## Future Enhancements

- Direct node clicking on graph (requires iframe message passing)
- Real-time WebSocket updates instead of polling
- Export graphs as images
- Search/filter in history
- Edit settings directly from UI
- Agent performance metrics visualization

