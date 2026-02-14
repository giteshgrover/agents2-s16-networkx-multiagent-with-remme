
import asyncio
import sys
import os
from pathlib import Path
from rich import print
from rich.console import Console
from rich.panel import Panel

# Add Arcturus to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.loop import AgentLoop4
from mcp_servers.multi_mcp import MultiMCP

import argparse

# ... existing code ...

async def run_query(agent_loop, query):
    """Helper to run a query and get text output"""
    context = await agent_loop.run(
        query=query,
        file_manifest=[],
        globals_schema={},
        uploaded_files=[]
    )
    if context:
        summary = context.get_execution_summary()
        if "final_outputs" in summary and summary["final_outputs"]:
            return str(summary["final_outputs"])
        else:
            summarizer_node = next((n for n in context.plan_graph.nodes if context.plan_graph.nodes[n].get("agent") == "SummarizerAgent"), None)
            if summarizer_node:
                return str(context.plan_graph.nodes[summarizer_node].get("output"))
    return "No output produced."

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true", help="Launch Web UI")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for UI development")
    args = parser.parse_args()

    console = Console()
    console.print(Panel.fit("[bold cyan]S16 NetworkX Agent System[/bold cyan]", border_style="blue"))

    # 1. Start MCP Servers
    multi_mcp = MultiMCP()
    await multi_mcp.start()

    try:
        # 2. Initialize Agent Loop
        agent_loop = AgentLoop4(multi_mcp=multi_mcp)

        if args.ui:
            try:
                from ui.advanced_ui import AdvancedUI
            except ImportError as e:
                print(f"[red]Error importing AdvancedUI: {e}[/red]")
                print("[yellow]Make sure all dependencies are installed: gradio, requests, pandas[/yellow]")
                return
            
            print("[bold green]Starting Advanced UI on http://localhost:7860[/bold green]")
            print("[yellow]Note: Make sure the API server is running on http://localhost:8000[/yellow]")
            print("[yellow]Start it with: uv run uvicorn api:app --reload --host 0.0.0.0 --port 8000[/yellow]")
            print("[yellow]Or: uv run python api.py[/yellow]")
            
            try:
                # Launch advanced UI (runs in separate thread, non-blocking)
                from ui.advanced_ui import launch_ui
                launch_ui(share=False, server_name="0.0.0.0", server_port=7860, reload=args.reload)
                
                # Keep the main thread alive
                while True:
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"[red]Error launching UI: {e}[/red]")
                import traceback
                traceback.print_exc()
                return 
        else:
            # 3. Interactive Loop (CLI)
            while True:
                try:
                    query = console.input("\n[bold green]User Input (or 'exit'):[/bold green] ")
                    if query.lower() in ["exit", "quit", "q"]:
                        break
                    
                    if not query.strip():
                        continue

                    console.print(f"\n[dim]Processing: {query}[/dim]")

                    # Run Workflow
                    result_text = await run_query(agent_loop, query)
                    console.print(Panel(result_text, title="Result", border_style="green"))

                except KeyboardInterrupt:
                    print("\n[yellow]Interrupted by user[/yellow]")
                    break
                except Exception as e:
                    print(f"[red]Error during execution: {e}[/red]")
                    import traceback
                    traceback.print_exc()

    finally:
        await multi_mcp.stop()
        print("[blue]System Shutdown.[/blue]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
