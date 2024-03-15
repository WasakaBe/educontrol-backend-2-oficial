from database import db, TBL_ACTIVOS_CUENTA
from flask import Blueprint, jsonify, request

# Crear un blueprint para las rutas
user_active_cuenta_routes = Blueprint('user_active_cuenta_routes', __name__)


# Ruta para obtener solo los activos y bloqueadas solo eso aun no se vera de cuales cuentas estan act o bloq
@user_active_cuenta_routes.route('/activos-cuenta', methods=['GET'])
def get_all_activos_cuenta():
    activos_cuenta = TBL_ACTIVOS_CUENTA.query.all()
    result = [{'id_activos_cuenta': activo.id_activos_cuenta, 'nombre_activos_cuenta': activo.nombre_activos_cuenta} for activo in activos_cuenta]
    return jsonify({'activos_cuenta': result})

# Ruta para obtener un activo de cuenta por ID 
 #Ruta para obtener solo los activos y bloqueadas solo eso aun no se vera de cuales cuentas estan act o bloq
@user_active_cuenta_routes.route('/activos-cuenta/<int:activo_id>', methods=['GET'])
def get_activo_cuenta_by_id(activo_id):
    activo_cuenta = TBL_ACTIVOS_CUENTA.query.get(activo_id)
    if activo_cuenta:
        result = {'id_activos_cuenta': activo_cuenta.id_activos_cuenta, 'nombre_activos_cuenta': activo_cuenta.nombre_activos_cuenta}
        return jsonify({'activo_cuenta': result})
    return jsonify({'message': 'Activo de cuenta no encontrado'}), 404
