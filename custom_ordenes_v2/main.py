from app import create_app
from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(".env")
# print("🧪 Cargando .env desde:", dotenv_path)

load_dotenv(dotenv_path, override=True)

# print("🔥 OCR endpoint cargado:", repr(os.getenv("AZURE_OCR_ENDPOINT")))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
