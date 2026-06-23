import json
from redis import Redis


redis_client = Redis.from_url(
    url="rediss://evident-thrush-148926.upstash.io:6379",
    password="gQAAAAAAAkW-AAIgcDE1Y2M5ZGIxZjIzZTY0Mjc2ODA0MDgxY2YyYzYwYWJjOA",
    decode_responses=True # Important for getting strings back
)


# -----------------------------
# Chat Memory
# -----------------------------
def append_chat(session_id: str, role: str, message: str):
    key = f"{session_id}:chat_history"
    print("✅ Saving to Redis:", session_id, role, message)
    
    history = redis_client.get(key)
    history = json.loads(history) if history else []

    history.append({
        "role": role,
        "content": message
    })

    # keep last 10 messages
    history = history[-10:]

    redis_client.set(key, json.dumps(history), ex=3600)


def get_chat_history(session_id: str):
    val = redis_client.get(f"{session_id}:chat_history")
    return json.loads(val) if val else []


# -----------------------------
# Optional: Structured memory (intent etc.)
# -----------------------------
def save_context(session_id: str, key: str, value: dict):
    redis_client.set(
        f"{session_id}:{key}",
        json.dumps(value),
        ex=3600
    )


def get_context(session_id: str, key: str):
    val = redis_client.get(f"{session_id}:{key}")
    return json.loads(val) if val else None
