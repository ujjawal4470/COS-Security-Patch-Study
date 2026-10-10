#!/usr/bin/env python3
"""Generate a security assessment report in Markdown format."""

import requests
import json
import os
from datetime import datetime

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")

def run():
    print(f"Connecting to {BACKEND_URL}...")
    try:
        # Trigger APIs or fetch latest
        assessment = requests.get(f"{BACKEND_URL}/api/assessment/latest").json()
        cis = requests.get(f"{BACKEND_URL}/api/cis/latest").json()
        network = requests.get(f"{BACKEND_URL}/api/network/analysis").json()
        container = requests.get(f"{BACKEND_URL}/api/container/security-checks").json()
        cve = requests.get(f"{BACKEND_URL}/api/cve/statistics").json()
        patch = requests.get(f"{BACKEND_URL}/api/patches/current-version").json()
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"reports/security-report-{timestamp}.md"

    with open(filepath, "w") as f:
        f.write("# Security Assessment Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Executive Summary\n")
        f.write("Automated security assessment of the Container-Optimized OS environment.\n\n")

        f.write("## OS Information\n")
        f.write(f"- Patch Status: {patch.get('version', 'Unknown')}\n\n")

        f.write("## Security Score\n")
        f.write(f"Score: {assessment.get('score', 'N/A')}/100\n\n")

        f.write("## CIS Compliance Results\n")
        f.write(f"Passed: {cis.get('passed', 0)}, Failed: {cis.get('failed', 0)}\n\n")

        f.write("## Network Security Analysis\n")
        f.write(f"Rules Evaluated: {len(network.get('rules', []))}\n\n")

        f.write("## Container Security Findings\n")
        f.write(f"Containers Scanned: {container.get('scanned_count', 0)}\n\n")

        f.write("## CVE Analysis\n")
        f.write(f"Total CVEs: {cve.get('total', 0)}\n\n")

        f.write("## Recommendations\n")
        f.write("Review the dashboard for detailed remediation steps.\n")

    print(f"Report generated successfully at {filepath}")

if __name__ == "__main__":
    run()
