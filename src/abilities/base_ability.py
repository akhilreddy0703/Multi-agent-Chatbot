from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAbility(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pass