import json
from .base_scanner import BaseScanner

class ContainerScanner(BaseScanner):
    def run(self):
        if self.is_live():
            return self.get_demo_data()
        return self.get_demo_data()

    def get_demo_data(self):
        try:
            with open('demo_data/sample_scan_results.json', 'r') as f:
                data = json.load(f)
                return {
                    "data_source": "demo",
                    "docker_info": data.get("docker_info", {}),
                    "running_containers": data.get("running_containers", []),
                    "security_checks": data.get("container_security_checks", [])
                }
        except:
            return {"data_source": "demo", "error": "Demo data not found"}
