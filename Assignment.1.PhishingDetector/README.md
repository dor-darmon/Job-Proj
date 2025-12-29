Email Phishing Detector

## Overview
This project is a cybersecurity tool developed to analyze emails and detect potential phishing attempts using heuristic analysis. It evaluates emails based on keywords, URL patterns, and sender authenticity. The system includes both a **Web Interface** and a **Chrome Extension** to scann within Gmail.

## Features
 **Keyword Analysis:** Detects high-pressure language (e.g., "Urgent", "Suspend").
 
 **URL Inspection:** Identifies IP-based links and insecure HTTP connections.
 
 **Sender Verification:** Flags suspicious public domains (e.g., "support@gmail.com") and spoofed domains (e.g., "paypa1.com").
 
 **Dual Interface:** 
    1. Standalone Web Dashboard.
    2. Integrated Chrome Extension for Gmail.
  
## How to Install and Update the Chrome Extension To run the extension on your computer, follow these steps:

Open your Google Chrome browser.

Navigate to the extensions management page by typing chrome://extensions in the address bar and pressing Enter.

In the top right corner of the page, find the Developer mode toggle and switch it to ON.

Click the Load unpacked button that appears in the top left menu.

Browse to the project folder and select the chrome_extension folder located inside Assignment.1.PhishingDetector.

The extension is now installed. To use it, open Gmail, view an email, and click the extension icon to scan the content.

## Project Structure
```text
/PhishingDetector
├── app.py     
├── phishing_detector.py    
├── requirements.txt      
├── templates/
│   └── appUI.html         
└── chrome_extension/   
    ├── manifest.json
    ├── popup.html
    └── popup.js
