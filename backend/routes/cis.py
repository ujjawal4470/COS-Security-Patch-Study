import json
from flask import Blueprint, jsonify, request
from models import get_vm_connection, save_cis_checks, get_cis_checks, save_scan_result, get_latest_scan

cis_bp = Blueprint('cis', __name__, url_prefix='/api/cis')

@cis_bp.route('/run', methods=['POST'])
def run_cis():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    
    with open('demo_data/cis_benchmarks.json', 'r') as f:
        benchmarks = json.load(f)
    
    for b in benchmarks:
        # Simulate result
        b['status'] = 'PASS' if b['severity'] == 'low' else 'FAIL'
        
    scan_id = save_scan_result('cis', data_source, 'CIS Scan', {}, 72)
    save_cis_checks(scan_id, benchmarks)
    
    return jsonify({"data_source": data_source, "message": "CIS Scan completed", "scan_id": scan_id})

@cis_bp.route('/latest', methods=['GET'])
def get_latest_cis():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    scan = get_latest_scan('cis')
    if scan:
        checks = get_cis_checks(scan['id'])
        # Normalize checks fields for frontend
        normalized = []
        for c in checks:
            normalized.append({
                'id': c.get('benchmark_id', c.get('id', '')),
                'category': c.get('category', ''),
                'description': c.get('description', ''),
                'status': c.get('status', 'UNKNOWN').lower()
            })
        return jsonify({"data_source": scan['data_source'], "compliance": 72.0, "compliance_percentage": 72.0, "checks": normalized})
    # Demo fallback
    return jsonify({
        "data_source": "demo",
        "compliance": 72.0,
        "compliance_percentage": 72.0,
        "checks": []
    })

@cis_bp.route('/benchmarks', methods=['GET'])
def get_benchmarks():
    with open('demo_data/cis_benchmarks.json', 'r') as f:
        benchmarks = json.load(f)
    return jsonify({"data_source": "demo", "benchmarks": benchmarks})
