def search_knowledge(vector_store, query: str, top_k: int = 4):
    if vector_store is None:
        return []
    return vector_store.search(query, top_k=top_k)
