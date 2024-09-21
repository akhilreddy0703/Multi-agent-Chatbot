# src/agents/rag_agent.py

from src.agents.base_agent import BaseAgent
from src.services.document_service import document_service
from src.services.llm_service import llm_service

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__("RAG Agent")

    async def process(self, task: dict) -> dict:
        query = task['query']
        user_id = task['user_id']

        # Retrieve relevant documents
        docs = await document_service.search_documents(query, user_id)

        # Prepare context from retrieved documents
        context = "\n".join([doc["content"] for doc in docs])

        # Prepare prompt for LLM
        prompt = f"Based on the following context, please answer the question: {query}\n\nContext: {context}"

        # Get response from LLM
        response = await llm_service.process_query(prompt)

        return {"response": response, "source_documents": docs}

rag_agent = RAGAgent()