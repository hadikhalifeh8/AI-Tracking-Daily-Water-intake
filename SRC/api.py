from fastapi import FastAPI
from pydantic import BaseModel
from SRC.agent import WaterIntakeAgent
from SRC.database import log_water_intake, get_intake_history
from SRC.logger import log_messages

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.post("/log_intake")
async def create_water_intake(request: WaterIntakeRequest):
    log_water_intake(request.user_id, request.intake_ml)

    analysis = agent.analyze_intake(request.intake_ml)

    log_messages(
        f"User {request.user_id} logged {request.intake_ml} ml of water intake."
    )

    return {
        "message": "Water intake logged successfully.",
        "analysis": analysis
    }




@app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)

    log_messages(
        f"User {user_id} requested intake history."
    )

    return {
        "user_id": user_id,
        "intake_history": history
    }




