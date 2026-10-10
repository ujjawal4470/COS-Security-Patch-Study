from .base_scanner import BaseScanner

class NetworkScanner(BaseScanner):
    def run(self):
        if self.is_live():
            # gcloud compute firewall-rules list ...
            return {"data_source": "live", "firewall_rules": []}
        return self.get_demo_data()

    def get_demo_data(self):
        rules = [
            {"rule_name": "default-allow-ssh", "direction": "INGRESS", "action": "ALLOW", "ports": "22", "source_ranges": "0.0.0.0/0", "risk_rating": "high", "priority": 65534},
            {"rule_name": "default-allow-icmp", "direction": "INGRESS", "action": "ALLOW", "protocol": "icmp", "source_ranges": "0.0.0.0/0", "risk_rating": "medium", "priority": 65534}
        ]
        return {"data_source": "demo", "firewall_rules": rules, "analysis": {"risk": "medium"}}
