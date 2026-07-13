from flask import Flask
from src.analysis_api import bp_analysis # absolute imports
'''
Flask API app factory
'''

def create_app():
    app = Flask(__name__)

    try:
        from src.forecast_api import bp_core
    except Exception as exc:
        app.logger.warning("Skipping core blueprint registration: %s", exc)
    else:
        app.register_blueprint(bp_core, url_prefix="/api") # routes will be under /api/...

    app.register_blueprint(bp_analysis, url_prefix="/api/analytics")
    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
