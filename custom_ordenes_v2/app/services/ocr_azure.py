import os
import requests
import time
from dotenv import load_dotenv

load_dotenv(override=True)  # importante

AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")  # sin slash final
AZURE_OCR_KEY = os.getenv("AZURE_OCR_KEY")

def extraer_texto_ocr_azure(image_bytes: bytes) -> str:
    """
    Utiliza Azure Read OCR para extraer texto plano desde una imagen o PDF.
    """
    url = f"{AZURE_OCR_ENDPOINT}/vision/v3.0/read/analyze"

    print("🧪 Endpoint cargado:", AZURE_OCR_ENDPOINT)

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_OCR_KEY,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(url, headers=headers, data=image_bytes)
    if response.status_code != 202:
        raise Exception(f"OCR Azure: Error en solicitud inicial ({response.status_code}): {response.text}")

    operation_url = response.headers["Operation-Location"]

    # Esperar y consultar resultado
    for _ in range(10):
        result = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": AZURE_OCR_KEY})
        result_json = result.json()

        if result_json.get("status") == "succeeded":
            lineas = []
            for lectura in result_json["analyzeResult"]["readResults"]:
                for linea in lectura["lines"]:
                    lineas.append(linea["text"])
            
            texto_final = "\n".join(lineas)
            print("📄 TEXTO EXTRAÍDO POR OCR:\n", texto_final)  # 👈 aquí el log por pantalla
            return texto_final
        
        elif result_json.get("status") == "failed":
            raise Exception("OCR Azure: Falló el análisis del documento.")

        time.sleep(1)  # esperar antes de volver a consultar

    raise TimeoutError("OCR Azure: Se agotó el tiempo de espera para obtener resultados.")
