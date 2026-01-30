"""
Video Trimmer Tool - Main Entry Point

A Windows desktop application for trimming frames from the end of video files.
Provides real-time preview and lossless export using FFmpeg stream copy.

Usage:
    python -m src.main
    
    Or run directly:
    python src/main.py
"""

import sys
import tkinter as tk
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.ui.app_window import AppWindow


def main() -> int:
    """
    Main entry point for the Video Trimmer application.
    
    Returns:
        int: Exit code (0 for success).
    """
    # Create root window
    root = tk.Tk()
    
    # Create application
    app = AppWindow(root)
    
    # Handle window close
    def on_closing():
        app.cleanup()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main event loop
    root.mainloop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
