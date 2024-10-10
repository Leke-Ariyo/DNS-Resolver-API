from flask import Blueprint, jsonify, make_response, current_app
from app import db
from sqlalchemy import text


health_blueprint = Blueprint('health', __name__)


@health_blueprint.route('/health')
def health_status():
    health = {}

    # Check database connection
    try:
        db.session.execute(text('SELECT 1'))
        health['database'] = 'OK'
    except Exception as e:
        health['database'] = 'Error'
        health['database_error'] = str(e)

    # Check /metrics endpoint
    try:
        with current_app.test_client() as client:
            response = client.get('/metrics')
            if response.status_code == 200:
                health['metrics_endpoint'] = 'OK'
            else:
                health['metrics_endpoint'] = 'Error'
                health['metrics_error'] = f'Status Code {response.status_code}'
    except Exception as e:
        health['metrics_endpoint'] = 'Error'
        health['metrics_error'] = str(e)

    # Determine overall status
    overall_status = 'OK'
    http_status_code = 200

    for key in ['database', 'metrics_endpoint']:
        if health.get(key) != 'OK':
            overall_status = 'Error'
            http_status_code = 503
            break

    health['status'] = overall_status

    # Return response with appropriate HTTP status code
    response = make_response(jsonify(health), http_status_code)
    return response
