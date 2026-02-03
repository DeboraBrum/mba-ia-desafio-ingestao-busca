from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import DATABASE_URL, PG_VECTOR_COLLECTION_NAME, GOOGLE_API_KEY, GOOGLE_EMBEDDING_MODEL

def get_embeddings():
    """Retorna o modelo de embeddings Google Generative AI."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY não está definida")
    
    return GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )

def get_vector_store(collection_name: str = PG_VECTOR_COLLECTION_NAME):
    """Cria e retorna a conexão com o banco de dados pgVector."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não está definida")
    
    collection = collection_name or "embeddings"
    embeddings = get_embeddings()

    vector_store = PGVector(
        connection=DATABASE_URL,
        embeddings=embeddings,
        collection_name=collection,
        use_jsonb=True,
    )

    return vector_store

if __name__ == "__main__": 
    print("🔌 Testando conexão com banco de dados...")
    try:
        vector_store = get_vector_store()
        print("✅ Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Certifique-se de que o PostgreSQL está rodando:")
        print("   docker-compose up -d")
