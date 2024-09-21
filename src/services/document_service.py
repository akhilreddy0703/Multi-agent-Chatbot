# src/services/document_service.py

import os
from typing import List, Dict, Any
from fastapi import UploadFile
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.vector_store import get_vector_store
from src.config.settings import settings
from src.utils.error_handler import handle_errors
from motor.motor_asyncio import AsyncIOMotorClient
from src.services.embedding_service import embedding_service

class DocumentService:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database_url)
        self.db = self.client.get_database()
        self.docs_collection = self.db.get_collection("documents")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_store = get_vector_store()

    @handle_errors
    async def upload_document(self, file: UploadFile, user_id: str) -> Dict[str, Any]:
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            loader = UnstructuredFileLoader(temp_file_path)
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)
            
            # Get embeddings
            embeddings = await embedding_service.get_embeddings([text.page_content for text in texts])
            
            # Store in vector database
            ids = self.vector_store.add_embeddings(
                texts=[text.page_content for text in texts],
                embeddings=embeddings,
                metadatas=[text.metadata for text in texts]
            )
            
            # Store document metadata
            doc_metadata = {
                "filename": file.filename,
                "user_id": user_id,
                "vector_ids": ids
            }
            await self.docs_collection.insert_one(doc_metadata)
            
            return {"message": "Document uploaded and processed successfully", "filename": file.filename}
        finally:
            os.remove(temp_file_path)

    @handle_errors
    async def search_documents(self, query: str, user_id: str, k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = await embedding_service.get_query_embedding(query)
        docs = self.vector_store.similarity_search_by_vector(query_embedding, k=k)
        
        # Filter documents by user_id
        user_docs = await self.docs_collection.find({"user_id": user_id}).to_list(length=None)
        user_vector_ids = set([id for doc in user_docs for id in doc["vector_ids"]])
        
        filtered_docs = [doc for doc in docs if doc.metadata.get("id") in user_vector_ids]
        
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in filtered_docs]

    @handle_errors
    async def delete_document(self, doc_id: str, user_id: str) -> Dict[str, Any]:
        result = await self.docs_collection.find_one_and_delete({"_id": doc_id, "user_id": user_id})
        if result:
            # Remove from vector store
            self.vector_store.delete(result["vector_ids"])
            return {"message": "Document deleted successfully"}
        return {"message": "Document not found or you don't have permission to delete it"}

    @handle_errors
    async def list_documents(self, user_id: str) -> List[Dict[str, Any]]:
        docs = await self.docs_collection.find({"user_id": user_id}).to_list(length=None)
        return [{"id": str(doc["_id"]), "filename": doc["filename"]} for doc in docs]

document_service = DocumentService()