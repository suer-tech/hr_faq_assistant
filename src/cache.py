import json
import redis
from config import Config

r = redis.from_url(Config.REDIS_URL)

def get_cached_embedding(query: str):
    key = f"emb:{query}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None

def cache_embedding(query: str, embedding: list):
    key = f"emb:{query}"
    r.setex(key, 3600, json.dumps(embedding))  # 1 hour TTL

def get_cached_answer(query: str):
    key = f"ans:{query}"
    cached = r.get(key)
    if cached:
        return cached.decode("utf-8")
    return None

def cache_answer(query: str, answer: str):
    key = f"ans:{query}"
    r.setex(key, 3600, answer)  # 1 hour TTL

def save_chat_history(user_id: str, history: list):
    key = f"chat:{user_id}"
    r.setex(key, 3600, json.dumps(history))

def load_chat_history(user_id: str):
    key = f"chat:{user_id}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return []