# System Architecture

## Overview
The Container-Optimized OS Hardening & Patch Study project utilizes a modular, decoupled architecture, splitting responsibilities between a modern frontend, a robust API backend, and specialized scanning modules.

## Component Diagram
```text
+-------------------+       HTTP/REST        +-------------------+
|   React / Vite    | <--------------------> |   Flask API       |
|   Frontend        |                        |   (Backend)       |
+-------------------+                        +---------+---------+
                                                       |
         +---------------------------------------------+
         |                       |                     |
+--------v--------+     +--------v--------+   +--------v--------+
|   SQLite DB     |     |   GCP Client    |   | Scanner Modules |
| (Data Storage)  |     | (gcloud/ssh)    |   | (OS, CIS, Net)  |
+-----------------+     +-----------------+   +-----------------+
```

## Data Flow
1. User initiates a scan via the frontend dashboard.
2. React application sends a POST request to the Flask backend.
3. Flask delegates the task to Python Scanner Modules.
4. If in Live Mode, Scanners invoke `gcloud compute ssh` to run scripts on the COS VM.
5. Scanners parse command outputs into JSON and store results in SQLite.
6. Backend returns the parsed data to the frontend for visualization.

## Technology Choices
- **React/Vite**: Fast development loop and rich ecosystem for data visualization.
- **Flask**: Lightweight Python web framework, ideal for wrapping shell scripts and system administration tasks.
- **SQLite**: Zero-configuration, file-based database perfect for local studies and small-scale deployments.
- **Container-Optimized OS**: The target system, selected for its hardened nature and importance in modern GCP Kubernetes/Docker deployments.

## Security Considerations
- Demo Mode operates without any credentials.
- Live Mode relies strictly on Google Cloud IAM (service accounts or user credentials).
- Firewall rules strictly limit ingress to the analyzer's IP.
- Backend avoids executing unsanitized user input in shell contexts.

## Database Schema Overview
- **assessments**: Historical scan runs with scores.
- **cis_results**: Log of pass/fail benchmarks.
- **cve_cache**: Local sync of relevant CVE data.
- **snapshots**: Before/after data points for patch comparison.
