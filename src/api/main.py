from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from rag.graph import create_rag_graph
from evaluation.metrics import evaluate_response
from cache import load_chat_history, save_chat_history
from config import Config

app = FastAPI(title="HR FAQ Assistant", version="1.0")

graph = create_rag_graph()

class ChatRequest(BaseModel):
    user_id: str
    query: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_with_hr(request: ChatRequest):
    try:
        history = load_chat_history(request.user_id)
        messages = [HumanMessage(content=msg) for msg in history]
        messages.append(HumanMessage(content=request.query))

        state = {"messages": messages, "context": ""}
        result = graph.invoke(state)

        answer = result["messages"][-1].content
        context = result.get("context", [])

        # Save updated history
        history.append(request.query)
        history.append(answer)
        save_chat_history(request.user_id, history)

        # Evaluate response metrics
        metrics = evaluate_response(request.query, answer, context)

        return {
            "answer": answer,
            "metrics": metrics,
            "context": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))