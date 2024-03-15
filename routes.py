from database import db, TBL_USUARIOS2,BITACORA_SESION,BITACORA_USUARIOS
from flask import Blueprint, jsonify, request
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import hashlib



# Función para encriptar una contraseña
def encrypt_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Crear un blueprint para las rutas
user_routes = Blueprint('user_routes', __name__)
# Ruta para obtener todos los usuarios
@user_routes.route('/users/view', methods=['GET'])
def get_all_users():
    users = TBL_USUARIOS2.query.all()
    result = []
    for tbl_users in users:
        result.append({
            'id_usuario2': tbl_users.id_usuario2,
            'nombre_usuario2': tbl_users.nombre_usuario2,
            'app_usuario2': tbl_users.app_usuario2,
            'apm_usuario2': tbl_users.apm_usuario2,
            'fecha_nacimiento_usuario2': tbl_users.fecha_nacimiento_usuario2,
            'token_usuario2': tbl_users.token_usuario2,
            'correo_usuario2': tbl_users.correo_usuario2,
            'pwd_usuario2': tbl_users.pwd_usuario2,
            'foto_usuario2': tbl_users.foto_usuario2.decode('utf-8') if tbl_users.foto_usuario2 else None,
            'no_control_usuario2': tbl_users.no_control_usuario2,
            'phone_usuario2': tbl_users.phone_usuario2,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idUsuarioActivo': tbl_users.idUsuarioActivo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
        })
    return jsonify({'users': result})

 # Ruta para obtener un usuario por ID
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    tbl_users = TBL_USUARIOS2.query.get(user_id)
    if tbl_users:
        result = {
            'id_usuario2': tbl_users.id_usuario2,
            'nombre_usuario2': tbl_users.nombre_usuario2,
            'app_usuario2': tbl_users.app_usuario2,
            'apm_usuario2': tbl_users.apm_usuario2,
            'fecha_nacimiento_usuario2': tbl_users.fecha_nacimiento_usuario2,
            'token_usuario2': tbl_users.token_usuario2,
            'correo_usuario2': tbl_users.correo_usuario2,
            'pwd_usuario2': tbl_users.pwd_usuario2,
            'foto_usuario2': tbl_users.foto_usuario2.decode('utf-8') if tbl_users.foto_usuario2 else None,
            'no_control_usuario2': tbl_users.no_control_usuario2,
            'phone_usuario2': tbl_users.phone_usuario2,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idUsuarioActivo': tbl_users.idUsuarioActivo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
        }
        return jsonify({'tbl_users': result})
    return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para verificar la existencia del número de control
@user_routes.route('/users/check-no-control', methods=['POST'])
def check_no_control():
    data = request.json
    no_control_usuario2 = data.get('no_control_usuario2')

    existing_user = TBL_USUARIOS2.query.filter_by(no_control_usuario2=no_control_usuario2).first()

    if existing_user:
         return jsonify({'exists': True, 'message': 'El número de control ya se encuentra registrado'}), 200
    else:
         return jsonify({'exists': False}), 200



