import json
from .base_scanner import BaseScanner

class CISScanner(BaseScanner):
    def run(self):
        if self.is_live():
            return self.get_demo_data() # Simulate for now
        return self.get_demo_data()

    def get_demo_data(self):
        try:
            with open('demo_data/cis_benchmarks.json', 'r') as f:
                benchmarks = json.load(f)
            
            passes = 0
            for b in benchmarks:
                b['status'] = 'PASS' if b['severity'] in ['low', 'medium'] else 'FAIL'
                if b['status'] == 'PASS': passes += 1
                
            compliance = (passes / len(benchmarks)) * 100 if benchmarks else 0
            return {
                "data_source": "demo",
                "compliance_percentage": compliance,
                "summary": {"pass": passes, "fail": len(benchmarks)-passes, "warn": 0},
                "checks": benchmarks
            }
        except:
            return {"data_source": "demo", "error": "Demo data not found"}
