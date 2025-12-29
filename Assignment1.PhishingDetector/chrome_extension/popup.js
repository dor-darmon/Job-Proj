document.getElementById('scanBtn').addEventListener('click', async () => {
  const btn = document.getElementById('scanBtn');
  btn.innerText = "Scanning Email...";
  
  // 1. קבלת הטאב הנוכחי
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 2. הרצת סקריפט חכם שמוצא את הטקסט לבד
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: getGmailContent // קורא לפונקציה החדשה למטה
  }, (results) => {
    
    if (results && results[0] && results[0].result) {
      // יש טקסט! שולחים לשרת
      analyzeText(results[0].result);
    } else {
      showError("Could not find email content automatically. Please open an email first.");
      btn.innerText = "SCAN EMAIL";
    }
  });
});

// --- זו הפונקציה החדשה שרצה בתוך העמוד של ג'ימייל ---
function getGmailContent() {
  // ניסיון 1: חיפוש המחלקה הספציפית של גוף ההודעה בג'ימייל
  const gmailBody = document.querySelector('.a3s');
  if (gmailBody) {
    return gmailBody.innerText;
  }
  
  // ניסיון 2: אם זה לא ג'ימייל, או שהמבנה השתנה, מחזירים את כל הטקסט בדף
  return document.body.innerText;
}

async function analyzeText(text) {
  try {
    // שליחה לשרת הפייתון שלך (בלי לשנות את השרת)
    const response = await fetch('http://127.0.0.1:5000/api/scan', {
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

  if (data.score >= 60) div.classList.add('phishing');
  else if (data.score > 20) div.classList.add('suspicious');
  else div.classList.add('safe');

  if (data.reasons.length > 0) {
    // list 
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