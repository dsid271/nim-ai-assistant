import pytest
from src.model_serving.nim_server import NIMServer

@pytest.mark.asyncio
async def test_nim_server_initialization():
    nim_server = await NIMServer.initialize("config/nim_config.yaml")
    assert nim_server.model is not None
    assert nim_server.tokenizer is not None

@pytest.mark.asyncio
async def test_nim_server_generate():
    nim_server = await NIMServer.initialize("config/nim_config.yaml")
    prompt = "Hello, how are you?"
    response = await nim_server.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0
