from langchain.memory import ConversationBufferWindowMemory

# Stores one memory object per WhatsApp number
_store: dict[str, ConversationBufferWindowMemory] = {}

def get_memory(user_id: str) -> ConversationBufferWindowMemory:
    """Return existing memory for a user, or create a fresh one."""
    if user_id not in _store:
        _store[user_id] = ConversationBufferWindowMemory(
            k=6,                        # remember last 6 exchanges
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    return _store[user_id]

def clear_memory(user_id: str):
    """Reset conversation for a user (e.g. after human handoff)."""
    _store.pop(user_id, None)

def active_users() -> list[str]:
    return list(_store.keys())
