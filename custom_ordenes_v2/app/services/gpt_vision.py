import openai
import os
import json
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

def detectar_firmas_gpt_vision(image_base64: str) -> dict:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                                "text": (
                                    "Indica si hay alguna firma en el documento.\n\n"
                                    "Responde en formato JSON con exactamente dos claves: 'Firma Afiliado' y 'Firma Comision'.\n\n"
                                    "Cada una debe contener:\n"
                                    "- 'valor': SI o NO\n"
                                    "- 'detalle': una breve descripción como: Se detecta alguna firma o no se detecta ninguna firma , etc.\n"
                                    "- 'confianza': número entre 0.0 y 1.0\n\n"
                                    "Ejemplo de respuesta:\n"
                                    "{\n"
                                    "  \"Firma Afiliado\": {\n"
                                    "    \"valor\": \"SI\",\n"
                                    "    \"detalle\": \"Firma/huella visible\",\n"
                                    "    \"confianza\": 0.95\n"
                                    "  },\n"
                                    "  \"Firma Comision\": {\n"
                                    "    \"valor\": \"NO\",\n"
                                    "    \"detalle\": \"Firma presente / no presente \",\n"
                                    "    \"confianza\": 0.90\n"
                                    "  }\n"
                                    "}"
                                )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        content = response.choices[0].message.content
        # print("🧠 Respuesta cruda de GPT-4o:\n", content)
        # Intenta parsear directamente
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Si viene con markdown ```json ... ```
            match = re.search(r"```(?:json)?\n(.*?)\n```", content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            else:
                raise ValueError("GPT no devolvió un JSON reconocible.")

    except Exception as e:
        raise RuntimeError(f"Error usando GPT Vision: {str(e)}")
