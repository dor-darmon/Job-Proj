import webbrowser
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
# Updated import name to match standard convention
from phishing_detector import PhishingDetector

app = Flask(__name__)
CORS(app)
detector = PhishingDetector()

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        email_data = {
            "sender": request.form.get('sender'),
            "subject": request.form.get('subject'),
            "body": request.form.get('body')
        }
        result = detector.analyze(email_data)
        
    return render_template('index.html', result=result)

@app.route('/api/scan', methods=['POST'])
def scan_api():
    data = request.json
    if 'text' in data:
        # Handle requests from Chrome Extension
        email_data = {"sender": "", "subject": "From Extension", "body": data['text']}
    else:
        email_data = data
        
    result = detector.analyze(email_data)
    return jsonify(result)

def print_instructions(url):
    print("-" * 60)
    print(f"Server Running at: {url}")
    print("-" * 60)
    print("OPTION 1: WEB INTERFACE")
    print(f"   1. Go to {url}")
    print("   2. Enter Sender, Subject, and Body.")
    print("   3. Click 'Analyze Email'.")
    print("\nOPTION 2: CHROME EXTENSION")
    print("   1. Go to chrome://extensions")
    print("   2. Enable 'Developer Mode'.")
    print("   3. Click 'Load Unpacked' and select the 'chrome_extension' folder.")
    print("   4. Open Gmail, open an email, and click the extension icon.")
    print("-" * 60)

if __name__ == '__main__':
    port = 5001
    url = f"http://127.0.0.1:{port}"
    
    print_instructions(url)
    
    # Auto-open browser
    try:
        webbrowser.open(url)
    except:
        pass

    app.run(debug=True, port=port, use_reloader=False)