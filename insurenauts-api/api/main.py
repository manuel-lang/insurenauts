import uvicorn
from fastapi import FastAPI
from api.models import GeneratedQuestion, UserAnswer, RecommendationResult, EmailBody
from api.utils import send_email


app = FastAPI()


@app.get("/healthcheck")
async def get_health():
    return {"status": "ok"}


@app.get("/init", description="Load initial data.")
async def load_initial_app_data_handler() -> None:
    return {"message": "Hello World"}


@app.post("/answer", description="Process a user answer and generate next question.")
async def process_answer_handler(user_answer: UserAnswer) -> GeneratedQuestion:
    pass


@app.get("/recommendations", description="Generate recommendations based on user id")
async def generate_recommendations_handler(user_id: int) -> RecommendationResult:
    pass


@app.post("/email")
async def send_email_handler(body: EmailBody):
    return send_email(body)


def run_app():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
