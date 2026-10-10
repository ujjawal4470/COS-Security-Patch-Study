import subprocess
from abc import ABC, abstractmethod

class BaseScanner(ABC):
    def __init__(self, vm_info=None):
        self.vm_info = vm_info

    def is_live(self):
        return self.vm_info is not None and self.vm_info.get('status') == 'connected'

    def execute_on_vm(self, command):
        if not self.is_live():
            return ""
        
        project = self.vm_info.get('gcp_project')
        zone = self.vm_info.get('zone')
        instance = self.vm_info.get('instance_name')
        
        cmd = [
            "gcloud", "compute", "ssh", instance,
            f"--project={project}", f"--zone={zone}",
            "--command", command
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_demo_data(self):
        pass
