from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os

# Cargar variables de entorno
ENDPOINT = os.getenv("AZURE_CUSTOM_VISION_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_CUSTOM_VISION_KEY")
PROJECT_ID = os.getenv("AZURE_CUSTOM_VISION_PROJECT_ID")
MODEL_NAME = os.getenv("AZURE_CUSTOM_VISION_MODEL_NAME")

# Cliente
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

def detectar_firmas_custom_vision(image_bytes: bytes) -> dict:
    result = predictor.detect_image(
        project_id=PROJECT_ID,
        published_name=MODEL_NAME,
        image_data=image_bytes
    )

    firmas = {
        "Firma Afiliado": {"valor": "NO", "detalle": "No detectado", "confianza": 0.0},
        "Huella Afiliado": {"valor": "NO", "detalle": "No detectado", "confianza": 0.0},
        "Firma Comision": {"valor": "NO", "detalle": "No detectado", "confianza": 0.0}
    }

    for pred in result.predictions:
        tag = pred.tag_name
        prob = round(pred.probability, 3)
        print(f"🧠 Detectado: {tag} - {prob}")

        if prob < 0.6:
            continue

        if tag == "Firma Afiliado":
            firmas["Firma Afiliado"] = {"valor": "SI", "detalle": "Firma", "confianza": prob}
       
        elif tag == "Firma Comision":
            firmas["Firma Comision"] = {"valor": "SI", "detalle": "Firma", "confianza": prob}

        elif tag == "Huella Afiliado":
            firmas["Huella Afiliado"] = {"valor": "SI", "detalle": "Huella", "confianza": prob}

    return firmas
