from database import db,TBL_ACTIVOS_USUARIO
from flask import Blueprint, jsonify, request

# Crear un blueprint para las rutas
user_active_user_routes = Blueprint('user_active_user_routes', __name__)

# Ruta para obtener todos los datos de activos 
@user_active_user_routes.route('/activos-usuario', methods=['GET'])
def get_all_activos_usuario():
    activos_usuario = TBL_ACTIVOS_USUARIO.query.all()
    result = [{'id_activo_usuario': activo.id_activo_usuario, 'nombre_activo_usuario': activo.nombre_activo_usuario} for activo in activos_usuario]
    return jsonify({'activos_usuario': result})

# Ruta para obtener un activo de la tabla por ID
@user_active_user_routes.route('/activos-usuario/<int:activo_id>', methods=['GET'])
def get_activo_usuario_by_id(activo_id):
    activo_usuario = TBL_ACTIVOS_USUARIO.query.get(activo_id)
    if activo_usuario:
        result = {'id_activo_usuario': activo_usuario.id_activo_usuario, 'nombre_activo_usuario': activo_usuario.nombre_activo_usuario}
        return jsonify({'activo_usuario': result})
    return jsonify({'message': 'Activo de usuario no encontrado'}), 404

