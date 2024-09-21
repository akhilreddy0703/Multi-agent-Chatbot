# src/services/llm_service.py

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from src.config.settings import settings

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(model_name=settings.llm_model, openai_api_key=settings.openai_api_key)

    async def process_query(self, query: str) -> str:
        messages = [HumanMessage(content=query)]
        response = self.llm(messages)
        return response.content

llm_service = LLMService()