#!/bin/bash
# ============================================================
# Ollama EC2 Setup Script
# Downloads Ollama to /opt/ollama, configures systemd service,
# and binds to 0.0.0.0:11434 for remote access.
# 
# Usage: sudo bash setup-ollama-ec2.sh
# ============================================================

set -euo pipefail

echo "=== Step 1: Download Ollama to /opt/ollama ==="
mkdir -p /opt/ollama
curl -fsSL https://ollama.com/install.sh | OLLAMA_INSTALL_DIR=/opt/ollama sh

echo ""
echo "=== Step 2: Create systemd service file ==="
cat > /etc/systemd/system/ollama.service << 'EOF'
[Unit]
Description=Ollama LLM Service
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Restart=always
RestartSec=3
User=root
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "=== Step 3: Enable and start Ollama via systemctl ==="
systemctl daemon-reload
systemctl enable ollama
systemctl start ollama

echo ""
echo "=== Verifying ==="
sleep 2
systemctl status ollama --no-pager

echo ""
echo "✓ Ollama installed at: /usr/local/bin/ollama"
echo "✓ Listening on: 0.0.0.0:11434"
echo "✓ Service: enabled + running"
echo ""
echo "Next steps:"
echo "  ollama pull llama3.2:3b"
echo "  ollama pull qwen3.5:4b"
