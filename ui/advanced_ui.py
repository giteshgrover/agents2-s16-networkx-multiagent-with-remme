"""
Advanced UI for S16 NetworkX Multi-Agent System
Features:
- Sidebar navigation (Chat, Chat History, Remme, MCP Servers, Settings)
- Real-time graph visualization with color-coded nodes
- Node details panel
- Markdown output display
"""

import gradio as gr
import json
import requests
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import pandas as pd

# API base URL
API_BASE = "http://localhost:8000"

# Custom CSS for modern styling
CUSTOM_CSS = """
/* Modern UI Styling */
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
}

.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.sidebar-item {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 4px 0;
    transition: all 0.2s;
    width: 100%;
    text-align: left;
}

.sidebar-item:hover {
    background: var(--bg-primary) !important;
}

.graph-container {
    width: 100%;
    height: 600px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-primary);
    overflow: hidden;
}

.node-details {
    background: var(--bg-secondary);
    padding: 16px;
    border-radius: 8px;
    max-height: 500px;
    overflow-y: auto;
}

.output-panel {
    background: var(--bg-secondary);
    padding: 16px;
    border-radius: 8px;
    max-height: 600px;
    overflow-y: auto;
}
"""

# Graph visualization HTML template - Simple CSS-based approach
GRAPH_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            padding: 20px; 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8fafc;
        }
        .graph-container { 
            width: 100%; 
            min-height: 400px;
            background: white;
            border-radius: 8px;
            padding: 20px;
            overflow: auto;
        }
        .graph-node {
            display: inline-block;
            margin: 10px;
            padding: 12px 20px;
            border-radius: 8px;
            border: 2px solid;
            font-weight: 600;
            font-size: 14px;
            text-align: center;
            min-width: 150px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .graph-node:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .node-completed { background: #10b981; border-color: #059669; color: white; }
        .node-running { background: #f59e0b; border-color: #d97706; color: white; }
        .node-failed { background: #ef4444; border-color: #dc2626; color: white; }
        .node-pending { background: #9ca3af; border-color: #6b7280; color: white; }
        .node-stale { background: #d1d5db; border-color: #9ca3af; color: #1f2937; }
        .graph-level {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            position: relative;
        }
        .graph-arrow {
            text-align: center;
            color: #94a3b8;
            font-size: 24px;
            margin: 5px 0;
        }
        .node-label {
            display: block;
            font-size: 12px;
            margin-top: 4px;
            opacity: 0.9;
        }
        .empty-graph {
            text-align: center;
            padding: 40px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="graph-container" id="graph-container">
        <div class="empty-graph">No graph data available. Run a query to see the execution graph.</div>
    </div>
</body>
</html>
"""


class AdvancedUI:
    def __init__(self):
        self.current_run_id: Optional[str] = None
        
    def get_runs(self) -> List[Dict]:
        """Get list of past runs"""
        try:
            response = requests.get(f"{API_BASE}/runs", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching runs: {e}")
        return []
    
    def get_run_graph(self, run_id: str) -> Optional[Dict]:
        """Get graph data for a run"""
        if not run_id:
            return None
        try:
            response = requests.get(f"{API_BASE}/runs/{run_id}", timeout=5)
            if response.status_code == 200:
                return response.json().get("graph")
        except Exception as e:
            print(f"Error fetching graph: {e}")
        return None
    
    def create_run(self, query: str) -> Optional[str]:
        """Create a new run and return run_id"""
        if not query or not query.strip():
            return None
        try:
            response = requests.post(
                f"{API_BASE}/runs",
                json={"query": query},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("id")
        except Exception as e:
            print(f"Error creating run: {e}")
        return None
    
    def get_remme_memories(self) -> List[Dict]:
        """Get Remme memories"""
        try:
            response = requests.get(f"{API_BASE}/remme/memories", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching Remme memories: {e}")
        return []
    
    def get_remme_preferences(self) -> Dict:
        """Get Remme preferences"""
        try:
            response = requests.get(f"{API_BASE}/remme/preferences", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching Remme preferences: {e}")
        return {}
    
    def get_mcp_servers(self) -> Dict:
        """Get MCP server information"""
        try:
            response = requests.get(f"{API_BASE}/mcp/servers", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching MCP servers: {e}")
        return {}
    
    def get_settings(self) -> Dict:
        """Get current settings"""
        try:
            response = requests.get(f"{API_BASE}/settings", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("settings", {})
        except Exception as e:
            print(f"Error fetching settings: {e}")
        return {}
    
    def get_final_output(self, run_id: str) -> str:
        """Extract final output from a run"""
        graph_data = self.get_run_graph(run_id)
        if not graph_data:
            return "No output available."
        
        # Find FormatterAgent or SummarizerAgent output
        for node in graph_data.get("nodes", []):
            node_data = node.get("data", {})
            agent_type = node_data.get("type", "")
            status = node_data.get("status", "")
            
            if status == "completed" and agent_type in ["FormatterAgent", "SummarizerAgent"]:
                output = node_data.get("output", "")
                if output:
                    try:
                        if isinstance(output, str):
                            try:
                                parsed = json.loads(output)
                                if isinstance(parsed, dict):
                                    markdown = parsed.get("markdown_report") or parsed.get("formatted_report") or parsed.get("final_answer")
                                    if markdown:
                                        return markdown
                                    return json.dumps(parsed, indent=2)
                            except:
                                return output
                        return str(output)
                    except:
                        return str(output)
        
        # Fallback: get any completed node output
        for node in graph_data.get("nodes", []):
            node_data = node.get("data", {})
            if node_data.get("status") == "completed":
                output = node_data.get("output", "")
                if output:
                    return str(output)[:2000]  # Limit length
        
        return "No output available yet."
    
    def format_node_details(self, node_data: Dict) -> str:
        """Format node details for display"""
        if not node_data:
            return "No node selected."
        
        details = []
        details.append(f"## {node_data.get('type', 'Unknown Agent')}")
        details.append(f"**Status:** `{node_data.get('status', 'unknown')}`")
        details.append(f"**Node ID:** `{node_data.get('id', 'N/A')}`")
        details.append("")
        
        if node_data.get('description'):
            details.append(f"**Description:**\n{node_data.get('description')}")
            details.append("")
        
        if node_data.get('prompt'):
            prompt = node_data.get('prompt', '')
            if len(prompt) > 500:
                prompt = prompt[:500] + "..."
            details.append(f"**Agent Prompt:**\n```\n{prompt}\n```")
            details.append("")
        
        reads = node_data.get('reads', [])
        if reads:
            details.append(f"**Reads:** `{', '.join(reads)}`")
        
        writes = node_data.get('writes', [])
        if writes:
            details.append(f"**Writes:** `{', '.join(writes)}`")
        
        if node_data.get('cost', 0) > 0:
            details.append(f"**Cost:** ${node_data.get('cost', 0):.6f}")
        
        if node_data.get('execution_time', 0) > 0:
            details.append(f"**Execution Time:** {node_data.get('execution_time', 0):.2f}s")
        
        if node_data.get('error'):
            details.append(f"\n**Error:**\n```\n{node_data.get('error')}\n```")
        
        output = node_data.get('output', '')
        if output:
            output_str = str(output)
            if len(output_str) > 1000:
                output_str = output_str[:1000] + "..."
            details.append(f"\n**Output Snippet:**\n```\n{output_str}\n```")
        
        return "\n".join(details)
    
    def build_graph_html(self, graph_data: Optional[Dict]) -> str:
        """Build HTML with graph data using simple CSS-based visualization"""
        if not graph_data:
            print("Warning: No graph data provided to build_graph_html")
            return GRAPH_HTML_TEMPLATE
        
        # Validate graph data structure
        if not isinstance(graph_data, dict) or 'nodes' not in graph_data:
            print(f"Warning: Invalid graph data structure: {type(graph_data)}")
            return GRAPH_HTML_TEMPLATE
        
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        print(f"Building graph HTML with {len(nodes)} nodes and {len(edges)} edges")
        
        if not nodes:
            return GRAPH_HTML_TEMPLATE
        
        # Build a simple hierarchical layout
        # Group nodes by level (simple approach: use topological order)
        node_map = {node['id']: node for node in nodes}
        edge_map = {}
        for edge in edges:
            source = edge.get('source', edge.get('from'))
            target = edge.get('target', edge.get('to'))
            if source not in edge_map:
                edge_map[source] = []
            edge_map[source].append(target)
        
        # Simple level assignment (BFS)
        levels = {}
        visited = set()
        queue = []
        
        # Find root nodes (nodes with no incoming edges)
        all_targets = set()
        for targets in edge_map.values():
            all_targets.update(targets)
        
        root_nodes = [n['id'] for n in nodes if n['id'] not in all_targets]
        if not root_nodes:
            root_nodes = [nodes[0]['id']] if nodes else []
        
        # Assign levels
        for root in root_nodes:
            queue.append((root, 0))
        
        while queue:
            node_id, level = queue.pop(0)
            if node_id in visited:
                continue
            visited.add(node_id)
            levels[node_id] = level
            
            # Add children to queue
            if node_id in edge_map:
                for child in edge_map[node_id]:
                    if child not in visited:
                        queue.append((child, level + 1))
        
        # Group nodes by level
        nodes_by_level = {}
        for node_id, level in levels.items():
            if level not in nodes_by_level:
                nodes_by_level[level] = []
            nodes_by_level[level].append(node_id)
        
        # Build HTML
        html_parts = ['<div class="graph-container">']
        
        for level in sorted(nodes_by_level.keys()):
            html_parts.append('<div class="graph-level">')
            for node_id in nodes_by_level[level]:
                node = node_map.get(node_id, {})
                node_data = node.get('data', {})
                status = node_data.get('status', 'pending')
                agent_type = node_data.get('type', node_data.get('label', node_id))
                
                status_class = f'node-{status}'
                html_parts.append(f'''
                    <div class="graph-node {status_class}" title="{node_id} - {status}">
                        <div>{agent_type}</div>
                        <div class="node-label">{node_id}</div>
                    </div>
                ''')
            html_parts.append('</div>')
            
            # Add arrow between levels
            if level < max(nodes_by_level.keys()):
                html_parts.append('<div class="graph-arrow">↓</div>')
        
        html_parts.append('</div>')
        
        # Replace the container content
        html = GRAPH_HTML_TEMPLATE.replace(
            '<div class="graph-container" id="graph-container">\n        <div class="empty-graph">No graph data available. Run a query to see the execution graph.</div>\n    </div>',
            ''.join(html_parts)
        )
        
        return html
    
    def build_ui(self):
        """Build the complete UI"""
        with gr.Blocks() as demo:
            gr.Markdown("# 🤖 S16 NetworkX Multi-Agent System", elem_classes="header")
            
            with gr.Row():
                # Left Sidebar
                with gr.Column(scale=1, min_width=200):
                    gr.Markdown("### Navigation")
                    
                    chat_btn = gr.Button("💬 Chat", variant="primary", size="lg", elem_classes="sidebar-item")
                    history_btn = gr.Button("📜 Chat History", variant="secondary", size="lg", elem_classes="sidebar-item")
                    remme_btn = gr.Button("🧠 Remme", variant="secondary", size="lg", elem_classes="sidebar-item")
                    mcp_btn = gr.Button("🔌 MCP Servers", variant="secondary", size="lg", elem_classes="sidebar-item")
                    settings_btn = gr.Button("⚙️ Settings", variant="secondary", size="lg", elem_classes="sidebar-item")
                
                # Main Content Area
                with gr.Column(scale=4):
                    # Chat Panel (Default)
                    with gr.Group(visible=True) as chat_panel:
                        with gr.Row():
                            with gr.Column(scale=2):
                                query_input = gr.Textbox(
                                    label="Enter your query",
                                    placeholder="What is the price of silver today in Bangalore?",
                                    lines=3
                                )
                                submit_btn = gr.Button("🚀 Run Query", variant="primary")
                                
                                # Graph visualization
                                graph_html = gr.HTML(
                                    value=GRAPH_HTML_TEMPLATE,
                                    elem_classes="graph-container",
                                    label="Execution Graph"
                                )
                                
                                # Node selector
                                node_selector = gr.Dropdown(
                                    choices=[],
                                    label="Select Node to View Details",
                                    interactive=True,
                                    allow_custom_value=True
                                )
                                
                                # Hidden state for run_id and graph_data
                                run_id_state = gr.State(value="")
                                graph_data_state = gr.State(value={})
                                
                            with gr.Column(scale=1):
                                gr.Markdown("### Node Details")
                                node_details = gr.Markdown("Select a node from the dropdown to view details", elem_classes="node-details")
                                
                                gr.Markdown("### Final Output")
                                final_output = gr.Markdown("Output will appear here after execution completes", elem_classes="output-panel")
                                
                                with gr.Row():
                                    maximize_output_btn = gr.Button("🔍 Maximize", variant="secondary", size="sm")
                                    refresh_graph_btn = gr.Button("🔄 Refresh", variant="secondary", size="sm")
                    
                    # Chat History Panel
                    with gr.Group(visible=False) as history_panel:
                        gr.Markdown("### Chat History")
                        with gr.Row():
                            load_history_btn = gr.Button("🔄 Refresh History", variant="primary")
                        
                        history_list = gr.Dataframe(
                            headers=["ID", "Query", "Date", "Status"],
                            label="Past Queries (Click to view)",
                            interactive=True,
                            type="pandas",
                            wrap=True
                        )
                        
                        with gr.Row():
                            with gr.Column(scale=2):
                                history_graph_html = gr.HTML(
                                    value=GRAPH_HTML_TEMPLATE,
                                    elem_classes="graph-container",
                                    label="Execution Graph"
                                )
                                
                                # History node selector
                                history_node_selector = gr.Dropdown(
                                    choices=[],
                                    label="Select Node to View Details",
                                    interactive=True,
                                    allow_custom_value=True
                                )
                                
                            with gr.Column(scale=1):
                                history_node_details = gr.Markdown("Select a node from the dropdown to view details", elem_classes="node-details")
                                history_final_output = gr.Markdown("", elem_classes="output-panel")
                        
                        selected_run_id = gr.State(value="")
                        history_graph_data_state = gr.State(value={})
                    
                    # Remme Panel
                    with gr.Group(visible=False) as remme_panel:
                        gr.Markdown("### 🧠 Remme - Memory & Preferences")
                        
                        with gr.Tabs():
                            with gr.Tab("Memories"):
                                with gr.Row():
                                    refresh_memories_btn = gr.Button("🔄 Refresh Memories", variant="primary")
                                remme_memories = gr.Dataframe(
                                    headers=["ID", "Text", "Category", "Source"],
                                    label="Stored Memories",
                                    interactive=False,
                                    wrap=True
                                )
                            
                            with gr.Tab("Preferences"):
                                with gr.Row():
                                    refresh_preferences_btn = gr.Button("🔄 Refresh Preferences", variant="primary")
                                remme_preferences = gr.JSON(
                                    label="User Preferences"
                                )
                    
                    # MCP Servers Panel
                    with gr.Group(visible=False) as mcp_panel:
                        gr.Markdown("### 🔌 MCP Servers")
                        with gr.Row():
                            refresh_mcp_btn = gr.Button("🔄 Refresh MCP Servers", variant="primary")
                        mcp_servers_info = gr.JSON(
                            label="Configured MCP Servers"
                        )
                    
                    # Settings Panel
                    with gr.Group(visible=False) as settings_panel:
                        gr.Markdown("### ⚙️ Settings")
                        with gr.Row():
                            refresh_settings_btn = gr.Button("🔄 Refresh Settings", variant="primary")
                        settings_info = gr.JSON(
                            label="System Settings"
                        )
            
            # Panel visibility controls
            def show_chat():
                return (
                    gr.Group(visible=True),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False)
                )
            
            def show_history():
                return (
                    gr.Group(visible=False),
                    gr.Group(visible=True),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False)
                )
            
            def show_remme():
                return (
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=True),
                    gr.Group(visible=False),
                    gr.Group(visible=False)
                )
            
            def show_mcp():
                return (
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=True),
                    gr.Group(visible=False)
                )
            
            def show_settings():
                return (
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=False),
                    gr.Group(visible=True)
                )
            
            # Event handlers for navigation
            chat_btn.click(show_chat, outputs=[chat_panel, history_panel, remme_panel, mcp_panel, settings_panel])
            history_btn.click(show_history, outputs=[chat_panel, history_panel, remme_panel, mcp_panel, settings_panel])
            remme_btn.click(show_remme, outputs=[chat_panel, history_panel, remme_panel, mcp_panel, settings_panel])
            mcp_btn.click(show_mcp, outputs=[chat_panel, history_panel, remme_panel, mcp_panel, settings_panel])
            settings_btn.click(show_settings, outputs=[chat_panel, history_panel, remme_panel, mcp_panel, settings_panel])
            
            # Query submission
            def submit_query(query):
                if not query or not query.strip():
                    return "", GRAPH_HTML_TEMPLATE, "Please enter a query.", {}, []
                
                run_id = self.create_run(query)
                if run_id:
                    graph_data = self.get_run_graph(run_id)
                    graph_html = self.build_graph_html(graph_data)
                    
                    # Build node choices
                    node_choices = []
                    if graph_data:
                        for node in graph_data.get("nodes", []):
                            node_id = str(node.get("id", ""))
                            node_data = node.get("data", {})
                            agent_type = node_data.get("type", "Unknown")
                            status = node_data.get("status", "pending")
                            label = f"{node_id} - {agent_type} ({status})"
                            node_choices.append((label, node_id))
                    
                    return run_id, graph_html, "Processing...", graph_data, node_choices
                return "", GRAPH_HTML_TEMPLATE, "Error: Failed to create run.", {}, []
            
            submit_btn.click(
                submit_query,
                inputs=[query_input],
                outputs=[run_id_state, graph_html, final_output, graph_data_state, node_selector]
            )
            
            # Graph polling and updates
            def poll_graph(run_id, current_graph_data):
                if not run_id:
                    return GRAPH_HTML_TEMPLATE, "No active run.", "", {}, []
                
                graph_data = self.get_run_graph(run_id)
                if graph_data:
                    graph_html = self.build_graph_html(graph_data)
                    output = self.get_final_output(run_id)
                    
                    # Build node choices for dropdown
                    node_choices = []
                    for node in graph_data.get("nodes", []):
                        node_id = str(node.get("id", ""))
                        node_data = node.get("data", {})
                        agent_type = node_data.get("type", "Unknown")
                        status = node_data.get("status", "pending")
                        label = f"{node_id} - {agent_type} ({status})"
                        node_choices.append((label, node_id))
                    
                    return graph_html, output, "", graph_data, node_choices
                return GRAPH_HTML_TEMPLATE, "Loading...", "", {}, []
            
            # Handle node selection
            def on_node_select(node_id, graph_data):
                if not node_id or not graph_data:
                    return "No node selected."
                
                # Handle if node_id is a tuple (label, value) - extract just the value
                if isinstance(node_id, (list, tuple)):
                    node_id = node_id[1] if len(node_id) > 1 else node_id[0]
                
                # Find the node in graph data
                for node in graph_data.get("nodes", []):
                    if node.get("id") == str(node_id):
                        node_data = node.get("data", {})
                        return self.format_node_details(node_data)
                
                return "Node not found."
            
            # Initial load on page load
            demo.load(
                poll_graph,
                inputs=[run_id_state, graph_data_state],
                outputs=[graph_html, final_output, node_details, graph_data_state, node_selector]
            )
            
            # Manual refresh
            refresh_graph_btn.click(
                poll_graph,
                inputs=[run_id_state, graph_data_state],
                outputs=[graph_html, final_output, node_details, graph_data_state, node_selector]
            )
            
            # Node selection handler
            node_selector.change(
                on_node_select,
                inputs=[node_selector, graph_data_state],
                outputs=[node_details]
            )
            
            # History panel handlers
            def load_history():
                runs = self.get_runs()
                if runs:
                    df = pd.DataFrame([{
                        "ID": r.get("id", ""),
                        "Query": (r.get("query", "")[:80] + "...") if len(r.get("query", "")) > 80 else r.get("query", ""),
                        "Date": r.get("created_at", "")[:10] if r.get("created_at") else "",
                        "Status": r.get("status", "unknown")
                    } for r in runs])
                    return df
                return pd.DataFrame(columns=["ID", "Query", "Date", "Status"])
            
            def select_history_run(evt: gr.SelectData):
                if evt.index[0] is not None:
                    runs = self.get_runs()
                    if evt.index[0] < len(runs):
                        run_id = runs[evt.index[0]].get("id")
                        graph_data = self.get_run_graph(run_id)
                        if graph_data:
                            graph_html = self.build_graph_html(graph_data)
                            output = self.get_final_output(run_id)
                            
                            # Build node choices
                            node_choices = []
                            for node in graph_data.get("nodes", []):
                                node_id = node.get("id", "")
                                node_data = node.get("data", {})
                                agent_type = node_data.get("type", "Unknown")
                                status = node_data.get("status", "pending")
                                label = f"{node_id} - {agent_type} ({status})"
                                node_choices.append((label, node_id))
                            
                            return graph_html, output, run_id, graph_data, node_choices
                return GRAPH_HTML_TEMPLATE, "", "", {}, []
            
            def on_history_node_select(node_id, graph_data):
                if not node_id or not graph_data:
                    return "No node selected."
                
                # Handle if node_id is a tuple (label, value) - extract just the value
                if isinstance(node_id, (list, tuple)):
                    node_id = node_id[1] if len(node_id) > 1 else node_id[0]
                
                # Find the node in graph data
                for node in graph_data.get("nodes", []):
                    if node.get("id") == str(node_id):
                        node_data = node.get("data", {})
                        return self.format_node_details(node_data)
                
                return "Node not found."
            
            load_history_btn.click(load_history, outputs=[history_list])
            history_list.select(
                select_history_run,
                outputs=[history_graph_html, history_final_output, selected_run_id, history_graph_data_state, history_node_selector]
            )
            
            # History node selection handler
            history_node_selector.change(
                on_history_node_select,
                inputs=[history_node_selector, history_graph_data_state],
                outputs=[history_node_details]
            )
            
            # Remme panel handlers
            def load_remme_memories():
                memories = self.get_remme_memories()
                if memories and isinstance(memories, list):
                    rows = []
                    for m in memories:
                        # Handle both dict and string responses
                        if isinstance(m, dict):
                            mem_id = str(m.get("id", ""))
                            mem_text = str(m.get("text", ""))
                            rows.append({
                                "ID": mem_id[:20] + "..." if len(mem_id) > 20 else mem_id,
                                "Text": (mem_text[:100] + "...") if len(mem_text) > 100 else mem_text,
                                "Category": str(m.get("category", "")),
                                "Source": str(m.get("source", ""))
                            })
                        elif isinstance(m, str):
                            # If it's just a string, create a simple row
                            rows.append({
                                "ID": m[:20] + "..." if len(m) > 20 else m,
                                "Text": m[:100] + "..." if len(m) > 100 else m,
                                "Category": "",
                                "Source": ""
                            })
                    if rows:
                        return pd.DataFrame(rows)
                return pd.DataFrame(columns=["ID", "Text", "Category", "Source"])
            
            def load_remme_preferences():
                return self.get_remme_preferences()
            
            refresh_memories_btn.click(load_remme_memories, outputs=[remme_memories])
            refresh_preferences_btn.click(load_remme_preferences, outputs=[remme_preferences])
            
            # MCP panel handlers
            def load_mcp_servers():
                return self.get_mcp_servers()
            
            refresh_mcp_btn.click(load_mcp_servers, outputs=[mcp_servers_info])
            
            # Settings panel handlers
            def load_settings():
                return self.get_settings()
            
            refresh_settings_btn.click(load_settings, outputs=[settings_info])
            
            # Initial load
            demo.load(load_history, outputs=[history_list])
            demo.load(load_remme_memories, outputs=[remme_memories])
            demo.load(load_remme_preferences, outputs=[remme_preferences])
            demo.load(load_mcp_servers, outputs=[mcp_servers_info])
            demo.load(load_settings, outputs=[settings_info])
            
            # Maximize output (refresh and show full output)
            def maximize_output(run_id):
                if run_id:
                    output = self.get_final_output(run_id)
                    if output and len(output) > 2000:
                        # Show full output with a note
                        return f"**Full Output (showing complete content):**\n\n{output}"
                    return output
                return "No output available. Run a query first."
            
            maximize_output_btn.click(
                maximize_output,
                inputs=[run_id_state],
                outputs=[final_output]
            )
        
        return demo


def launch_ui(share=False, server_name="0.0.0.0", server_port=7860, reload=False):
    """Launch the advanced UI
    
    Args:
        share: Create a public link
        server_name: Server hostname
        server_port: Server port
        reload: Enable auto-reload on file changes (watches ui/advanced_ui.py)
    """
    ui = AdvancedUI()
    demo = ui.build_ui()
    
    if reload:
        # Watch for file changes and reload
        import os
        import sys
        from pathlib import Path
        
        ui_file = Path(__file__).resolve()
        print(f"[yellow]Auto-reload enabled. Watching: {ui_file}[/yellow]")
        print("[yellow]Changes to ui/advanced_ui.py will automatically reload the UI[/yellow]")
        
        # Use Gradio's watch parameter to watch the UI file
        demo.launch(
            share=share, 
            server_name=server_name, 
            server_port=server_port,
            css=CUSTOM_CSS,
            theme=gr.themes.Soft(),
            show_error=True,
            watch=[str(ui_file)]  # Watch the UI file for changes
        )
    else:
        demo.launch(
            share=share, 
            server_name=server_name, 
            server_port=server_port,
            css=CUSTOM_CSS,
            theme=gr.themes.Soft(),
            show_error=True
        )


if __name__ == "__main__":
    import sys
    reload_mode = "--reload" in sys.argv
    launch_ui(reload=reload_mode)
