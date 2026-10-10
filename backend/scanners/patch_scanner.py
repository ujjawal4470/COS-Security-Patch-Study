from .base_scanner import BaseScanner

class PatchScanner(BaseScanner):
    def run(self):
        if self.is_live():
            return self.get_demo_data()
        return self.get_demo_data()

    def get_demo_data(self):
        return {
            "data_source": "demo",
            "current_version": "cos-101-17162.336.36",
            "latest_available": "cos-109-17800.50.2",
            "updates_available": True,
            "patches_behind": 3
        }
