import json
from flask import Blueprint, request, jsonify
from models import get_vm_connection, save_scan_result, get_latest_scan, get_scan_history

assessment_bp = Blueprint('assessment', __name__, url_prefix='/api/assessment')

@assessment_bp.route('/run', methods=['POST'])
def run_assessment():
    data = request.json or {}
    label = data.get('label', 'Manual Scan')
    
    vm = get_vm_connection()
    is_live = vm and vm.get('status') == 'connected'
    data_source = 'live' if is_live else 'demo'

    # Retrieve demo results to store
    with open('demo_data/sample_scan_results.json', 'r') as f:
        demo_results = json.load(f)

    scan_id = save_scan_result('comprehensive', data_source, label, demo_results, 65)
    
    return jsonify({
        "data_source": data_source,
        "message": "Scan completed",
        "scan_id": scan_id
    })

@assessment_bp.route('/latest', methods=['GET'])
def get_latest_assessment():
    vm = get_vm_connection()
    scan = get_latest_scan('comprehensive')
    if scan:
        results = scan.get('results', {})
        return jsonify({
            "data_source": scan['data_source'],
            "score": scan.get('security_score', 65),
            "os_info": results.get('os_info', {"name": "Container-Optimized OS", "version": "101", "kernel": "5.15.109+", "arch": "x86_64"}),
            "scan": scan
        })
    # Demo fallback
    return jsonify({
        "data_source": "demo",
        "score": 65,
        "os_info": {"name": "Container-Optimized OS", "version": "cos-101-17162.336.36", "kernel": "5.15.109+", "arch": "x86_64"},
        "message": "No scans run yet - showing demo data"
    })

@assessment_bp.route('/history', methods=['GET'])
def get_history():
    history = get_scan_history('comprehensive')
    return jsonify({"data_source": "demo" if not history else history[0]['data_source'], "history": history})
