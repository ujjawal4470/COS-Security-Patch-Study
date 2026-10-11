import json
import os
import re
from .base_scanner import BaseScanner


class OSScanner(BaseScanner):
    def run(self):
        if not self.is_live():
            return self.get_demo_data()

        # Read-only commands executed on the connected VM.
        release = self.execute_on_vm("cat /etc/os-release")
        if not release or release.startswith("Error:"):
            raise RuntimeError(
                "Could not read OS information from the VM: " + str(release)
            )

        kernel = self.execute_on_vm("uname -r")
        uptime = self.execute_on_vm("uptime -p")
        arch = self.execute_on_vm("uname -m")

        if any(
            not value or value.startswith("Error:")
            for value in (kernel, arch)
        ):
            raise RuntimeError("Failed to collect required OS details from VM")

        os_name = "Unknown"
        version = "Unknown"
        for line in release.splitlines():
            match = re.match(r'^(NAME|VERSION_ID)="?(.*?)"?$', line)
            if match:
                if match.group(1) == "NAME":
                    os_name = match.group(2)
                elif match.group(1) == "VERSION_ID":
                    version = match.group(2)

        ports_output = self.execute_on_vm("ss -lnt")
        services_output = self.execute_on_vm(
            "systemctl list-units --type=service --state=running --no-legend"
        )
        users_output = self.execute_on_vm(
            "cut -d: -f1 /etc/passwd"
        )

        sysctl_findings = []
        for key, recommended in (
            ("net.ipv4.ip_forward", "0"),
            ("net.ipv4.tcp_syncookies", "1"),
            ("kernel.dmesg_restrict", "1"),
        ):
            value = self.execute_on_vm("sysctl -n " + key)
            if not value or value.startswith("Error:"):
                status = "UNKNOWN"
                value = "Unavailable"
            else:
                status = "PASS" if value.strip() == recommended else "FAIL"

            sysctl_findings.append({
                "key": key,
                "value": value.strip(),
                "recommended": recommended,
                "status": status,
            })

        open_ports = []
        if ports_output and not ports_output.startswith("Error:"):
            for line in ports_output.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    address = parts[3]
                    port = address.rsplit(":", 1)[-1]
                    open_ports.append({
                        "port": port,
                        "protocol": "tcp",
                        "service": "unknown",
                    })

        running_services = []
        if services_output and not services_output.startswith("Error:"):
            for line in services_output.splitlines():
                parts = line.split()
                if parts:
                    running_services.append(parts[0])

        user_accounts = []
        if users_output and not users_output.startswith("Error:"):
            user_accounts = [
                line.strip() for line in users_output.splitlines()
                if line.strip()
            ]

        return {
            "data_source": "live",
            "os_info": {
                "os": os_name,
                "name": os_name,
                "version": version,
                "kernel": kernel.strip(),
                "architecture": arch.strip(),
                "arch": arch.strip(),
                "uptime": uptime.strip() if uptime and not uptime.startswith("Error:") else "Unavailable",
            },
            "open_ports": open_ports,
            "running_services": running_services,
            "user_accounts": user_accounts,
            "sysctl_findings": sysctl_findings,
            "container_security_checks": [],
            "scan_notes": [
                "Only read-only OS checks were performed.",
                "Container checks are not implemented in this live scan yet."
            ],
        }


    def run_local(self):
        """Collect read-only security observations from this Cloud Shell host."""
        import platform
        import subprocess
        from pathlib import Path

        def command(args):
            try:
                result = subprocess.run(
                    args, capture_output=True, text=True, timeout=10, check=False
                )
                if result.returncode != 0:
                    return ""
                return result.stdout.strip()
            except (OSError, subprocess.TimeoutExpired):
                return ""

        release_text = Path("/etc/os-release").read_text(errors="replace")
        release = {}
        for line in release_text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                release[key] = value.strip().strip('"')

        def sysctl_check(key, recommended):
            value = command(["sysctl", "-n", key])
            if not value:
                return {"setting": key, "value": "UNKNOWN",
                        "recommended": str(recommended), "status": "UNKNOWN"}
            ok = value == str(recommended)
            return {"setting": key, "value": value,
                    "recommended": str(recommended),
                    "status": "PASS" if ok else "FAIL"}

        ports_text = command(["ss", "-lnt"])
        open_ports = []
        for line in ports_text.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4:
                address = parts[3]
                port = address.rsplit(":", 1)[-1]
                open_ports.append({
                    "protocol": "tcp",
                    "address": address,
                    "port": port,
                    "source": "ss -lnt"
                })

        accounts_text = command(["cut", "-d:", "-f1", "/etc/passwd"])
        users = [u for u in accounts_text.splitlines() if u]
        uptime = command(["uptime", "-p"])
        disk = command(["df", "-h", "/"])

        return {
            "data_source": "live",
            "target_type": "cloud_shell",
            "target_name": "Google Cloud Shell (Ubuntu host)",
            "os_info": {
                "name": release.get("PRETTY_NAME", platform.system()),
                "version": release.get("VERSION_ID", "unknown"),
                "kernel": platform.release(),
                "architecture": platform.machine(),
                "uptime": uptime or "Unavailable"
            },
            "open_ports": open_ports,
            "running_services": [],
            "user_accounts": users,
            "sysctl_findings": [
                sysctl_check("net.ipv4.ip_forward", 0),
                sysctl_check("net.ipv4.tcp_syncookies", 1),
                sysctl_check("kernel.dmesg_restrict", 1)
            ],
            "container_security_checks": [],
            "scan_notes": [
                "Read-only scan of the Cloud Shell Ubuntu environment.",
                "This is not a scan of a Container-Optimized OS (COS) VM.",
                "Running services and container security checks were not assessed."
            ],
            "uptime": uptime,
            "disk_usage": disk
        }

    def get_demo_data(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "demo_data",
            "sample_scan_results.json",
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "data_source": "demo",
            **data,
        }
