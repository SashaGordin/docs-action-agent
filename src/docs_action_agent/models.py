from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints

QuestionText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class QuestionRequest(BaseModel):
    question: QuestionText


class QuestionResponse(BaseModel):
    response: str
    status: Literal["answered", "abstained"]
