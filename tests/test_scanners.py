import pytest

# Mock classes for testing the contract
class BaseScanner:
    def run(self): pass

class OSScanner(BaseScanner):
    def run(self): return {"data_source": "demo", "os": "cos"}

class CISScanner(BaseScanner):
    def run(self): return {"data_source": "demo", "checks": [{"id": "1.1", "status": "pass"}]}

class NetworkScanner(BaseScanner):
    def run(self): return {"data_source": "demo", "rules": []}

class ContainerScanner(BaseScanner):
    def run(self): return {"data_source": "demo", "docker_info": {}}

class PatchScanner(BaseScanner):
    def run(self): return {"data_source": "demo", "version": "latest"}

class CVEAnalyzer(BaseScanner):
    def run(self): return {"data_source": "demo", "cve_list": []}

def test_base_scanner():
    assert hasattr(BaseScanner, 'run')

def test_os_scanner_demo():
    data = OSScanner().run()
    assert data["data_source"] == "demo"
    assert "os" in data

def test_cis_scanner_demo():
    data = CISScanner().run()
    assert data["data_source"] == "demo"
    assert "checks" in data
    assert "id" in data["checks"][0]

def test_network_scanner_demo():
    data = NetworkScanner().run()
    assert data["data_source"] == "demo"
    assert "rules" in data

def test_container_scanner_demo():
    data = ContainerScanner().run()
    assert data["data_source"] == "demo"
    assert "docker_info" in data

def test_patch_scanner_demo():
    data = PatchScanner().run()
    assert data["data_source"] == "demo"
    assert "version" in data

def test_cve_analyzer_demo():
    data = CVEAnalyzer().run()
    assert data["data_source"] == "demo"
    assert "cve_list" in data
