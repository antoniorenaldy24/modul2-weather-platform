from taipy.gui import Gui
import sys
import os
import threading

# Add root to python path for framework independent cross-loading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import state variables natively to attach them to the Taipy Environment Scope
from frontend_taipy.state_manager import (
    fig, 
    kpi_temp, 
    kpi_wind, 
    status_text,
    background_fetcher
)
from frontend_taipy.pages.dashboard import dashboard_md

# Inline raw CSS injection to emulate the White Glassmorphism styling of Dash, overriding Taipy's raw UI where possible
aesthetic_css = """
body {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
    color: #333333;
}
.glass-panel {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
    transition: transform 0.2s ease-in-out;
}
.kpi-value {
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: -webkit-linear-gradient(#2c3e50, #3498db);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.kpi-label {
    font-size: 0.9rem !important;
    color: #7f8c8d !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-weight: 600 !important;
}
"""

# Establish global pages
pages = {
    "/": dashboard_md
}

if __name__ == '__main__':
    # Initialize Taipy GUI
    core_gui = Gui(pages=pages)
    
    # Start the daemon background polling thread, feeding it the GUI instance
    poll_loop = threading.Thread(target=background_fetcher, args=(core_gui,), daemon=True)
    poll_loop.start()
    
    # Serve Taipy Application. Port 5000 avoids port 8050 utilized by Dash.
    # We turn on use_reloader=False because Taipy reloading kills our background threading loop destructively in some setups
    with open("temp_style.css", "w") as f:
        f.write(aesthetic_css)
        
    core_gui.run(port=5001, dark_mode=False, use_reloader=False, css_file="temp_style.css", title="System Beta - Map")
