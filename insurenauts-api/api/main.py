import uvicorn
from fastapi import FastAPI
from api.models import (
    GeneratedQuestion,
    UserAnswer,
    RecommendationResult,
    EmailBody,
    InsurancePackage,
    CompletionResult,
    Story,
)
from api.utils import (
    get_all_insurance_packages,
    send_email,
    generate_email_content,
    start_story,
)


app = FastAPI()


@app.get("/healthcheck")
async def get_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/init", description="Load initial data.")
async def load_initial_app_data_handler() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/insurances", description="List all insurance packages.")
async def list_all_insurance_packages() -> list[InsurancePackage]:
    return get_all_insurance_packages()


@app.post("/answer", description="Process a user answer and generate next question.")
async def process_answer_handler(user_answer: UserAnswer) -> GeneratedQuestion:
    pass


@app.get("/recommendations", description="Generate recommendations based on user id")
async def generate_recommendations_handler(user_id: int) -> RecommendationResult:
    pass


@app.post("/email")
async def send_email_handler(body: EmailBody) -> dict[str, str]:
    return send_email(body)


@app.post("/submit", description="User completes game and result gets mailed to agent.")
async def complete_game(completion_result: CompletionResult) -> dict[str, str]:
    email_content = generate_email_content(completion_result)
    email_body = EmailBody(
        to="manuellang183@gmail.com",
        subject="Auswertung von InsureNauts verfügbar",
        message=email_content,
    )
    return send_email(email_body)


@app.get("/story", description="Get the first Story Tree.")
async def get_story_tree() -> Story:
    return start_story()


def run_app():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
