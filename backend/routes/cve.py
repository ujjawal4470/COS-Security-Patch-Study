from flask import Blueprint, jsonify, request
from models import get_cve_list, get_cve_statistics

cve_bp = Blueprint('cve', __name__, url_prefix='/api/cve')

@cve_bp.route('/list', methods=['GET'])
def list_cves():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    severity = request.args.get('severity')
    
    cves, total = get_cve_list(page, per_page, severity)
    # Normalize for frontend CVETable (expects: id, severity, cvss, description, status)
    normalized = []
    for c in cves:
        normalized.append({
            'id': c.get('cve_id', c.get('id', '')),
            'severity': c.get('severity', 'UNKNOWN').upper(),
            'cvss': c.get('cvss_score', c.get('cvss', 0.0)),
            'description': c.get('description', ''),
            'status': c.get('patch_status', c.get('status', 'unknown')),
            'affected_versions': c.get('affected_versions', ''),
            'fixed_in': c.get('fixed_in_version', ''),
            'reference_url': c.get('reference_url', ''),
        })
    return jsonify({
        "data_source": "demo",
        "cves": normalized,
        "total": total,
        "page": page,
        "per_page": per_page
    })

@cve_bp.route('/statistics', methods=['GET'])
def get_statistics():
    stats = get_cve_statistics()
    return jsonify({"data_source": "demo", "statistics": stats})

@cve_bp.route('/<cve_id>', methods=['GET'])
def get_cve(cve_id):
    cves, _ = get_cve_list(1, 100)
    for c in cves:
        if c['cve_id'] == cve_id:
            return jsonify({"data_source": "demo", "cve": c})
    return jsonify({"error": "CVE not found"}), 404
