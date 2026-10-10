from flask import Blueprint, jsonify
from models import get_vm_connection, get_latest_comparison, get_patch_history, get_cve_statistics, get_hardening_actions

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary', methods=['GET'])
def get_summary():
    vm = get_vm_connection()
    is_live = vm and vm.get('status') == 'connected'
    data_source = 'live' if is_live else 'demo'

    cve_stats = get_cve_statistics()
    hardening = get_hardening_actions()
    applied_h = sum(1 for h in hardening if h['status'] == 'applied')

    return jsonify({
        "data_source": data_source,
        "overall_score": 65,
        "score": 65,
        "cis_compliance": 72.0,
        "total_cves": cve_stats.get('total', 0),
        "critical_cves": cve_stats.get('critical', 0),
        "high_cves": cve_stats.get('high', 0),
        "patch_status": "2 Updates Available",
        "cos_version": vm.get('cos_version') if is_live else "cos-101-17162.336.36",
        "firewall_rules_count": 5,
        "containers_running": 3,
        "hardening_applied": applied_h,
        "hardening_total": len(hardening),
        "last_scan": "2024-01-15T10:30:00Z",
        "score_history": [
            {"date": "2023-11-01", "score": 42},
            {"date": "2024-01-15", "score": 65}
        ]
    })
