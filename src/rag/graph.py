from src.cache import get_cached_embedding, cache_embedding, get_cached_answer, cache_answer
from src.embeddings.jina_embeddings import JinaEmbeddings
from langchain.vectorstores import PGVector
from langchain.chat_models import ChatOpenAI
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

    llm = ChatOpenAI(model=Config.LLM_MODEL, api_key=Config.OPENAI_API_KEY)

    system_prompt = (
        "You are an HR assistant. Use the following context to answer the user's question. "
        "If you don't know, say that you don't know."
        "\n\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)

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