from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.context_management.context_tracker import ContextTracker
from src.skill_modules.skill_router import SkillRouter
from src.adaptive_learning.fine_tuning import FineTuner
from src.adaptive_learning.few_shot import FewShotLearner
from src.monitoring.metrics import MonitoringSystem

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, 
                context_tracker: ContextTracker = Depends(lambda: router.app.state.context_tracker),
                skill_router: SkillRouter = Depends(lambda: router.app.state.skill_router),
                monitoring: MonitoringSystem = Depends(lambda: router.app.state.monitoring)):
    try:
        monitoring.process_request(request.message)
        
        # Determine the appropriate skill (for simplicity, always use 'qa' skill here)
        skill_name = "qa"
        
        response = await skill_router.route_and_execute(skill_name, request.message)
        
        context_tracker.add_interaction(request.message, response)
        
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FinetuneRequest(BaseModel):
    dataset: list

@router.post("/finetune")
async def finetune(request: FinetuneRequest,
                   fine_tuner: FineTuner = Depends(lambda: router.app.state.fine_tuner)):
    try:
        await fine_tuner.fine_tune(request.dataset)
        return {"message": "Fine-tuning completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FewShotRequest(BaseModel):
    prompt: str
    examples: list

@router.post("/few-shot", response_model=ChatResponse)
async def few_shot(request: FewShotRequest,
                   few_shot_learner: FewShotLearner = Depends(lambda: router.app.state.few_shot_learner)):
    try:
        response = await few_shot_learner.generate_with_examples(request.prompt, request.examples)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
