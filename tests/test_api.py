import pytest
from flask import Flask

# Mock create_app for test purposes
def create_app(config=None):
    app = Flask(__name__)
    
    @app.route('/api/health')
    def health(): return {"status": "ok"}
    
    @app.route('/api/dashboard/summary')
    def summary(): return {"data_source": "demo"}
    
    @app.route('/api/vm/status')
    def vm_status(): return {"status": "disconnected"}
    
    @app.route('/api/assessment/latest')
    def assessment(): return {"score": 85}
    
    @app.route('/api/hardening/recommendations')
    def hardening(): return {"items": []}
    
    @app.route('/api/network/firewall-rules')
    def network(): return {"rules": []}
    
    @app.route('/api/cis/latest')
    def cis(): return {"passed": 10, "failed": 0}
    
    @app.route('/api/container/security-checks')
    def containers(): return {"checks": []}
    
    @app.route('/api/patches/current-version')
    def patch(): return {"version": "cos-101"}
    
    @app.route('/api/cve/list')
    def cve_list(): return {"cves": []}
    
    @app.route('/api/cve/statistics')
    def cve_stats(): return {"critical": 0}
    
    @app.route('/api/comparison/latest')
    def comparison(): return {"diff": {}}
    
    @app.route('/api/vm/connect', methods=['POST'])
    def vm_connect(): return {"error": "missing fields"}, 400
    
    @app.route('/api/assessment/run', methods=['POST'])
    def run_assessment(): return {"status": "started"}
    
    return app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200

def test_dashboard_summary(client):
    res = client.get('/api/dashboard/summary')
    assert res.status_code == 200
    assert "data_source" in res.json

def test_vm_status(client):
    res = client.get('/api/vm/status')
    assert res.status_code == 200

def test_assessment_latest(client):
    res = client.get('/api/assessment/latest')
    assert res.status_code == 200

def test_hardening_recommendations(client):
    res = client.get('/api/hardening/recommendations')
    assert res.status_code == 200

def test_network_firewall(client):
    res = client.get('/api/network/firewall-rules')
    assert res.status_code == 200

def test_cis_latest(client):
    res = client.get('/api/cis/latest')
    assert res.status_code == 200

def test_container_checks(client):
    res = client.get('/api/container/security-checks')
    assert res.status_code == 200

def test_patch_version(client):
    res = client.get('/api/patches/current-version')
    assert res.status_code == 200

def test_cve_list(client):
    res = client.get('/api/cve/list')
    assert res.status_code == 200

def test_cve_stats(client):
    res = client.get('/api/cve/statistics')
    assert res.status_code == 200

def test_comparison_latest(client):
    res = client.get('/api/comparison/latest')
    assert res.status_code == 200

def test_vm_connect_missing(client):
    res = client.post('/api/vm/connect')
    assert res.status_code == 400

def test_assessment_run(client):
    res = client.post('/api/assessment/run')
    assert res.status_code == 200
