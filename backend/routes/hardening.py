from flask import Blueprint, jsonify, request
from models import get_hardening_actions, update_hardening_status, get_vm_connection

hardening_bp = Blueprint('hardening', __name__, url_prefix='/api/hardening')

@hardening_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    actions = get_hardening_actions()
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    # Normalize fields for frontend (expects 'actions' list with 'id', 'category', 'title', 'status')
    normalized = []
    for a in actions:
        normalized.append({
            'id': a.get('action_id', a.get('id', '')),
            'category': a.get('category', 'General'),
            'title': a.get('title', a.get('action_name', '')),
            'description': a.get('description', ''),
            'status': a.get('status', 'pending'),
            'risk_level': a.get('risk_level', 'MEDIUM'),
            'priority': a.get('risk_level', 'MEDIUM'),
        })
    return jsonify({"data_source": data_source, "actions": normalized, "recommendations": normalized})

@hardening_bp.route('/status', methods=['GET'])
def get_hardening_status():
    actions = get_hardening_actions()
    total = len(actions)
    applied = sum(1 for a in actions if a['status'] == 'applied')
    pending = total - applied
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    return jsonify({"data_source": data_source, "total": total, "applied": applied, "pending": pending})

# Frontend calls POST /api/hardening/apply with body {actionId: ...}
@hardening_bp.route('/apply', methods=['POST'])
def apply_hardening_body():
    data = request.json or {}
    action_id = data.get('actionId', data.get('action_id'))
    if not action_id:
        return jsonify({"error": "actionId required"}), 400
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    update_hardening_status(action_id, 'applied')
    return jsonify({"data_source": data_source, "status": "success", "message": f"Action {action_id} applied"})

# Also support URL-param form
@hardening_bp.route('/apply/<action_id>', methods=['POST'])
def apply_hardening(action_id):
    vm = get_vm_connection()
    data_source = 'live' if vm and vm.get('status') == 'connected' else 'demo'
    update_hardening_status(action_id, 'applied')
    return jsonify({"data_source": data_source, "status": "success", "message": f"Action {action_id} applied"})
