Email Phishing Detector

## Overview
This project is a cybersecurity tool developed to analyze emails and detect potential phishing attempts using heuristic analysis. It evaluates emails based on keywords, URL patterns, and sender authenticity (including spoofing detection). The system includes both a **Web Interface** and a **Chrome Extension** for real-time scanning within Gmail.

## Features
* **Keyword Analysis:** Detects high-pressure language (e.g., "Urgent", "Suspend").
* **URL Inspection:** Identifies IP-based links and insecure HTTP connections.
* **Sender Verification:** Flags suspicious public domains (e.g., "support@gmail.com") and spoofed domains (e.g., "paypa1.com").
* **Dual Interface:** 1. Standalone Web Dashboard.
    2. Integrated Chrome Extension for Gmail.

## Project Structure
```text
/PhishingDetector
├── app.py                  # Main Flask Server
├── phishing_detector.py    # Detection Logic Class
├── requirements.txt        # Dependencies
├── templates/
│   └── index.html          # Web UI
└── chrome_extension/       # Chrome Extension Source
    ├── manifest.json
    ├── popup.html
    └── popup.js