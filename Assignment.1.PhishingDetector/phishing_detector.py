import re
from urllib.parse import urlparse
# Library used to compare text similarity (for typosquatting)
import difflib  

class PhishingDetector:
    def __init__(self):
        # Setting up the scoring system. 
        # The higher the score, the more dangerous the email is.
        self.weights = {
            'urgency_keyword': 5,
            'danger_keyword': 20,
            'ip_link': 50,  
            'http_link': 15,
            'suspicious_sender': 30,
            'spoofed_domain': 50,
            'malformed_url': 40
        }
        
        # Urgency Keywords
        # Words that try to panic the user into clicking without thinking.
        # Includes both English and Hebrew terms.
        self.urgency_keywords = [
            'urgent', 'immediately', 'suspend', 'verify', 'action required', 'limited',
            'דחוף', 'מיידי', 'הושעה', 'לאמת', 'פעולה נדרשת', 'חסימה', 'לעדכן', 
            'תוך 24 שעות', 'מוגבל', 'הקפאה', 'להסדיר', 'עכשיו', 'בנק', 'אשראי'
        ]
        
        # Danger Keywords
        # Words related to sensitive data (passwords, banking, ID).
        self.danger_keywords = [
            'password', 'bank', 'social security', 'unauthorized login', 'credit card', 
            'security code', 'account locked',
            'סיסמה', 'כניסה לא מורשית', 'קוד אימות', 'חשבון מוגבל', 
            'פרטי תשלום', 'תעודת זהות', 'קוד סודי', 'ויזה'
        ]
        
        # List of free public email domains.
        # Official companies will NEVER use these for support emails.
        self.public_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'walla.co.il']
        
        # Protected Brands
        # We protect these brands against "Typosquatting"
        self.protected_brands = [
            'paypal', 'amazon', 'apple', 'microsoft', 'facebook', 'netflix', 'google',
            'bit', 'pepper', 'isracard', 'cal', 'max', 'leumi', 'hapoalim', 'discount', 
            'israelpost', 'doar'
        ]

    def check_keywords(self, text):
        """Scans the text for words that indicate pressure or danger."""
        score = 0
        reasons = []
        text_lower = text.lower() if text else ""

        # Check if the email is screaming "URGENT!"
        for word in self.urgency_keywords:
            if word in text_lower:
                score += self.weights['urgency_keyword']
                reasons.append(f"High urgency language detected: '{word}'")

        # Check if the email is asking for secrets like passwords
        for word in self.danger_keywords:
            if word in text_lower:
                score += self.weights['danger_keyword']
                reasons.append(f"Sensitive request detected: '{word}'")
                
        return score, reasons

    def check_urls(self, body):
        """Analyzes all links in the email body to find traps."""
        score = 0
        reasons = []
        body = body if body else ""
        
        # Find all links (http or https)
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
        
        for url in urls:
            try:
                # TRICK CHECK: Hackers often use the '@' symbol to hide the real destination.
                # Example: http://google.com@evil-site.com
                if '@' in url:
                    score += self.weights['malformed_url']
                    reasons.append(f"Deceptive URL structure detected (@ symbol usage): {url}")

                parsed = urlparse(url)
                
                # Security Check: HTTP is not secure. Real banks use HTTPS.
                if parsed.scheme == 'http':
                    score += self.weights['http_link']
                    reasons.append(f"Insecure link (HTTP): {url}")
                
                # IP Check: If the link is just numbers (IP) instead of a name, it's a red flag.
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', parsed.netloc):
                    score += self.weights['ip_link']
                    reasons.append(f"Link points to IP address instead of domain: {url}")
                
                # Length Check: Super long domains are often used to hide the real identity.
                if len(parsed.netloc) > 50:
                    score += 10
                    reasons.append(f"Suspiciously long domain name: {parsed.netloc}")

            except:
                continue

        return score, reasons

    def check_sender(self, sender):
        """
        Sender Analysis.
        Checks for:
        Official names using free Gmail accounts. 'Typosquatting' is : fake domains looking like real ones
        """
        score = 0
        reasons = []
        sender = sender if sender else ""
        
        if '@' not in sender:
            return 0, []

        try:
            user, domain = sender.split('@')
            
            # Gmail Imposter chek if the user claims to be 'support' or 'security' but uses Gmail/Yahoo.
            suspicious_users = ['admin', 'support', 'security', 'service', 'verify', 'billing', 'info', 'bit']
            is_suspicious_user = any(s in user.lower() for s in suspicious_users)
            is_public_domain = domain.lower() in self.public_domains
            
            if is_suspicious_user and is_public_domain:
                score += self.weights['suspicious_sender']
                reasons.append(f"Suspicious: Official name '{user}' sending from public domain '{domain}'")
            
            # strip the extension to compare just the name.
            domain_name = domain.split('.')[0] 
            
            for brand in self.protected_brands:
                # We use a fuzzy matching algorithm to see if the domain is 'almost' identical to a brand.
                # Example: 'paypa1' is 90% similar to 'paypal'.
                similarity = difflib.SequenceMatcher(None, domain_name, brand).ratio()
                
                # If similarity is between 80% and 99% (Close but not exact)
                if 0.80 <= similarity < 1.0:
                    # Double check to make sure it's not a false alarm
                    if brand in domain_name or domain_name in brand or len(domain_name) == len(brand):
                        score += self.weights['spoofed_domain']
                        reasons.append(f"Typosquatting Detected: Domain '{domain}' is confusingly similar to '{brand}'")
                        break # We found a match, no need to keep checking

        except:
            pass

        return score, reasons

    def analyze(self, email_data):
        """Main function that runs all checks and returns the final verdict."""
        total_score = 0
        all_reasons = []

        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        sender = email_data.get('sender', '')

        # Combine subject and body to search for keywords everywhere
        full_text = subject + " " + body
        
        # Check keywords
        kw_score, kw_reasons = self.check_keywords(full_text)
        total_score += kw_score
        all_reasons.extend(kw_reasons)

        # Check links
        url_score, url_reasons = self.check_urls(body)
        total_score += url_score
        all_reasons.extend(url_reasons)

        # Check the sender (Smart Check)
        sender_score, sender_reasons = self.check_sender(sender)
        total_score += sender_score
        all_reasons.extend(sender_reasons)

        # Final Verdict Calculation
        status = "SAFE"
        if total_score >= 60:
            status = "PHISHING DETECTED"
        elif total_score > 20:
            status = "SUSPICIOUS"

        return {
            "score": total_score,
            "status": status,
            "reasons": all_reasons
        }