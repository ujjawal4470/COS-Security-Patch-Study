import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import init_db, get_db
from demo_data.seed import seed_demo_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)

    with app.app_context():
        init_db()
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM hardening_actions")
        if cursor.fetchone()[0] == 0:
            seed_demo_data(db)
        db.close()

    from routes.dashboard import dashboard_bp
    from routes.assessment import assessment_bp
    from routes.hardening import hardening_bp
    from routes.network import network_bp
    from routes.cis import cis_bp
    from routes.container import container_bp
    from routes.patches import patches_bp
    from routes.cve import cve_bp
    from routes.comparison import comparison_bp
    from routes.vm_connection import vm_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(hardening_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(cis_bp)
    app.register_blueprint(container_bp)
    app.register_blueprint(patches_bp)
    app.register_blueprint(cve_bp)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(vm_bp)

    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy", "demo_mode": app.config['DEMO_MODE']})

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
