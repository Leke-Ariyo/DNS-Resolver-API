from flask import Blueprint, jsonify


# Create a Flask blueprint
health_blueprint = Blueprint('health', __name__)


# Define a route for the /health endpoint
@health_blueprint.route('/health')
def health_status():
    # Check the health status of the application
    return jsonify({"status": "OK"})
