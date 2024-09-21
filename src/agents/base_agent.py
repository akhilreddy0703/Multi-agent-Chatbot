from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.abilities.base_ability import BaseAbility

class BaseAgent(ABC):
    def __init__(self, name: str, abilities: List[BaseAbility]):
        self.name = name
        self.abilities = abilities

    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass