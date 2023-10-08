from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import Cliente
from app.schemas import ClienteSchema
from app import db
from app.utils import require_static_token
cliente_bp = Blueprint('cliente_bp', __name__)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

@cliente_bp.route('/', methods=['POST'])
@require_static_token
def agregar_cliente():
    try:
        email = request.json['email']
        app_uuid = request.json['app_uuid']
        blocked_reason = request.json.get('blocked_reason', None) 
        datetime_request = datetime.now()  
        ip_request = request.remote_addr
        nuevo_cliente = Cliente(app_uuid, email, blocked_reason, datetime_request, ip_request)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({'id': nuevo_cliente.id, 'message': 'Cliente creado correctamente'})
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@cliente_bp.route('/<string:email>', methods=['GET'])
@require_static_token
def obtener_cliente_por_email(email):
    cliente = Cliente.query.filter_by(email=email).first()
    if cliente is None:
        return jsonify({'is_blacklisted': False})
    return jsonify({'is_blacklisted': True,
                    'reason': cliente.blocked_reason})

