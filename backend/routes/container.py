import json
from flask import Blueprint, jsonify
from models import get_vm_connection

container_bp = Blueprint('container', __name__, url_prefix='/api/container')

def get_demo_results():
    with open('demo_data/sample_scan_results.json', 'r') as f:
        return json.load(f)

# Frontend calls /container/info
@container_bp.route('/info', methods=['GET'])
@container_bp.route('/docker-info', methods=['GET'])
def get_docker_info():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    try:
        demo = get_demo_results()
        info = demo.get('docker_info', {})
    except Exception:
        info = {"version": "20.10.x", "storage_driver": "overlay2"}
    info['data_source'] = data_source
    return jsonify({"data_source": data_source, "info": info, **info})

@container_bp.route('/running', methods=['GET'])
def get_running_containers():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    try:
        demo = get_demo_results()
        containers = demo.get('running_containers', [])
    except Exception:
        containers = []
    return jsonify({"data_source": data_source, "containers": containers})

# Frontend calls /container/security
@container_bp.route('/security', methods=['GET'])
@container_bp.route('/security-checks', methods=['GET'])
def get_security_checks():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    try:
        demo = get_demo_results()
        checks = demo.get('container_security_checks', [])
    except Exception:
        checks = []
    return jsonify({"data_source": data_source, "checks": checks})
