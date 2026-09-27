from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleVectorStore:
    """
    Lightweight RAG retrieval for Streamlit Cloud.
    Uses TF-IDF + cosine similarity instead of a hosted vector database.
    """

    def __init__(self):
        self.chunks = []
        self.sources = []
        self.vectorizer = None
        self.matrix = None

    def _chunk_text(self, text, chunk_size=900, overlap=150):
        text = " ".join(text.split())

        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start = max(end - overlap, start + 1)

        return chunks

    def add_document(self, source_name, text):
        chunks = self._chunk_text(text)

        for chunk in chunks:
            self.chunks.append(chunk)
            self.sources.append(source_name)

        if self.chunks:
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2)
            )
            self.matrix = self.vectorizer.fit_transform(self.chunks)

    def search(self, query, top_k=4):
        if not self.chunks or self.vectorizer is None or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()

        indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in indices:
            if scores[idx] <= 0:
                continue

            results.append({
                "text": self.chunks[idx],
                "source": self.sources[idx],
                "score": float(scores[idx])
            })

        return results
