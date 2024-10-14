from abc import ABC, abstractmethod

class SkillBase(ABC):
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    @abstractmethod
    async def execute(self, input: str) -> str:
        pass
