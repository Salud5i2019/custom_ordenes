# ✍️ Validador de Firmas Digitales con OpenAI

Este proyecto es una API en **Python + Flask** que permite validar la autenticidad de firmas en documentos (imágenes o PDFs) utilizando **inteligencia artificial con OpenAI (visión)**.  
El sistema identifica firmas en documentos, clasifica si son **firma de afiliado, firma certificada, firma de comisión o huella**, y entrega un resultado estructurado para uso en automatización documental.

---

## ✅ Instalación rápida

### 1. Requisitos previos
Asegúrate de tener instalado:

| Requisito | Versión recomendada |
|------------|--------------------|
| Python     | 3.11               |
| pip        | Última versión     |

---

### 2. Crear entorno virtual
Desde la carpeta del proyecto:

```bash
py -3.11 -m venv venv
3. Activar entorno virtual (Windows)
bash
Copiar código
venv\Scripts\activate
4. Instalar dependencias
bash
Copiar código
pip install --upgrade pip
pip install -r requirements.txt
5. Configurar variables de entorno
Crear un archivo .env con los siguientes valores:

ini
Copiar código
OPENAI_API_KEY=tu_api_key
JWT_SECRET_KEY=clave_de_seguridad
Ajustar según el entorno y configuración de seguridad.

🚀 Ejecutar el servicio
bash
Copiar código
python app.py
La API quedará disponible en:

arduino
Copiar código
http://localhost:5000