# Ruta para crear un nuevo usuario2 
@user_routes.route('/users/insert', methods=['POST'])
def create_user2():
    data = request.json
    no_control_existente = check_existing_data('no_control_usuario2', data['no_control_usuario2'])

    if no_control_existente:
        return jsonify({'message': 'Error: Datos duplicados', 'no_control_existente': no_control_existente}), 400

    # Obtener la dirección IP del usuario
    user_ip = request.remote_addr


    # Encriptar la contraseña con la sal
    hashed_password = encrypt_password(data['pwd_usuario2'])
    
    new_user2 = TBL_USUARIOS2(
        nombre_usuario2=data['nombre_usuario2'],
        app_usuario2=data['app_usuario2'],
        apm_usuario2=data.get('apm_usuario2'),
        fecha_nacimiento_usuario2=data.get('fecha_nacimiento_usuario2'),
        token_usuario2=data.get('token_usuario2'),
        correo_usuario2=data['correo_usuario2'],
        pwd_usuario2=hashed_password,  # Guardar la contraseña encriptada
        foto_usuario2=data.get('foto_usuario2').encode('utf-8') if data.get('foto_usuario2') else None,
        no_control_usuario2=data['no_control_usuario2'],
        phone_usuario2=data.get('phone_usuario2'),
        ip_usuario2=user_ip ,
        idRol=data['idRol'],
        idSexo=data['idSexo'],
        idUsuarioActivo=data.get('idUsuarioActivo'),
        idCuentaActivo=data.get('idCuentaActivo')
    )

    try:
        db.session.add(new_user2)
        db.session.commit()
        
        # Insertar un nuevo registro en BITACORA_USUARIOS
        new_bitacora = BITACORA_USUARIOS(
            ID_USUARIO=new_user2.id_usuario2,
            NOMBRE_USUARIO=new_user2.nombre_usuario2,
            ACCION_REALIZADA='Registro',
            DETALLES_ACCION='Usuario registrado exitosamente',
            FECHA_ACCESO=datetime.now(),
            IP_ACCESO=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()
        # Envío de correo electrónico después de agregar el usuario exitosamente
        send_email(data['correo_usuario2'], 'Bienvenido a la aplicación', data['nombre_usuario2'])

        
        print(f"Nuevo usuario2: {request.json['nombre_usuario2']}")
        return jsonify({'message': 'Usuario2 creado exitosamente'}), 201

    except Exception as e:
        # Manejar errores al agregar el usuario2
        print(f"Error al agregar usuario2: {str(e)}")
        return jsonify({'message': 'Error al crear el usuario2'}), 500

def send_email(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('email.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()
    
def check_existing_data(field_name, field_value):
    existing_user = TBL_USUARIOS2.query.filter_by(**{field_name: field_value}).first()
    return True if existing_user else False  

# Ruta para verificar la disponibilidad del correo
@user_routes.route('/check-email', methods=['POST'])
def check_email_availability():
    try:
        data = request.json
        existing_user = TBL_USUARIOS2.query.filter_by(correo_usuario2=data['correo_usuario2']).first()
        if existing_user:
            return jsonify({'exists': True}), 200
        return jsonify({'exists': False}), 200
    except SQLAlchemyError as e:
        print('Error en la verificación de correo:', str(e))
        return jsonify({'error': 'Error en la verificación de correo'}), 500
    
# Ruta para obtener el token a partir del correo
@user_routes.route('/get-token', methods=['POST'])
def get_token_by_email():
    data = request.json
    tbl_users = TBL_USUARIOS2.query.filter_by(correo_usuario2=data['correo_usuario2']).first()
    
    if tbl_users:
        send_token_notification(tbl_users.correo_usuario2, 'Notificación de inicio de sesión', tbl_users.token_usuario2)
        return jsonify({'token_usuario2': tbl_users.token_usuario2, 'id_usuario2': tbl_users.id_usuario2}), 200
    
    return jsonify({'message': 'Correo no encontrado'}), 404

# Añade esta función en tu código
def send_token_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('emailupdate.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()

    

@user_routes.route('/get-token-by-emai/<string:user_email>', methods=['GET'])
def get_token_by_emai(user_email):
    # Busca un usuario con el correo proporcionado
    tbl_user = TBL_USUARIOS2.query.filter_by(correo_usuario2=user_email).first()

    # Verifica si se encontró un usuario con el correo
    if tbl_user:
        return jsonify({'token_usuario2': tbl_user.token_usuario2}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    
# Ruta para actualizar la contraseña de un usuario por correo electrónico
@user_routes.route('/updates-password', methods=['POST'])
def updates_password():
    try:
        data = request.json
        correo = data.get('correo_usuario2')
        new_password = data.get('new_password')

        # Buscar al usuario por correo electrónico
        tbl_users = TBL_USUARIOS2.query.filter_by(correo_usuario2=correo).first()

        if tbl_users:
            # Verificar si la nueva contraseña es diferente de la anterior
            if tbl_users.pwd_usuario2 != new_password:
                # Actualizar la contraseña
                tbl_users.pwd_usuario2 = new_password
                db.session.commit()
                
                 # Insertar un nuevo registro en BITACORA_USUARIOS
                new_bitacora = BITACORA_USUARIOS(
                    ID_USUARIO=tbl_users.id_usuario2,
                    NOMBRE_USUARIO=tbl_users.nombre_usuario2,
                    ACCION_REALIZADA='Actualizacion',
                    DETALLES_ACCION='Usuario Actualizo exitosamente su password',
                    FECHA_ACCESO=datetime.now(),
                    IP_ACCESO=request.remote_addr
                )
                db.session.add(new_bitacora)
                db.session.commit()
                
                send_update_notification(tbl_users.correo_usuario2, 'Notificación de Actualizacion de Contraseña', tbl_users.nombre_usuario2)
                return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
            else:
                return jsonify({'message': 'La nueva contraseña debe ser diferente de la anterior'}), 400
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except SQLAlchemyError as e:
        print('Error al actualizar la contraseña:', str(e))
        return jsonify({'error': 'Error al actualizar la contraseña'}), 500
    
 # Añade esta función en tu código
def send_update_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('emailupdatepwd.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()   

# Ruta para el proceso de inicio de sesión
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    # Encripta la contraseña proporcionada por el usuario para compararla con la almacenada
    hashed_password = encrypt_password(data['pwd_usuario2'])
    tbl_users = TBL_USUARIOS2.query.filter_by(correo_usuario2=data['correo_usuario2'], pwd_usuario2=hashed_password).first()
    if tbl_users:
        result = {
            'id_usuario2': tbl_users.id_usuario2,
            'nombre_usuario2': tbl_users.nombre_usuario2,
            'app_usuario2': tbl_users.app_usuario2,
            'apm_usuario2': tbl_users.apm_usuario2,
            'fecha_nacimiento_usuario2': tbl_users.fecha_nacimiento_usuario2,
            'token_usuario2': tbl_users.token_usuario2,
            'correo_usuario2': tbl_users.correo_usuario2,
            'pwd_usuario2': tbl_users.pwd_usuario2,
            'foto_usuario2': tbl_users.foto_usuario2.decode('utf-8') if tbl_users.foto_usuario2 else None,
            'no_control_usuario2': tbl_users.no_control_usuario2,
            'phone_usuario2': tbl_users.phone_usuario2,
            'ip_usuario2':tbl_users.ip_usuario2,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idUsuarioActivo': tbl_users.idUsuarioActivo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
        }

         # Enviar la notificación de inicio de sesión
        send_login_notification(tbl_users.correo_usuario2, 'Notificación de inicio de sesión', tbl_users.nombre_usuario2)
        
        # Insertar un nuevo registro en BITACORA_SESION
        new_sesion = BITACORA_SESION(
            ID_USUARIO2=tbl_users.id_usuario2,
            NOMBRE_USUARIO2=tbl_users.nombre_usuario2,
            CORREO_USUARIO2=tbl_users.correo_usuario2,
            FECHA_INICIO=datetime.now(),
            IP_USUARIO2=request.remote_addr,
            URL_SOLICITADA=request.url
        )
        db.session.add(new_sesion)
        db.session.commit()
        
        return jsonify({'tbl_users': result})
    return jsonify({'message': 'Credenciales incorrectas'}), 401


# Añade esta función en tu código
def send_login_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('loginemail.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()