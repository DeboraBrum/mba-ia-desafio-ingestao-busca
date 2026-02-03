from search import semantic_search, PROMPT_TEMPLATE, format_docs
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from config import GOOGLE_API_KEY, GOOGLE_MODEL, K_RESULTS
from langchain.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

def get_model_llm():
    model_llm = GoogleGenerativeAI(
        model=GOOGLE_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,
    )
    return model_llm

def rag_chain():
    """Executa o fluxo busca -> contexto -> llm -> resposta."""
    llm = get_model_llm()
    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )
    chain = (
        {
            "contexto": RunnableLambda(semantic_search) | format_docs, 
            "pergunta": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def main():
    print("Inicializando chain")
    chain = rag_chain()
    print("Chain inicializada com sucesso")
    print("Iniciando o chat! Digite 'sair' para encerrar.\n")
    while True:
        try:
            question = input("Digite sua pergunta: ").strip()
            if not question:
                continue
            if question.lower() == "sair":
                break
            print("\n🔍 Buscando informações")
            response = chain.invoke(question)
            print(f"\n🤖 Resposta: {response}")
        except Exception as e:
            print(f" Erro ao processar a pergunta: {e}")
            continue
        except KeyboardInterrupt:
            print("\n👋 Chat encerrado pelo usuário")
            break

if __name__ == "__main__":
    main()