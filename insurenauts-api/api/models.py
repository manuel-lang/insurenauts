from pydantic import BaseModel


class UserAnswer(BaseModel):
    """Answer to a question"""

    question_id: str
    message: str


class GeneratedQuestion(BaseModel):
    """Question that is sent to a user"""

    id: str
    question: str
    options: list[str]


class RecommendationResult(BaseModel):
    """Product recommendations"""

    recommendations: list[str]


class EmailBody(BaseModel):
    """Email definition"""

    to: str
    subject: str
    message: str
