import argparse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, PDF_PATH
from database import get_vector_store, get_embeddings

def load_pdf(pdf_path: str = PDF_PATH):
    """Carrega o PDF e retorna o loader."""
    try: 
        loader = PyPDFLoader(str(pdf_path))
        print(f"✅ PDF carregado: {len(loader.load())} páginas")
        return loader.load()
    except Exception as e:
        raise Exception(f"❌ Erro ao carregar PDF: {e}")

def split_pdf(documents, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    """Divide os documentos em chunks."""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap)
    
        chunks = splitter.split_documents(documents)

        enriched_documents = [
            Document(
                page_content=d.page_content,
                metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
            )
            for d in chunks
        ]

        print(f"✅ PDF dividido em {len(chunks)} chunks")
        return enriched_documents
    except Exception as e:
        raise Exception(f"❌ Erro ao dividir PDF: {e}")

def ingest_pdf(pdf_path: str):
    """
    Função principal para ingestão de PDF.
    1. Carrega o PDF
    2. Divide o PDF em chunks
    3. Insere os chunks no banco de dados
    """
    try:
        documents = load_pdf(pdf_path)
        enriched_documents = split_pdf(documents)
        if len(enriched_documents) == 0:
            raise Exception("❌ Nenhum documento processado")
        
        ids = [f"doc-{i}" for i in range(len(enriched_documents))]
        
        vector_store = get_vector_store()
        vector_store.add_documents(documents=enriched_documents, ids=ids)
        
        print(f"✅ {len(ids)} documentos ingeridos com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao ingerir PDF: {e}")

def main():
    """
    Função principal para ingestão de PDF.
    Permite executar: python src/ingest.py document.pdf
    """
    parser = argparse.ArgumentParser(
        description="Ingestão de PDF para o banco de dados"
    )
    parser.add_argument("pdf_path", type=str, help="Caminho para o arquivo PDF")
    args = parser.parse_args()

    ingest_pdf(args.pdf_path)

if __name__ == "__main__":
    main()