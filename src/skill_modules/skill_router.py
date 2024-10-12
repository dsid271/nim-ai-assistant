from typing import Dict
from .qa_skill import QASkill
from .summarization_skill import SummarizationSkill

class SkillRouter:
    def __init__(self, model, tokenizer):
        self.skills: Dict[str, SkillBase] = {
            "qa": QASkill(model, tokenizer),
            "summarization": SummarizationSkill(model, tokenizer),
        }

    async def route_and_execute(self, skill_name: str, input: str) -> str:
        if skill_name not in self.skills:
            raise ValueError(f"Skill '{skill_name}' not found")
        return await self.skills[skill_name].execute(input)
