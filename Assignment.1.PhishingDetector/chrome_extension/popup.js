document.getElementById('scanBtn').addEventListener('click', async () => {
  const btn = document.getElementById('scanBtn');
  btn.innerText = "Scanning Email...";
  
  // 1. Get the current active tab
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 2. Execute script to automatically find and extract email text
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: getGmailContent // Calls the extraction function defined below
  }, (results) => {
    
    if (results && results[0] && results[0].result) {
      // Content found successfully, sending to server for analysis
      analyzeText(results[0].result);
    } else {
      showError("Could not find email content automatically. Please open an email first.");
      btn.innerText = "SCAN EMAIL";
    }
  });
});

// Function executed within the context of the Gmail page
function getGmailContent() {
  // Method 1: Look for the specific Gmail message body class
  const gmailBody = document.querySelector('.a3s');
  if (gmailBody) {
    return gmailBody.innerText;
  }
  
  // Method 2: Fallback to capturing all page text if not Gmail or structure changed
  return document.body.innerText;
}

async function analyzeText(text) {
  try {
    // Send extracted text to the local Python backend server
    const response = await fetch('http://127.0.0.1:5001/api/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });
    
    const data = await response.json();
    showResult(data);
    
  } catch (error) {
    showError("Server Error: Make sure python app.py is running!");
  }
  document.getElementById('scanBtn').innerText = "SCAN EMAIL";
}

function showResult(data) {
  const div = document.getElementById('resultArea');
  const verdict = document.getElementById('verdict');
  const score = document.getElementById('score');
  const reasons = document.getElementById('reasons');

  div.style.display = 'block';
  div.className = 'result-box'; 
  
  verdict.innerText = data.status;
  score.innerText = data.score + "/100";

  // Apply visual styling based on the risk score
  if (data.score >= 60) div.classList.add('phishing');
  else if (data.score > 20) div.classList.add('suspicious');
  else div.classList.add('safe');

  if (data.reasons.length > 0) {
    // Generate an unordered list of detection reasons
    reasons.innerHTML = "<ul>" + data.reasons.map(r => `<li>${r}</li>`).join('') + "</ul>";
  } else {
    reasons.innerHTML = "<p>No threats found.</p>";
  }
}

function showError(msg) {
  const div = document.getElementById('resultArea');
  div.style.display = 'block';
  div.className = 'result-box';
  div.innerHTML = `<p style="color:red; font-weight:bold;">${msg}</p>`;
}