import pytest
from src.adaptive_learning.fine_tuning import FineTuner
from src.adaptive_learning.few_shot import FewShotLearner
from src.model_serving.nim_server import NIMServer

@pytest.mark.asyncio
async def test_fine_tuning():
    nim_server = await NIMServer.initialize("config/nim_config.yaml")
    fine_tuner = FineTuner(nim_server.model, nim_server.tokenizer)
    dataset = [{"input": "Hello", "output": "Hi there!"}]
    await fine_tuner.fine_tune(dataset)
    assert fine_tuner.model is not None

@pytest.mark.asyncio
async def test_few_shot_learning():
    nim_server = await NIMServer.initialize("config/nim_config.yaml")
    few_shot_learner = FewShotLearner(nim_server.model, nim_server.tokenizer)
    prompt = "Translate 'hello' to French"
    examples = [{"input": "Translate 'goodbye' to French", "output": "Au revoir"}]
    response = await few_shot_learner.generate_with_examples(prompt, examples)
    assert isinstance(response, str)
    assert len(response) > 0
