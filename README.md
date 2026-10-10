# Container-Optimized OS Hardening & Patch Study

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Node](https://img.shields.io/badge/Node-18%2B-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## Overview
This project is a comprehensive security dashboard and automated scanner for Google Cloud's Container-Optimized OS (COS). Designed as a cybersecurity study, it evaluates COS security posture, checks CIS benchmark compliance, and generates actionable hardening recommendations.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Quick Start](#quick-start)
- [GCP Setup](#gcp-setup)
- [Demo Mode vs Live Mode](#demo-mode-vs-live-mode)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
1. Automated Security Scanning
2. CIS Benchmark Compliance Checks
3. Live VM Connection (GCP)
4. Demo Mode (Mock Data fallback)
5. OS Hardening Recommendations
6. Network Firewall Analysis
7. Container Security Posture
8. CVE Vulnerability Matching
9. Patch Status Tracking
10. Before/After Comparison
11. Historical Assessment Tracking
12. Markdown Report Generation
13. RESTful JSON API
14. React Frontend Dashboard
15. SQLite Local Data Storage
16. Dockerized Full-Stack Deployment

## Architecture
```text
[ React Frontend ]  <-->  [ Flask REST API ]  <-->  [ SQLite DB ]
                                 |
                                 v
                    [ Security Scanners (Python) ]
                                 |
(Demo Mode) <---------+----------+----------+--------> (Live Mode)
[ Mock JSON ]                                          [ gcloud / SSH ]
                                                             |
                                                             v
                                                      [ GCP COS VM ]
```

## Tech Stack
| Component | Technology | Description |
|-----------|------------|-------------|
| Frontend  | React, Vite | Modern UI, Port 3000 (Nginx 80 in prod) |
| Backend   | Flask, Python | REST API, Port 5000 |
| Database  | SQLite | Local data persistence |
| Deployment| Docker Compose | Containerized environments |
| Cloud     | Google Cloud Platform | Target environment for scans |

## Screenshots
*(Placeholders for UI screenshots)*
- `docs/assets/dashboard.png`
- `docs/assets/cis_scan.png`

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- gcloud CLI (Optional, for Live Mode only)

### 1. Clone the repo
```bash
git clone <repository-url>
cd COS-Security-Patch-Study
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

### 4. Docker Deployment (Alternative)
```bash
docker-compose up --build
```

## GCP Setup
For connecting to live infrastructure, configure your GCP credentials. See [GCP Deployment Guide](docs/gcp-deployment.md) for detailed instructions on spinning up the COS VM and setting firewall rules.

## Demo Mode vs Live Mode
- **Demo Mode**: Requires NO cloud credentials. The backend serves static, realistic mock data for UI testing and development.
- **Live Mode**: The backend executes shell commands against a target GCP COS VM using `gcloud compute ssh` to gather real-time security data.

## API Reference
See [API Reference](docs/api-reference.md) for the complete list of endpoints.

## Project Structure
```text
COS-Security-Patch-Study/
├── backend/       # Flask API, DB, Scanners
├── frontend/      # React UI
├── scripts/       # Automation and GCP tools
├── docs/          # Project documentation
├── tests/         # Pytest test suite
├── docker-compose.yml
└── README.md
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

## Acknowledgments
- Google Cloud Platform (GCP)
- Center for Internet Security (CIS)
- National Vulnerability Database (NVD)
