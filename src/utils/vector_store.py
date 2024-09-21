# src/utils/vector_store.py

from langchain.vectorstores import Pinecone
import pinecone
from src.config.settings import settings
from src.services.embedding_service import embedding_service

class CustomPinecone(Pinecone):
    def add_embeddings(self, texts, embeddings, metadatas):
        vectors = [
            (f"vec{i}", embedding, metadata)
            for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))
        ]
        self.index.upsert(vectors=vectors)
        return [v[0] for v in vectors]

def get_vector_store():
    pinecone.init(api_key=settings.pinecone_api_key, environment=settings.pinecone_environment)
    return CustomPinecone.from_existing_index(
        index_name=settings.pinecone_index_name,
        embedding=embedding_service.model
    )

# You can easily add more vector store implementations here and choose based on configuration