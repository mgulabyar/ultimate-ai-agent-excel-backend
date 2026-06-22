from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any, Optional
from services.agent_brain import AgentBrain
from services.db_service import DBService

router = APIRouter(prefix="/api/agent", tags=["AI Agent"])


class AgentRequest(BaseModel):
    prompt: str
    snapshot: Optional[List[List[Any]]] = []


@router.post("/chat")
async def agent_chat(req: AgentRequest):
    try:
        # 1. Fetch memory standard format me
        history = await DBService.get_recent_history(limit=5)

        # 2. Process query
        agent_data = await AgentBrain.process_user_request(
            req.prompt, req.snapshot, history
        )

        # 3. Log interaction properly
        await DBService.log_interaction(req.prompt, agent_data.get("message", ""))

        return {"status": "success", "agent_data": agent_data}
    except Exception as e:
        print(f"Server Error Detail: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
