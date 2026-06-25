#!/bin/bash
# ngrok tunnel helper
# Usage: bash tools/ngrok_setup.sh

echo "[*] Starting ngrok tunnel on port 443..."
echo "[*] Your public URL will appear below:"
echo ""

ngrok http 443 --log=stdout 2>&1 | grep -E "url=|URL:"