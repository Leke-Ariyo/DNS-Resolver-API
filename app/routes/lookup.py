from flask import Blueprint, request, jsonify
import socket
import time
from app.models import DNSQuery
from app import (
    db,
    dns_lookup_total,
    dns_lookup_success,
    dns_lookup_failure,
    dns_lookup_duration
)

lookup_blueprint = Blueprint('lookup', __name__)


@lookup_blueprint.route('/tools/lookup')
def dns_lookup():
    """Resolve the IPv4 addresses for a given domain"""
    domain = request.args.get('domain')
    if not domain:
        return {'error': 'Domain parameter is required'}, 400

    dns_lookup_total.inc()
    start_time = time.time()

    try:
        ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        ipv4_addresses = [ip for ip in ipv4_addresses if ":" not in ip]

        if not ipv4_addresses:
            dns_lookup_failure.inc()
            return {'error': 'No IPv4 addresses found'}, 404

        new_query = DNSQuery(
            domain=domain,
            addresses=','.join(ipv4_addresses),
            client_ip=request.remote_addr
        )
        db.session.add(new_query)
        db.session.commit()

        dns_lookup_success.inc()
        dns_lookup_duration.observe(time.time() - start_time)

        return jsonify({
            'queryID': new_query.id,
            'domain': domain,
            'addresses': ipv4_addresses,
            'client_ip': new_query.client_ip,
            'created_time': new_query.created_time
        }), 200
    except socket.gaierror:
        dns_lookup_failure.inc()
        return jsonify({'error': 'DNS resolution failed'}), 404
    except Exception:
        dns_lookup_failure.inc()
        return jsonify({'error': 'Internal server error'}), 500
