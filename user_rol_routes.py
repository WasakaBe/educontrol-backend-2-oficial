from database import db, TBL_TIPO_ROL
from flask import Blueprint, jsonify, request
import smtplib
import os

# Crear un blueprint para las rutas
user_rol_routes = Blueprint('user_rol_routes', __name__)
# Ruta para obtener todos los tipos de roles
@user_rol_routes.route('/tipos-rol', methods=['GET'])
def get_all_tipos_rol():
    tipos_rol = TBL_TIPO_ROL.query.all()
    result = [{'id_tipo_rol': tipo_rol.id_tipo_rol, 'nombre_tipo_rol': tipo_rol.nombre_tipo_rol} for tipo_rol in tipos_rol]
    return jsonify({'tipos_rol': result})

# Ruta para obtener un tipo de rol por ID
@user_rol_routes.route('/tipos-rol/<int:tipo_rol_id>', methods=['GET'])
def get_tipo_rol_by_id(tipo_rol_id):
    tipo_rol = TBL_TIPO_ROL.query.get(tipo_rol_id)
    if tipo_rol:
        result = {'id_tipo_rol': tipo_rol.id_tipo_rol, 'nombre_tipo_rol': tipo_rol.nombre_tipo_rol}
        return jsonify({'tipo_rol': result})
    return jsonify({'message': 'Tipo de rol no encontrado'}), 404
