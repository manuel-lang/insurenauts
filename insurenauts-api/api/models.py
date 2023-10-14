from pydantic import BaseModel


class UserAnswer(BaseModel):
    """Answer to a question"""

    question_id: str
    message: str


class InsurancePackage(BaseModel):
    """Insure package definition"""

    name: str
    price: int
    description: str
    covered_items: list[str]


class Option(BaseModel):
    """Option to answer a question"""

    id: int
    description: str
    price: int


class GeneratedQuestion(BaseModel):
    """Question that is sent to a user"""

    id: str
    question: str
    options: list[Option]


class RecommendationResult(BaseModel):
    """Product recommendations"""

    recommendations: list[str]


class EmailBody(BaseModel):
    """Email definition"""

    to: str
    subject: str
    message: str


class CompletionResult(BaseModel):
    """Information provided for agent once user completes game."""

    name: str
    email: str
    suggested_insurance_packages: list[str]
    relevant_attributes: list[str]
