import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class UserAnswer(BaseModel):
    message: str


class GeneratedQuestion(BaseModel):
    question: str


class RecommendationResult(BaseModel):
    recommendations: list[str]


app = FastAPI()


@app.get("/init", description="Load initial data.")
async def load_initial_app_data() -> None:
    return {"message": "Hello World"}


@app.post("/answer", description="Process a user answer and generate next question.")
async def process_answer(user_answer: UserAnswer) -> GeneratedQuestion:
    pass


@app.get("/recommendations", description="Generate recommendations based on user id")
async def generate_recommendations(user_id: int) -> RecommendationResult:
    pass


def run_app():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
