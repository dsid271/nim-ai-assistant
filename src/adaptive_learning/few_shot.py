from src.model_serving.nim_server import NIMServer
from typing import List, Dict

class FewShotLearner:
    def __init__(self, nim_server: NIMServer):
        self.nim_server = nim_server

    async def generate_with_examples(self, prompt: str, examples: List[Dict[str, str]], max_length: int = 100) -> str:
        # Prepare the prompt with examples
        few_shot_prompt = self.prepare_few_shot_prompt(prompt, examples)

        # Generate the response
        response = await self.nim_server.generate(few_shot_prompt, max_length)

        return response

    def prepare_few_shot_prompt(self, prompt: str, examples: List[Dict[str, str]]) -> str:
        few_shot_prompt = ""
        for example in examples:
            few_shot_prompt += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
        few_shot_prompt += f"Input: {prompt}\nOutput:"
        return few_shot_prompt
