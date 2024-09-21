# src/agents/search_agent.py

import requests
from bs4 import BeautifulSoup
from src.agents.base_agent import BaseAgent
from src.services.llm_service import llm_service
from src.config.settings import settings

class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("Search Agent")

    async def process(self, task: dict) -> dict:
        query = task['query']

        # Perform web search
        search_results = self._web_search(query)

        # Prepare context from search results
        context = "\n".join([result['snippet'] for result in search_results])

        # Prepare prompt for LLM
        prompt = f"Based on the following search results, please answer the question: {query}\n\nSearch Results: {context}"

        # Get response from LLM
        response = await llm_service.process_query(prompt)

        return {"response": response, "search_results": search_results}

    def _web_search(self, query: str, num_results: int = 5):
        # This is a placeholder. In a real implementation, you would use a proper search API.
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for g in soup.find_all('div', class_='g')[:num_results]:
            anchor = g.find('a')
            if anchor:
                link = anchor['href']
                title = g.find('h3').text
                snippet = g.find('div', class_='s').text
                results.append({'title': title, 'link': link, 'snippet': snippet})
        
        return results

search_agent = SearchAgent()