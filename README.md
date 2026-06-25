# Facebook Phishing Toolkit

**Author:** Jitu Jak  
**Motivated to:** Nancy  
**Purpose:** Authorized Penetration Testing & Security Awareness

> ⚠️ **WARNING:** This tool is for **AUTHORIZED SECURITY TESTING ONLY**.  
> Use only on systems you own or have explicit written permission to test.

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

## Quick Start

```bash
# Install
chmod +x setup.sh
sudo bash setup.sh

# Activate environment
source venv/bin/activate

# Run server
sudo python3 fb_phish.py --port 443