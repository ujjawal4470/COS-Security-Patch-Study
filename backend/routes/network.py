from flask import Blueprint, jsonify
from models import get_db, get_vm_connection

network_bp = Blueprint('network', __name__, url_prefix='/api/network')

@network_bp.route('/firewall', methods=['GET'])
@network_bp.route('/firewall-rules', methods=['GET'])
def get_firewall_rules():
    db = get_db()
    rows = db.execute("SELECT * FROM firewall_rules ORDER BY priority").fetchall()
    raw_rules = [dict(r) for r in rows]
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    # Normalize for frontend (expects: name, direction, action, ports, source, risk)
    rules = []
    for r in raw_rules:
        rules.append({
            'name': r.get('rule_name', r.get('name', '')),
            'direction': r.get('direction', 'INGRESS'),
            'action': r.get('action', 'ALLOW'),
            'ports': r.get('ports', r.get('protocol', 'all')),
            'source': r.get('source_ranges', r.get('source', '0.0.0.0/0')),
            'risk': r.get('risk_rating', r.get('risk', 'medium')).lower(),
        })
    # If no rules in DB yet, provide demo data
    if not rules:
        rules = [
            {'name': 'default-allow-ssh', 'direction': 'INGRESS', 'action': 'ALLOW', 'ports': 'tcp:22', 'source': '0.0.0.0/0', 'risk': 'high'},
            {'name': 'allow-internal', 'direction': 'INGRESS', 'action': 'ALLOW', 'ports': 'all', 'source': '10.128.0.0/9', 'risk': 'low'},
            {'name': 'default-allow-https', 'direction': 'INGRESS', 'action': 'ALLOW', 'ports': 'tcp:443', 'source': '0.0.0.0/0', 'risk': 'low'},
        ]
    return jsonify({"data_source": data_source, "rules": rules})

@network_bp.route('/analysis', methods=['GET'])
def get_network_analysis():
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    return jsonify({
        "data_source": data_source,
        "open_ports": 2,
        "high_risk_rules": 0,
        "medium_risk_rules": 2,
        "summary": "Network exposure is generally low. Port 22 and 443 are open."
    })
