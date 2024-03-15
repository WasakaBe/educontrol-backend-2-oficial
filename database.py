from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class TBL_TIPO_ROL(db.Model):
    id_tipo_rol = db.Column(db.Integer, primary_key=True)
    nombre_tipo_rol = db.Column(db.String(255), nullable=False)
class TBL_PREGUNTAS(db.Model):
    id_preguntas = db.Column(db.Integer, primary_key=True)
    nombre_preguntas = db.Column(db.String(255), nullable=False)
class TBL_SEXOS(db.Model):
    id_sexos = db.Column(db.Integer, primary_key=True)
    nombre_sexo = db.Column(db.String(10))
class TBL_ACTIVOS_USUARIO(db.Model):
    id_activo_usuario = db.Column(db.Integer, primary_key=True)
    nombre_activo_usuario = db.Column(db.String(30))
class TBL_ACTIVOS_CUENTA(db.Model):
    id_activos_cuenta = db.Column(db.Integer, primary_key=True)
    nombre_activos_cuenta = db.Column(db.String(30))
class TBL_USUARIOS2(db.Model):
    id_usuario2 = db.Column(db.Integer, primary_key=True)
    nombre_usuario2 = db.Column(db.String(255), nullable=False)
    app_usuario2 = db.Column(db.String(255), nullable=False)
    apm_usuario2 = db.Column(db.String(255))
    fecha_nacimiento_usuario2 = db.Column(db.DateTime, nullable=True)
    token_usuario2 = db.Column(db.String(20))
    correo_usuario2 = db.Column(db.String(255), unique=True, nullable=False)
    pwd_usuario2 = db.Column(db.String(255), nullable=False)
    foto_usuario2 = db.Column(db.LargeBinary)
    no_control_usuario2 = db.Column(db.BigInteger, unique=True)
    phone_usuario2 = db.Column(db.BigInteger)
    ip_usuario2 = db.Column(db.BigInteger)
    idRol = db.Column(db.Integer)
    idSexo = db.Column(db.Integer)
    idUsuarioActivo = db.Column(db.Integer)
    idCuentaActivo = db.Column(db.Integer)

    
class BITACORA_SESION(db.Model):
    id_sesion = db.Column(db.Integer,primary_key=True)
    ID_USUARIO2 = db.Column(db.Integer)
    NOMBRE_USUARIO2 = db.Column(db.String(255),nullable=False)
    CORREO_USUARIO2 = db.Column(db.String(255), nullable=False)
    FECHA_INICIO = db.Column(db.DateTime, nullable=True)
    IP_USUARIO2 = db.Column(db.BigInteger)
    URL_SOLICITADA = db.Column(db.String(255), nullable=False)
class BITACORA_USUARIOS(db.Model):
    ID_BITACORA = db.Column(db.Integer,primary_key=True)
    ID_USUARIO = db.Column(db.Integer)
    NOMBRE_USUARIO = db.Column(db.String(255),nullable=False)
    ACCION_REALIZADA = db.Column(db.String(255), nullable=False)
    DETALLES_ACCION = db.Column(db.String(255), nullable=False)
    FECHA_ACCESO =db.Column(db.DateTime, nullable=True)
    IP_ACCESO = db.Column(db.BigInteger)