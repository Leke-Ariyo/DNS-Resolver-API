from flask import Blueprint, jsonify
from app.models import DNSQuery


history_blueprint = Blueprint('history', __name__)


@history_blueprint.route('/v1/history')
def dns_query_history():
    """List the last 20 DNS queries"""
    try:
        queries = DNSQuery.query.order_by(DNSQuery.id.desc()).limit(20).all()
        result = [{
            'domain': q.domain,
            'client_ip': q.client_ip,
            'addresses': q.addresses.split(','),
            'created_time': q.created_time
        } for q in queries]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f"Failed to retrieve query history: {e}"}), 500
