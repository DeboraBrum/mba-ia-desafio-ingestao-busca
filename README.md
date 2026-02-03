# Sistema de Busca Semântica em PDFs

Sistema completo de ingestão e busca semântica em documentos PDF utilizando **LangChain**, **PostgreSQL com pgVector**, e **Google Gemini** para embeddings e geração de respostas. O sistema permite fazer perguntas sobre o conteúdo de PDFs através de uma interface CLI interativa.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos de Uso](#exemplos-de-uso)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) que:

1. **Ingere PDFs** - Carrega documentos PDF, divide em chunks e gera embeddings
2. **Armazena vetores** - Salva embeddings no PostgreSQL usando pgVector
3. **Busca semântica** - Encontra documentos relevantes baseado em similaridade vetorial
4. **Gera respostas** - Usa Google Gemini para responder perguntas baseadas no contexto encontrado

## 🛠 Tecnologias

### Principais Bibliotecas
- **LangChain** (0.3.27) - Framework para aplicações LLM
- **LangChain Google GenAI** (2.1.9) - Integração com Google Gemini
- **LangChain Postgres** (0.0.15) - Integração com PostgreSQL + pgVector
- **LangChain Community** (0.3.27) - Loaders de documentos (PyPDFLoader)
- **LangChain Text Splitters** (0.3.9) - Divisão de texto em chunks

### Infraestrutura
- **PostgreSQL** com extensão **pgVector** - Banco de dados vetorial
- **Docker & Docker Compose** - Orquestração de containers
- **Python 3+** - Linguagem de programação

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3+** ([Download](https://www.python.org/downloads/))
- **Docker** e **Docker Compose** ([Download](https://www.docker.com/get-started))
- **Google API Key** 

## 🚀 Instalação

### 1. Clone o repositório (ou navegue até a pasta do projeto)

```bash
cd /Users/debora.brum/Study/mba-ia-desafio-ingestao-busca
```

### 2. Crie um ambiente virtual Python

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**No macOS/Linux:**
```bash
source venv/bin/activate
```

**No Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

### 2. Edite o arquivo `.env`

Abra o arquivo `.env` e preencha as seguintes variáveis:

```bash
# Google API Configuration
GOOGLE_API_KEY=sua_chave_api_google_aqui
GOOGLE_EMBEDDING_MODEL='models/embedding-001'
GOOGLE_MODEL='gemini-2.0-flash-exp'

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=rag

# PDF Path (opcional)
PDF_PATH='./document.pdf'
```

**Importante:**
- Substitua `sua_chave_api_google_aqui` pela sua chave real da Google API
- O `DATABASE_URL` já está configurado para o Docker Compose padrão
- O `PG_VECTOR_COLLECTION_NAME` é o nome da coleção/tabela no banco

### 3. Inicie o banco de dados PostgreSQL

```bash
docker-compose up -d
```

Este comando irá:
- Iniciar o container PostgreSQL com pgVector
- Criar o banco de dados `rag`
- Habilitar a extensão `vector` automaticamente

**Verifique se o container está rodando:**
```bash
docker ps
```

Você deve ver um container chamado `postgres_rag` em execução.

### 4. (Opcional) Teste a conexão com o banco

```bash
python src/database.py
```

Se tudo estiver correto, você verá:
```
✅ Conexão estabelecida com sucesso!
```

## 🎮 Como Executar

### Passo 1: Ingerir um PDF

Para processar um PDF e armazená-lo no banco de dados:

```bash
python src/ingest.py document.pdf
```

**Ou com caminho completo:**
```bash
python src/ingest.py /caminho/para/seu/arquivo.pdf
```

**O que acontece:**
1. O PDF é carregado e dividido em chunks (tamanho: 1000 caracteres, overlap: 150)
2. Cada chunk recebe um embedding usando Google Gemini
3. Os embeddings são armazenados no PostgreSQL

**Saída esperada:**
```
✅ PDF carregado: X páginas
✅ PDF dividido em Y chunks
✅ Y documentos ingeridos com sucesso!
```

### Passo 2: Iniciar o Chat Interativo

Após ingerir pelo menos um PDF, inicie o chat:

```bash
python src/chat.py
```

**O que acontece:**
1. A chain RAG é inicializada usando LCEL (LangChain Expression Language)
2. Um loop interativo é iniciado
3. Você pode fazer perguntas sobre o conteúdo dos PDFs ingeridos

**Exemplo de uso:**
```
Inicializando chain
Chain inicializada com sucesso
Iniciando o chat! Digite 'sair' para encerrar.

Digite sua pergunta: Qual é o faturamento da empresa?

🔍 Buscando informações

🤖 Resposta: [Resposta baseada no conteúdo do PDF]
```

**Para sair do chat:**
Digite `sair` e pressione Enter.

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── docker-compose.yml          # Configuração do PostgreSQL + pgVector
├── requirements.txt             # Dependências Python
├── .env.example                 # Template de variáveis de ambiente
├── .env                         # Variáveis de ambiente (não commitado)
├── .gitignore                   # Arquivos ignorados pelo Git
├── document.pdf                 # PDF de exemplo para ingestão
├── README.md                    # Este arquivo
├── plan_to_desafio.md           # Plano de desenvolvimento
└── src/
    ├── config.py               # Configurações e variáveis de ambiente
    ├── database.py              # Conexão com PostgreSQL e pgVector
    ├── ingest.py                # Script de ingestão de PDFs
    ├── search.py                # Busca semântica e formatação
    └── chat.py                   # Interface CLI interativa com chain RAG
```

### Descrição dos Módulos

- **`config.py`**: Centraliza todas as configurações do projeto (API keys, modelos, parâmetros)
- **`database.py`**: Gerencia conexão com PostgreSQL e criação do vector store
- **`ingest.py`**: Processa PDFs, divide em chunks e armazena no banco
- **`search.py`**: Implementa busca semântica e formatação de documentos
- **`chat.py`**: Interface CLI que usa chains LCEL para RAG

## 💡 Exemplos de Uso

### Exemplo 1: Ingestão de PDF

```bash
# Ingerir o PDF de exemplo
python src/ingest.py document.pdf

# Ingerir outro PDF
python src/ingest.py outro_documento.pdf
```

### Exemplo 2: Chat Interativo

```bash
python src/chat.py
```

**Perguntas de exemplo:**
```
Digite sua pergunta: Qual é o faturamento da empresa?
Digite sua pergunta: Quais são os principais produtos?
Digite sua pergunta: Quantos funcionários a empresa tem?
Digite sua pergunta: sair
```

### Exemplo 3: Verificar Configurações

```bash
python src/config.py
```

Mostra todas as configurações carregadas do ambiente.

### Exemplo 4: Testar Conexão com Banco

```bash
python src/database.py
```

Verifica se a conexão com PostgreSQL está funcionando.

## 🔧 Troubleshooting

### Erro: "GOOGLE_API_KEY não está definida"

**Solução:**
1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Confirme que a variável `GOOGLE_API_KEY` está preenchida
3. Certifique-se de que não há espaços extras ou aspas desnecessárias

### Erro: "DATABASE_URL não está definida"

**Solução:**
1. Verifique se o arquivo `.env` contém a variável `DATABASE_URL`
2. Confirme que o formato está correto: `postgresql://usuario:senha@host:porta/banco`

### Erro: "Connection refused" ou "Could not connect to database"

**Solução:**
1. Verifique se o Docker está rodando:
   ```bash
   docker ps
   ```
2. Inicie o PostgreSQL:
   ```bash
   docker-compose up -d
   ```
3. Aguarde alguns segundos para o banco inicializar completamente
4. Teste a conexão:
   ```bash
   python src/database.py
   ```

### Erro: "No module named 'langchain'"

**Solução:**
1. Certifique-se de que o ambiente virtual está ativado
2. Reinstale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Erro: "Nenhum documento encontrado" durante a busca

**Solução:**
1. Certifique-se de que você ingeriu pelo menos um PDF:
   ```bash
   python src/ingest.py document.pdf
   ```
2. Verifique se o `PG_VECTOR_COLLECTION_NAME` no `.env` corresponde ao usado na ingestão

### Erro: "Extension 'vector' does not exist"

**Solução:**
1. Pare o Docker Compose:
   ```bash
   docker-compose down
   ```
2. Remova o volume (cuidado: apaga os dados):
   ```bash
   docker-compose down -v
   ```
3. Inicie novamente:
   ```bash
   docker-compose up -d
   ```

### O chat não encontra informações relevantes

**Possíveis causas:**
1. O PDF não foi ingerido corretamente
2. A pergunta está muito diferente do conteúdo do PDF
3. Tente reformular a pergunta de forma mais específica

### Erro ao executar `python src/chat.py`

**Verifique:**
1. Se todas as dependências estão instaladas
2. Se o ambiente virtual está ativado
3. Se o banco de dados está rodando
4. Se pelo menos um PDF foi ingerido