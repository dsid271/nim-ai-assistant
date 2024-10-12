from .skill_base import SkillBase

class SummarizationSkill(SkillBase):
    async def execute(self, input: str) -> str:
        prompt = f"Summarize the following text: {input}"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=100)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
