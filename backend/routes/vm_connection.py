import subprocess
from flask import Blueprint, request, jsonify
from models import get_vm_connection, save_vm_connection, clear_vm_connection

vm_bp = Blueprint('vm_connection', __name__, url_prefix='/api/vm')

@vm_bp.route('/status', methods=['GET'])
def get_status():
    vm = get_vm_connection()
    if vm and vm.get('status') == 'connected':
        return jsonify({
            "data_source": "live",
            "connected": True,
            "mode": "live",
            "connection": vm
        })
    return jsonify({
        "data_source": "demo",
        "connected": False,
        "mode": "demo",
        "connection": {"status": "disconnected"}
    })

@vm_bp.route('/connect', methods=['POST'])
def connect_vm():
    data = request.json
    project = data.get('project')
    zone = data.get('zone')
    instance = data.get('instance')

    if not all([project, zone, instance]):
        return jsonify({"error": "Missing project, zone, or instance"}), 400

    try:
        cmd = ["gcloud", "compute", "instances", "describe", instance, f"--project={project}", f"--zone={zone}", "--format=value(status)"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and "RUNNING" in result.stdout:
            # For simplicity, simulating the version fetch
            save_vm_connection(project, zone, instance, "connected", "cos-101-17162.336.36")
            return jsonify({"data_source": "live", "status": "success", "message": "Connected successfully"})
        else:
            return jsonify({"data_source": "live", "status": "error", "message": "Instance not found or not running"}), 400
    except Exception as e:
        return jsonify({"data_source": "demo", "status": "error", "message": str(e)}), 500

@vm_bp.route('/disconnect', methods=['POST'])
def disconnect_vm():
    clear_vm_connection()
    return jsonify({"data_source": "demo", "status": "success", "message": "Disconnected"})
