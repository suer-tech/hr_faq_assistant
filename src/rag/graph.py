from cache import get_cached_embedding, cache_embedding, get_cached_answer, cache_answer
from embeddings.jina_embeddings import JinaEmbeddings
from langchain.vectorstores import PGVector
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from config import Config

def create_rag_graph():
    embeddings = JinaEmbeddings(model_name=Config.EMBEDDING_MODEL)

    vectorstore = PGVector(
        collection_name=Config.COLLECTION_NAME,
        connection_string=Config.DATABASE_URL,
        embedding_function=embeddings,
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 3
        }
    )

    llm = ChatOpenAI(
        model=Config.LLM_MODEL,
        api_key=Config.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"  # <-- Указываем OpenRouter
    )

    system_prompt = (
        "Ты — HR-ассистент компании. Твоя задача — отвечать на вопросы сотрудников, "
        "используя только информацию, содержащуюся в предоставленном контексте. "
        "Не придумывай ничего самостоятельно, не используй знания, полученные до обучения. "
        "Если в контексте нет информации — честно скажи, что не можешь ответить, и предложи "
        "обратиться в HR-отдел.\n\n"
        "Формат ответа:\n"
        "- Краткий заголовок.\n"
        "- Подробное объяснение.\n"
        "- При необходимости — ссылка на конкретный документ или раздел.\n\n"
        "Стиль:\n"
        "- Вежливый, профессиональный.\n"
        "- Ясный, структурированный.\n"
        "- На русском языке.\n\n"
        "Контекст:\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    def rag_node(state: dict):
        query = state["messages"][-1].content

        # Check cache
        cached_answer = get_cached_answer(query)
        if cached_answer:
            return {"messages": [cached_answer]}

        # Retrieve context
        response = rag_chain.invoke({"input": query})
        answer = response["answer"]
        context = response["context"]

        # Cache answer
        cache_answer(query, answer)

        return {
            "messages": [answer],
            "context": context
        }

    workflow = StateGraph(dict)
    workflow.add_node("rag", rag_node)
    workflow.set_entry_point("rag")
    workflow.add_edge("rag", "__end__")

    return workflow.compile()