import json
import os
from .base_scanner import BaseScanner

class OSScanner(BaseScanner):
    def run(self):
        if self.is_live():
            # In a real scenario we would execute_on_vm and parse results
            os_rel = self.execute_on_vm("cat /etc/os-release")
            # For simplicity, if it fails, fallback to demo
            if "Error" in os_rel or not os_rel:
                return self.get_demo_data()
            return {"data_source": "live", "os_info": {"raw": os_rel}}
        return self.get_demo_data()

    def get_demo_data(self):
        try:
            with open('demo_data/sample_scan_results.json', 'r') as f:
                data = json.load(f)
                return {
                    "data_source": "demo",
                    "os_info": data.get("os_info", {}),
                    "open_ports": data.get("open_ports", []),
                    "running_services": data.get("running_services", []),
                    "user_accounts": data.get("user_accounts", []),
                    "sysctl_findings": data.get("sysctl_findings", [])
                }
        except:
            return {"data_source": "demo", "error": "Demo data not found"}
