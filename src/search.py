from database import get_vector_store
from config import K_RESULTS

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def semantic_search(query: str, k: int = None):
  k = k or K_RESULTS
  try:
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results
  except Exception as e:
    raise Exception(f" Erro ao realizar busca semântica: {e}")

def format_docs(results):
  """
  Formata documentos para contexto textual.
  """
  if not results:
    return "Não tenho informações necessárias para responder sua pergunta."
  context_parts = []
  for i, (doc, score) in enumerate(results, start=1):
    context_parts.append(
      f"Documento {i} (Relevância: {score:.3f})\n{doc.page_content}\n"
    )
  context = "\n".join(context_parts)
  return context
  
def print_results(results):
  try:
    print(f"\n{'='*60}")
    print(f"Encontrados {len(results)} documento(s)")
    print(f"{'='*60}\n")
    for i, (doc, score) in enumerate(results, 1):
      print(f"📄 Documento {i}")
      print(f"   Score: {score:.4f} (menor = mais relevante)")
      print(f"   Fonte: {doc.metadata.get('source', 'N/A')}")
      print(f"   Conteúdo: {doc.page_content[:150]}...")
      print("-" * 60)
  except Exception as e:
    raise Exception(f" Erro ao exibir resultados: {e}")
