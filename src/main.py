import asyncio
import uvicorn
from fastapi import FastAPI
from src.api.endpoints import router as api_router
from src.model_serving.nim_server import NIMServer
from src.context_management.context_tracker import ContextTracker
from src.skill_modules.skill_router import SkillRouter
from src.adaptive_learning.fine_tuning import FineTuner
from src.adaptive_learning.few_shot import FewShotLearner
from src.monitoring.metrics import MonitoringSystem

app = FastAPI(title="NIM-powered Adaptive AI Assistant")

@app.on_event("startup")
async def startup_event():
    # Initialize NIM server
    app.state.nim_server = await NIMServer.create("config/model_config.yaml")
    
    # Initialize context tracker
    app.state.context_tracker = ContextTracker()

    # Initialize skill router
    app.state.skill_router = SkillRouter(app.state.nim_server.model, app.state.nim_server.tokenizer)

    # Initialize adaptive learning components
    app.state.fine_tuner = FineTuner(app.state.nim_server.model, app.state.nim_server.tokenizer)
    app.state.few_shot_learner = FewShotLearner(app.state.nim_server.model, app.state.nim_server.tokenizer)

    # Initialize monitoring system
    app.state.monitoring = MonitoringSystem()
    app.state.monitoring.start()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
