import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", default="models/embedding-001")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", default="gemini-2.0-flash-exp")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", default="text-embedding-3-small")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
PDF_PATH = os.getenv("PDF_PATH")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
K_RESULTS = 10

if __name__ == "__main__":
    print("🔧 Configurações carregadas:")
    print(f"  - GOOGLE_API_KEY: {'✅ Definida' if GOOGLE_API_KEY else '❌ Não definida'}")
    print(f"  - GOOGLE_EMBEDDING_MODEL: {GOOGLE_EMBEDDING_MODEL}")
    print(f"  - DATABASE_URL: {DATABASE_URL}")
    print(f"  - PG_VECTOR_COLLECTION_NAME: {PG_VECTOR_COLLECTION_NAME}")
    print(f"  - CHUNK_SIZE: {CHUNK_SIZE}")
    print(f"  - CHUNK_OVERLAP: {CHUNK_OVERLAP}")
    print(f"  - K_RESULTS: {K_RESULTS}")
