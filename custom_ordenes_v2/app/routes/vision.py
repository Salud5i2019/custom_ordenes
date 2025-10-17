from flask import Blueprint, request, Response, jsonify
from app.services.ocr_azure import extraer_texto_ocr_azure
from app.services.gpt_vision import detectar_firmas_gpt_vision
from app.utils.rut import normalizar_rut
from collections import OrderedDict
from flask_jwt_extended import jwt_required
import re
import json
import base64  # ← nuevo

vision_bp = Blueprint("vision", __name__)

RUT_ASOCIADOS = {
    "Asociación de Aseguradores de Chile": "8127800-9",
    "Provida": "76265736-8",
    "Cuprum": "76240079-0",
    "Instituto de Previsión Social": "61979440-0",
    "Planvital": "98001200-K",
    "Habitat": "98000100-8",
    "Modelo": "76726250-3",
    "Uno": "76960424-3",
    "Capital": "98000000-1"
}

@vision_bp.route("/detectar-datos-firma", methods=["POST"])
@jwt_required()
def detectar_datos_firma():
    if "file" not in request.files:
        return jsonify({"error": "No se proporcionó archivo."}), 400

    file = request.files["file"]
    filename = file.filename.lower()

    try:
        file_bytes = file.read()
        texto = extraer_texto_ocr_azure(file_bytes)
        print("📄 TEXTO OCR:\n", texto)

        def buscar(patron):
            match = re.search(patron, texto, re.IGNORECASE)
            return match.group(1).strip() if match else ""

        cedula = buscar(r"(?:C[eé]dula|RUT)\s*[:\-]?\s*([\dKk\-.]+)")
        if not cedula:
            cedula = buscar(r"C[eé]d\.?\s*Ident\.?\s*(?:Nº|:)?\s*([\dKk\-.]+)")

        campos = {
            "Orden": buscar(r"Orden\s*(?:Nº|nº)?\s*[:\-]?\s*(.*)"),
            "Expediente": buscar(r"Expediente\s*[:\-]?\s*(\S+)"),
            "Fecha Consulta": buscar(r"Fecha\s+Consulta\s*[:\-]?\s*([\d/-]+)"),
            "Medico": extraer_medico_desde_doctor(texto),
            "Especialidad": buscar(r"Especialidad\s*[:\-]?\s*([^\n\r]+)"),
            "Cedula Paciente": cedula
        }

        nombre_remitente = ""
        rut_remitente = ""
        for nombre, rut in RUT_ASOCIADOS.items():
            if nombre.lower() in texto.lower():
                nombre_remitente = nombre
                rut_remitente = rut
                break

        # ⚠️ Nuevo flujo: base64 → GPT-4 Vision
        image_base64 = base64.b64encode(file_bytes).decode("utf-8")
        firmas = detectar_firmas_gpt_vision(image_base64)

        resultado = OrderedDict()
        resultado["Orden"] = {
            "valor": campos["Orden"],
            "confianza": evaluar_confianza(campos["Orden"])
        }
        resultado["Expediente"] = {
            "valor": campos["Expediente"],
            "confianza": evaluar_confianza(campos["Expediente"])
        }
        resultado["Fecha Consulta"] = {
            "valor": campos["Fecha Consulta"],
            "confianza": evaluar_confianza(campos["Fecha Consulta"])
        }
        resultado["Medico"] = {
            "valor": campos["Medico"],
            "confianza": evaluar_confianza(campos["Medico"])
        }
        resultado["Especialidad"] = {
            "valor": campos["Especialidad"],
            "confianza": evaluar_confianza(campos["Especialidad"])
        }
        resultado["Cedula Paciente"] = {
            "valor": normalizar_rut(campos["Cedula Paciente"]),
            "confianza": evaluar_confianza(campos["Cedula Paciente"])
        }
        resultado["Remitente boleta o factura - Nombre"] = {
            "valor": nombre_remitente,
            "confianza": evaluar_confianza(nombre_remitente)
        }
        resultado["Remitente boleta o factura - RUT"] = {
            "valor": normalizar_rut(rut_remitente),
            "confianza": 1.0 if rut_remitente else 0.0
        }

        resultado["Firma Afiliado Certificada"] = detectar_certificacion_por_ocr(texto)
        resultado["Firma Afiliado"] = firmas.get("Firma Afiliado", {
            "valor": "NO",
            "detalle": "No detectado",
            "confianza": 0.0
        })
        resultado["Firma Comision"] = firmas.get("Firma Comision", {
            "valor": "NO",
            "detalle": "No detectado",
            "confianza": 0.0
        })

        return Response(json.dumps(resultado, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        return jsonify({
            "error": "Error al procesar el archivo.",
            "detalle": str(e)
        }), 500

def evaluar_confianza(valor):
    if not valor:
        return 0.0
    longitud = len(valor.strip())
    if longitud < 5:
        return 0.7
    elif longitud > 30:
        return 0.85
    else:
        return 0.9

def extraer_medico_desde_doctor(texto):
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if re.match(r"^\s*Doctor\s*$", linea.strip(), re.IGNORECASE):
            if i + 1 < len(lineas):
                return lineas[i + 1].strip()
    return ""

def detectar_certificacion_por_ocr(texto):
    texto = texto.lower()
    if "certifico" in texto and "no se firm" in texto:
        return {"valor": "SI", "detalle": "Texto indica validación manual de identidad", "confianza": 0.95}
    patrones_negativos = [
        r"no se firm[oó]",
        r"firma no realizada",
        r"firma no obtenida",
        r"no fue posible obtener firma",
        r"no se estamp[oó] huella"
    ]
    for patron in patrones_negativos:
        if re.search(patron, texto, re.IGNORECASE):
            return {"valor": "SI", "detalle": "Texto indica validación manual de identidad", "confianza": 0.95}
    return {"valor": "NO", "detalle": "No detectado", "confianza": 0.7}
