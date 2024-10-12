import pytest
from src.skill_modules import SkillRouter, QASkill, SummarizationSkill
from src.model_serving import NIMServer

@pytest.fixture
async def nim_server():
    return await NIMServer.initialize("config/nim_config.yaml")

@pytest.mark.asyncio
async def test_qa_skill(nim_server):
    qa_skill = QASkill(nim_server.model, nim_server.tokenizer)
    question = "What is the capital of France?"
    response = await qa_skill.execute(question)
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_summarization_skill(nim_server):
    summarization_skill = SummarizationSkill(nim_server.model, nim_server.tokenizer)
    text = "The quick brown fox jumps over the lazy dog. This sentence is often used as a pangram in typography."
    summary = await summarization_skill.execute(text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert len(summary) < len(text)

@pytest.mark.asyncio
async def test_skill_router(nim_server):
    skill_router = SkillRouter(nim_server.model, nim_server.tokenizer)
    
    # Test QA skill routing
    question = "What is the capital of France?"
    response = await skill_router.route_and_execute("qa", question)
    assert isinstance(response, str)
    assert len(response) > 0
    
    # Test Summarization skill routing
    text = "The quick brown fox jumps over the lazy dog. This sentence is often used as a pangram in typography."
    summary = await skill_router.route_and_execute("summarization", text)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert len(summary) < len(text)

    # Test invalid skill routing
    with pytest.raises(ValueError):
        await skill_router.route_and_execute("invalid_skill", "Some input")
