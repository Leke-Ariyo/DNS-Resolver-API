from flask import Blueprint, request, jsonify


validate_blueprint = Blueprint('validate', __name__)


@validate_blueprint.route('/v1/tools/validate', methods=['POST'])
def validate_ip():
    """Validate if the given input is a valid IPv4 address"""
    data = request.get_json()
    if not data or 'ip' not in data:
        return {'error': 'IP to validate is required'}, 400

    ip = data['ip']
    valid = (
        ip.count('.') == 3 and
        all(
            num.isdigit() and 0 <= int(num) <= 255
            for num in ip.split('.')
        )
    )
    return jsonify({'status': valid}), 200
