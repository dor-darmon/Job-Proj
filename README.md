The main README file acts as "master menu" for all assigment . And lanch page web    

## Assignment 1. Phishing Detector
Gmail analysis system designed to identify phishing emails . The system combines heuristic text analysis and link inspection to determine the risk level of a message.

Key Features The system performs keyword analysis to detect language indicating urgency or requests for sensitive information. It inspects URLs to identify suspicious links, such as exposed IP addresses, insecure HTTP connections, or deceptive domain names. Additionally, it verifies the sender by flagging officials sending from public domains and detecting typosquatting attempts against known brands. The tool is available as both a standalone web dashboard and a Chrome browser extension.

## How to Install and Update the Chrome Extension To run the extension on your computer, follow these steps:

Open your Google Chrome browser.

Navigate to the extensions management page by typing chrome://extensions in the address bar and pressing Enter.

In the top right corner of the page, find the Developer mode toggle and switch it to ON.

Click the Load unpacked button that appears in the top left menu.

Browse to the project folder and select the chrome_extension folder located inside Assignment.1.PhishingDetector.

The extension is now installed. To use it, open Gmail, view an email, and click the extension icon to scan the content.

## Assignment 2. Malware Analysis Sandbox
Overview A dynamic analysis tool that executes suspicious files in a controlled environment and monitors their activity in real-time to detect malicious behavior.

Key Features This desktop application allows users to select and run executable files while monitoring system changes. It tracks file system activity to detect creation, deletion, or renaming of files, which are common indicators of ransomware. It also monitors CPU and RAM usage to identify resource exhaustion and detects network activity to spot attempts to connect to external servers. At the end of the analysis, the system generates a detailed text report.

## Assignment 3. SQL Injection Simulation
Overview An educational application that demonstrates one of the most common web vulnerabilities, SQL Injection (SQLi), and highlights the difference between vulnerable and secure code.

Key Features The application features a login interface with two modes. The Vulnerable Mode uses string concatenation to build queries, allowing users to bypass authentication using input manipulation. The Secure Mode demonstrates how parameterized queries treat input as data rather than executable code, effectively neutralizing the attack. The interface displays the backend SQL query in real-time, providing immediate visual feedback on the success or failure of the attack.

# Installation and Usage
Launcher The project includes a central management script named launcher.py that allows you to run all assignments from a single dashboard.

**1. Prerequisites**
Ensure that you have **Python 3.x** installed on your machine.

**2. Install Dependencies**
Open your terminal or command prompt and run commands to install the required libraries:
```bash
pip install flask flask-cors watchdog psutil
```

**3. Launch the System**
```bash
python launcher.py
```

## Project Structure
```text
/Job-Assignments
├── launcher.py
├── README.md
├── templates/
│   └── dashboard.html
│
├── Assignment.1.PhishingDetector/
│   ├── app.py          
│   ├── phishing_detector.py
│   ├── requirements.txt 
│   ├── README.md     
│   ├── templates/
│   │   └── appUI.html 
│   └── chrome_extension/
│       ├── manifest.json 
│       ├── popup.html 
│       └── popup.js         
│
├── Assignment.2.MalwareSandboxProject/
│   ├── main.py
│   ├── gui.py
│   ├── sandbox_monitor.py 
│   ├── test_malware.py  
│   └── README.md            
│
└── Assignment.3.SQLInjection/
    ├── app.py
    ├── demo_database.db        
    ├── README.md             
    └── templates/
        └── appUI.html
