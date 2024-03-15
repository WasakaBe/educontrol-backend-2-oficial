from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from database import db
from routes import user_routes
from user_rol_routes import user_rol_routes
from routes_sexs import user_sex_routes
from routes_active_cuenta import user_active_cuenta_routes
from routes_active_user import user_active_user_routes



from waitress import serve
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

app = Flask(__name__)
CORS(app)

# SQL SERVER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Telcel4773@WasakaBegeinTv/EDUCBTA52?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, SQLAlchemyError):
        return jsonify({'error': 'Error de la base de datos'}), 500
    return jsonify({'error': str(e)}), 500



# Registrar las rutas
app.register_blueprint(user_routes)
app.register_blueprint(user_rol_routes)
app.register_blueprint(user_sex_routes)
app.register_blueprint(user_active_cuenta_routes)
app.register_blueprint(user_active_user_routes)

@app.route('/')
def hello_world():
    return 'API CORRIENDO EDU CONTROL CBTA5 xxxx'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=50009)