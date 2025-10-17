from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FirmaDeteccionLog(db.Model):
    __tablename__ = 'firma_deteccion_log'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    nombre_archivo = db.Column(db.String(255))
    usuario = db.Column(db.String(100))  # si ocupas autenticación puedes vincularlo
    exito = db.Column(db.Boolean, default=True)
    error_mensaje = db.Column(db.Text, nullable=True)

    orden = db.Column(db.String(100))
    orden_confianza = db.Column(db.Float)

    expediente = db.Column(db.String(100))
    expediente_confianza = db.Column(db.Float)

    fecha_consulta = db.Column(db.String(100))
    fecha_consulta_confianza = db.Column(db.Float)

    medico = db.Column(db.String(255))
    medico_confianza = db.Column(db.Float)

    especialidad = db.Column(db.String(255))
    especialidad_confianza = db.Column(db.Float)

    cedula_paciente = db.Column(db.String(100))
    cedula_paciente_confianza = db.Column(db.Float)

    remitente_boleta_nombre = db.Column(db.String(255))
    remitente_boleta_nombre_confianza = db.Column(db.Float)

    remitente_boleta_rut = db.Column(db.String(100))
    remitente_boleta_rut_confianza = db.Column(db.Float)

    firma_afiliado = db.Column(db.String(20))
    firma_afiliado_confianza = db.Column(db.Float)
    firma_afiliado_detalle = db.Column(db.String(100))
    firma_afiliado_detalle_confianza = db.Column(db.Float)

    firma_comision = db.Column(db.String(20))
    firma_comision_confianza = db.Column(db.Float)
