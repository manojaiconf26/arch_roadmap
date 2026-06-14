#!/bin/bash
# Setup Grafana + Tempo observability stack with Docker Compose

set -e

# Create project directory
mkdir -p /opt/grafana-observability
cd /opt/grafana-observability

# Create tempo.yaml
cat > tempo.yaml << 'EOF'
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        http:
          endpoint: "0.0.0.0:4318"
        grpc:
          endpoint: "0.0.0.0:4317"

storage:
  trace:
    backend: local
    local:
      path: /var/tempo/traces
    wal:
      path: /var/tempo/wal
EOF

# Create grafana datasource provisioning
cat > grafana-datasources.yml << 'EOF'
apiVersion: 1
datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    isDefault: true
    editable: true
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: "3.9"
services:
  tempo:
    image: grafana/tempo:latest
    command: ["-config.file=/etc/tempo.yaml"]
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
      - tempo-data:/var/tempo
    ports:
      - "4318:4318"
      - "4317:4317"
      - "3200:3200"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml
    depends_on:
      - tempo

volumes:
  tempo-data:
  grafana-data:
EOF

# Start the stack
docker-compose up -d

echo ""
echo "=== Grafana + Tempo Stack Running ==="
echo "  Grafana UI:     http://$(hostname -I | awk '{print $1}'):3000"
echo "  Login:          admin / admin"
echo "  OTLP endpoint:  http://$(hostname -I | awk '{print $1}'):4318"
echo ""
echo "  From your notebook:"
echo "    strands_telemetry.setup_otlp_exporter(endpoint=\"http://$(hostname -I | awk '{print $1}'):4318\")"
echo ""
