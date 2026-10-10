from flask import Blueprint, jsonify
from models import get_vm_connection, get_patch_history

patches_bp = Blueprint('patches', __name__, url_prefix='/api/patches')

@patches_bp.route('/current', methods=['GET'])
@patches_bp.route('/current-version', methods=['GET'])
def get_current_version():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    cos_ver = vm.get('cos_version') if vm else "cos-101-17162.336.36"
    return jsonify({
        "data_source": data_source,
        "version": cos_ver,
        "current_version": cos_ver,
        "latest_available": "cos-109-17800.50.2",
        "updates_available": True
    })

@patches_bp.route('/history', methods=['GET'])
def get_history():
    history = get_patch_history()
    # Normalize for frontend PatchTimelineChart (expects: date, cves_fixed)
    normalized = []
    for h in history:
        normalized.append({
            'date': h.get('release_date', h.get('date', '')),
            'milestone': h.get('cos_milestone', ''),
            'version': h.get('build_number', ''),
            'cves_fixed': h.get('cve_fixes_count', h.get('cves_fixed', 0)),
        })
    return jsonify({"data_source": "demo", "history": normalized})

@patches_bp.route('/available', methods=['GET'])
def get_available_updates():
    return jsonify({
        "data_source": "demo",
        "updates": [
            {"version": "cos-105-17412.100.1", "cves_fixed": 15},
            {"version": "cos-109-17800.50.2", "cves_fixed": 18}
        ]
    })
