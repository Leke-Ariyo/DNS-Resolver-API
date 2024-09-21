from flask import Blueprint, jsonify
import os
from datetime import datetime


# Initialize blueprint and API
status_blueprint = Blueprint('status', __name__)


@status_blueprint.route('/')
def home_status():
    """Return the current app status and whether it's running in Kubernetes"""
    kubernetes = True if os.getenv('KUBERNETES_SERVICE_HOST') else False
    return jsonify({
        "date": int(datetime.utcnow().timestamp()),  # Current UNIX timestamp
        "kubernetes": kubernetes,  # Boolean to see if the app runs in K8
        "version": "0.1.0"  # Application version
    })
