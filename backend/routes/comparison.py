from flask import Blueprint, jsonify, request
from models import get_latest_comparison, save_comparison_snapshot, get_db

comparison_bp = Blueprint('comparison', __name__, url_prefix='/api/comparison')

@comparison_bp.route('/latest', methods=['GET'])
def get_latest():
    res = get_latest_comparison()
    res['data_source'] = "demo"
    if 'before' in res and 'after' in res:
        res['improvement_delta'] = res['after']['overall_score'] - res['before']['overall_score']
    return jsonify(res)

@comparison_bp.route('/snapshot', methods=['POST'])
def create_snapshot():
    data = request.json
    label = data.get('label', 'BEFORE')
    scores = data.get('scores', {})
    scan_id = save_comparison_snapshot(label, scores, "demo")
    return jsonify({"data_source": "demo", "message": "Snapshot saved", "id": scan_id})

@comparison_bp.route('/history', methods=['GET'])
def get_history():
    db = get_db()
    rows = db.execute("SELECT * FROM comparison_snapshots ORDER BY id DESC").fetchall()
    return jsonify({"data_source": "demo", "history": [dict(r) for r in rows]})
