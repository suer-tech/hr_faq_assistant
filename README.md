# HR FAQ Assistant
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   HR Documents  │───▶│   Ingestion      │───▶│   Vector Store   │
│   (PDF/MD)      │    │   (chunking +    │    │   (pgvector)     │
│                 │    │   embedding)     │    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                       │
┌─────────────────┐    ┌──────────────────┐    ┌───────▼──────────┐
│   FastAPI API   │◀───│   LangGraph RAG  │◀───│   Retrieval      │
│   (chat + eval) │    │   (with history) │    │   (similarity)   │
│                 │    │   + metrics      │    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                       │
┌─────────────────┐    ┌──────────────────┐    ┌───────▼──────────┐
│   MLflow UI     │◀───│   Eval Metrics   │    │   OpenAI API     │
│   (experiments) │    │   (faithfulness, │    │                  │
│                 │    │   recall, etc.)  │    └──────────────────┘
└─────────────────┘    └──────────────────┘

## 🧠 Описание

**HR FAQ Assistant** — это RAG-приложение, которое отвечает на вопросы сотрудников по внутренним HR-политикам компании.  
Система использует **векторный поиск**, **OpenAI**, **Jina embeddings**, **pgvector**, **Redis**, **LangGraph**, **FastAPI**, **MLflow**, **Docker** и **CI/CD**.

## 🚀 Функционал

- **Поиск по документам** с помощью RAG.
- **Чат с историей** (multi-turn).
- **Кэширование** через Redis.
- **Метрики качества**: faithfulness, recall, precision, F1-score, p95/p99.
- **MLflow** для отслеживания экспериментов.
- **Docker** и **docker-compose** для контейнеризации.
- **CI/CD** через GitHub Actions.

## 🛠️ Технологии

- **FastAPI** — API
- **OpenAI** — LLM
- **Jina embeddings** — векторизация
- **pgvector** — векторная БД
- **LangGraph** — RAG-цепочка
- **Redis** — кэширование
- **MLflow** — отслеживание метрик
- **Docker** — контейнеризация
- **ragas** — метрики RAG
- **GitHub Actions** — CI/CD


