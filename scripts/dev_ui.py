#!/usr/bin/env python3
"""
Development script that auto-restarts the UI when files change.
Usage: uv run python scripts/dev_ui.py
"""

import subprocess
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class UIChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.last_restart = 0
        self.restart_ui()
    
    def restart_ui(self):
        """Restart the UI process"""
        import time
        current_time = time.time()
        # Debounce: only restart once per 2 seconds
        if current_time - self.last_restart < 2.0:
            return
        self.last_restart = current_time
        
        # Kill existing process
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
        
        try:
            from rich import print
            print("\n[yellow]🔄 Restarting UI...[/yellow]")
        except:
            print("\n🔄 Restarting UI...")
        
        # Start new process
        project_root = Path(__file__).parent.parent
        app_path = project_root / "app.py"
        
        self.process = subprocess.Popen(
            [sys.executable, str(app_path), "--ui"],
            cwd=str(project_root),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        try:
            from rich import print
            print("[green]✅ UI restarted[/green]")
        except:
            print("✅ UI restarted")
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only watch Python files in ui/ directory
        if event.src_path.endswith('.py') and 'ui/' in event.src_path:
            try:
                from rich import print
                print(f"\n[yellow]📝 File changed: {event.src_path}[/yellow]")
            except:
                print(f"\n📝 File changed: {event.src_path}")
            self.restart_ui()

def main():
    project_root = Path(__file__).parent.parent
    ui_dir = project_root / "ui"
    
    try:
        from rich import print
        print("[bold green]🚀 Starting UI with auto-reload[/bold green]")
        print(f"[yellow]Watching: {ui_dir}[/yellow]")
        print("[yellow]Press Ctrl+C to stop[/yellow]\n")
    except:
        print("🚀 Starting UI with auto-reload")
        print(f"Watching: {ui_dir}")
        print("Press Ctrl+C to stop\n")
    
    event_handler = UIChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(ui_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        try:
            from rich import print
            print("\n[yellow]Stopping...[/yellow]")
        except:
            print("\nStopping...")
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    
    observer.join()

if __name__ == "__main__":
    try:
        from rich import print
    except ImportError:
        # Fallback to regular print if rich is not available
        pass
    main()

