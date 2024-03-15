from database import db, TBL_SEXOS
from flask import Blueprint, jsonify, request
# Crear un blueprint para las rutas
user_sex_routes = Blueprint('user_sex_routes', __name__)

# Ruta para obtener todos los sexos
@user_sex_routes.route('/sexs', methods=['GET'])
def get_all_sexs():
    sexs = TBL_SEXOS.query.all()
    result = [{'id_sexos': sex.id_sexos, 'nombre_sexo': sex.nombre_sexo} for sex in sexs]
    return jsonify({'sexs': result})
# Ruta para obtener un sexo por ID
@user_sex_routes.route('/sexs/<int:sex_id>', methods=['GET'])
def get_sex_by_id(sex_id):
    sex = TBL_SEXOS.query.get(sex_id)
    if sex:
        result = {'id_sexos': sex.id_sexos, 'nombre_sexo': sex.nombre_sexo}
        return jsonify({'sex': result})
    return jsonify({'message': 'Sexo no encontrado'}), 404
