import os
import sys
import subprocess
import webbrowser
from flask import Flask, render_template, jsonify
from threading import Timer

# Initialize Flask Application
app = Flask(__name__)

#  CONFIGURATION
# Define your projects here.
# 'folder': The directory name relative to this launcher.
# 'script': The Python file to execute.
# 'type': 'web' for web apps (opens browser), 'script' for console tools.
# 'url': (Optional) The URL to open if type is 'web'.

PROJECTS = {
    'Assignment.1.PhishingDetector': {
        'name': 'Phishing Detectoro',
        'folder': 'Assignment.1.PhishingDetector',
        'script': 'app.py',
        'type': 'web',
        'url': 'http://127.0.0.1:5001'  # Ensure this matches the port in the project's app.py
    },
     'Assignment.2.MalwareSandboxProject': {
        'name': 'Sandbox Project',
        'folder': 'Assignment.2.MalwareSandboxProject',
        'script': 'main.py',
        'type': 'script'
    },
    'Assignment.3.SQLInjection': {
        'name': 'Network Scanner',
        'folder': 'Assignment.3.SQLInjection',
        'script': 'app.py',
        'type': 'web',
        'url': 'http://127.0.0.1:5002'
    }
}

#  APPLICATION LOGIC

@app.route('/')
def dashboard():
    """Renders the main dashboard HTML."""
    return render_template('dashboard.html', projects=PROJECTS)

@app.route('/run/<project_id>', methods=['POST'])
def run_project(project_id):
    """
    Handler to execute a specific project.
    It spawns a new subprocess for the requested script.
    """
    if project_id not in PROJECTS:
        return jsonify({'status': 'error', 'message': 'Project ID not found in configuration'}), 404

    config = PROJECTS[project_id]
    
    # Construct absolute paths to ensure execution context is correct
    base_dir = os.getcwd()
    project_dir = os.path.join(base_dir, config['folder'])
    script_path = config['script']

    # Validation: Check if directory exists
    if not os.path.exists(project_dir):
        return jsonify({'status': 'error', 'message': f"Directory not found: {config['folder']}"}), 404

    try:
        # Launch Logic
        # We handle Windows specifically to ensure a new console window opens for scripts.
        if sys.platform == "win32":
            # CREATE_NEW_CONSOLE ensures scripts like scanners/calculators open in a visible window
            subprocess.Popen(
                [sys.executable, script_path], 
                cwd=project_dir, 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # macOS / Linux
            subprocess.Popen([sys.executable, script_path], cwd=project_dir)

        # If it is a Web Application, schedule the browser to open
        if config['type'] == 'web' and 'url' in config:
            Timer(1.5, lambda: webbrowser.open(config['url'])).start()

        return jsonify({'status': 'success', 'message': f"Successfully launched {config['name']}"})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def open_main_dashboard():
    """Opens the main launcher dashboard in the browser."""
    webbrowser.open("http://127.0.0.1:5000")

#  MAIN ENTRY POINT
if __name__ == '__main__':
    print("--- CENTRAL MANAGEMENT CONSOLE STARTED ---")
    print("Server running on http://127.0.0.1:5000")
    print("Press CTRL+C to stop.")
    
    # Open the dashboard automatically after 1 second
    Timer(1, open_main_dashboard).start()
    
    # Run the Flask server
    app.run(port=5000, debug=False)