import json
from .base_scanner import BaseScanner

class CVEAnalyzer(BaseScanner):
    def run(self):
        if self.is_live():
            return self.get_demo_data()
        return self.get_demo_data()

    def get_demo_data(self):
        try:
            with open('demo_data/sample_cves.json', 'r') as f:
                cves = json.load(f)
            return {
                "data_source": "demo",
                "cve_list": cves,
                "statistics": {
                    "critical": len([c for c in cves if c['severity'].lower() == 'critical']),
                    "high": len([c for c in cves if c['severity'].lower() == 'high']),
                    "total": len(cves)
                }
            }
        except:
            return {"data_source": "demo", "error": "Demo data not found"}
