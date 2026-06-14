# Grafana + Tempo Observability Setup (Docker, no Compose)

Open-source observability stack for capturing and visualizing Strands Agent traces on EC2.

## Architecture

```
Notebook (Colab/Local) → OTLP HTTP → EC2:4318 (Tempo) → EC2:3200 (Tempo Query)
                                                                ↓
                                                    EC2:3000 (Grafana UI)
```

## Prerequisites

- EC2 instance (t3.small or larger, Amazon Linux 2023 / AL2)
- Docker installed and running
- Security group with inbound rules:
  - Port `3000` (TCP) — Grafana UI
  - Port `4318` (TCP) — OTLP HTTP trace ingestion
  - Port `3200` (TCP) — Tempo query API (optional, only needed if querying externally)

## Step 1: Create Tempo Configuration

```bash
mkdir -p /opt/grafana-observability
cd /opt/grafana-observability

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
```

## Step 2: Run Tempo

```bash
docker run -d --name tempo \
  -p 4318:4318 \
  -p 4317:4317 \
  -p 3200:3200 \
  -v /opt/grafana-observability/tempo.yaml:/etc/tempo.yaml \
  grafana/tempo:latest \
  -config.file=/etc/tempo.yaml
```

Verify Tempo is running:
```bash
curl -s http://localhost:3200/ready
# Expected: "ready"
```

## Step 3: Run Grafana OSS

```bash
docker run -d --name grafana \
  -p 3000:3000 \
  grafana/grafana-oss
```

Verify Grafana is healthy:
```bash
curl -s http://localhost:3000/api/health
# Expected: {"database":"ok","version":"...","commit":"..."}
```

Access Grafana UI: `http://<EC2_PUBLIC_IP>:3000`

Default login: `admin` / `admin`

## Step 4: Connect Tempo as a Datasource in Grafana

1. Go to **Connections → Data sources → Add data source**
2. Select **Tempo**
3. URL: `http://<EC2_PRIVATE_IP>:3200`
4. Click **Save & test** — should show "Data source successfully connected"

### Finding your EC2 private IP:
```bash
hostname -I | awk '{print $1}'
# Example output: 10.0.138.238
```

Use that IP in the Tempo datasource URL: `http://10.0.138.238:3200`

## Step 5: Send Traces from Your Notebook

```python
from strands.telemetry import StrandsTelemetry

strands_telemetry = StrandsTelemetry()
strands_telemetry.setup_otlp_exporter(
    endpoint="http://<EC2_PUBLIC_IP>:4318",
)

# Now any Agent you create will emit traces to Tempo
agent = Agent(model=get_model(), tools=[...], callback_handler=None)
agent("Your prompt here")
```

## Step 6: View Traces in Grafana

1. Go to **Explore** (compass icon in left sidebar)
2. Select **Tempo** datasource from the dropdown
3. Choose **Search** tab
4. Click **Run query** — your traces will appear
5. Click a trace to see the span waterfall (agent → cycle → model invoke → tool calls)

---

## Troubleshooting

### "Grafana has failed to load its application files"

**Cause:** Known issue with `grafana/grafana:latest` (v13.x) frontend asset loading.

**Fix:** Use `grafana/grafana-oss` instead:
```bash
docker stop grafana && docker rm grafana
docker run -d --name grafana -p 3000:3000 grafana/grafana-oss
```

Or pin to a stable version:
```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana-oss:11.4.0
```

### "host.docker.internal: no such host" when connecting Tempo datasource

**Cause:** `host.docker.internal` only works on Docker Desktop (Mac/Windows), not on Linux/EC2.

**Fix:** Use the EC2 private IP instead:
```bash
hostname -I | awk '{print $1}'
```
Then set Tempo URL to: `http://<PRIVATE_IP>:3200`

### Grafana shows old cached error page

**Fix:** Open in incognito/private window, or hard refresh with `Ctrl+Shift+R`.

### Port 3000/4318 not reachable from browser/notebook

**Fix:** Check EC2 security group inbound rules:
- Port 3000, TCP, Source: `0.0.0.0/0` (or your IP)
- Port 4318, TCP, Source: `0.0.0.0/0` (or your notebook's IP)

### Tempo not receiving traces

Check Tempo is running and listening:
```bash
docker logs tempo | tail -10
ss -tlnp | grep 4318
```

Test OTLP endpoint:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:4318/v1/traces
# Expected: 405 (Method Not Allowed — means it's listening, just rejects GET)
```

---

## Managing the Stack

```bash
# Check running containers
docker ps

# View logs
docker logs grafana | tail -20
docker logs tempo | tail -20

# Restart
docker restart grafana tempo

# Stop
docker stop grafana tempo

# Remove containers (data preserved in volumes)
docker rm grafana tempo

# Full cleanup (removes data too)
docker rm -f grafana tempo
docker volume prune
```

---

## Ports Reference

| Service | Port | Purpose |
|---------|------|---------|
| Grafana | 3000 | Dashboard UI |
| Tempo | 4318 | OTLP HTTP receiver (traces come in here) |
| Tempo | 4317 | OTLP gRPC receiver |
| Tempo | 3200 | Tempo query API (Grafana reads from here) |
