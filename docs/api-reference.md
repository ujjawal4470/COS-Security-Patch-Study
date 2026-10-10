# API Reference

All endpoints are prefixed with `/api`.

## VM Connection
- `GET /api/vm/status`: Returns current connection status.
- `POST /api/vm/connect`: Initializes connection to GCP VM. (Body: `{"project": "...", "zone": "...", "instance": "..."}`)
- `POST /api/vm/disconnect`: Terminates session and reverts to Demo Mode.

## Dashboard
- `GET /api/dashboard/summary`: High-level metrics for main dashboard view. includes `data_source` field ("demo" or "live").

## Assessment
- `POST /api/assessment/run`: Triggers a new overall security assessment.
- `GET /api/assessment/latest`: Retrieves the most recent assessment results.
- `GET /api/assessment/history`: Retrieves list of past assessments.

## Hardening
- `GET /api/hardening/recommendations`: List of recommended configuration changes.
- `GET /api/hardening/status`: Status of applied hardening rules.
- `POST /api/hardening/apply/{action_id}`: Apply a specific hardening fix.

## Network
- `GET /api/network/firewall-rules`: Lists current iptables/GCP firewall rules.
- `GET /api/network/analysis`: Open ports and network vulnerabilities.

## CIS Benchmarks
- `POST /api/cis/run`: Executes the CIS benchmark script.
- `GET /api/cis/latest`: Retrieves the last CIS scan report.
- `GET /api/cis/benchmarks`: Retrieves the benchmark definitions.

## Container Security
- `GET /api/container/docker-info`: Docker daemon configuration.
- `GET /api/container/running`: List of running containers and their privilege levels.
- `GET /api/container/security-checks`: Misconfigurations in running containers.

## Patches & Updates
- `GET /api/patches/current-version`: Current COS milestone and build.
- `GET /api/patches/available`: Available updates.
- `GET /api/patches/history`: Timeline of applied updates.

## CVE Analysis
- `GET /api/cve/list`: Known CVEs for current OS version.
- `GET /api/cve/statistics`: Aggregated severity counts.
- `GET /api/cve/{cve_id}`: Detailed information on a specific CVE.

## Comparison
- `GET /api/comparison/latest`: Delta between current state and last snapshot.
- `POST /api/comparison/snapshot`: Save a snapshot for future comparison.
- `GET /api/comparison/history`: List of saved snapshots.
