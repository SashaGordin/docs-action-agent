import asyncio
import re
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    StringConstraints,
    ValidationError,
)

_EVIDENCE_FIXTURES = [
    {
        "chunk_id": "request-body-001",
        "source_title": "Request Body",
        "source_url": "https://fastapi.tiangolo.com/tutorial/body/",
        "excerpt": "FastAPI uses Pydantic models to declare and validate request bodies.",
        "content": (
            "A request body contains data sent by a client to an API. FastAPI uses "
            "Pydantic models to declare the expected fields, validate incoming data, "
            "and include the resulting schema in the generated API documentation. "
            "A path operation can receive a model instance after validation succeeds."
        ),
    },
    {
        "chunk_id": "dependencies-001",
        "source_title": "Dependencies",
        "source_url": "https://fastapi.tiangolo.com/tutorial/dependencies/",
        "excerpt": "FastAPI provides a dependency injection system using Depends.",
        "content": (
            "FastAPI provides a dependency injection system through Depends. A path "
            "operation declares what it needs, and FastAPI calls the dependency and "
            "supplies its result. Dependencies can share validation, authentication, "
            "database access, and other reusable request-processing behavior."
        ),
    },
    {
        "chunk_id": "errors-001",
        "source_title": "Handling Errors",
        "source_url": "https://fastapi.tiangolo.com/tutorial/handling-errors/",
        "excerpt": "HTTPException can be used to return HTTP error responses to clients.",
        "content": (
            "A FastAPI path operation can raise HTTPException to stop normal request "
            "processing and return a controlled HTTP error response. The exception "
            "includes a status code and a bounded detail value for the client. Custom "
            "exception handlers can provide consistent application error responses."
        ),
    },
]

QueryString = Annotated[
    str, StringConstraints(min_length=1, max_length=500, strip_whitespace=True)
]

ResultLimit = Field(default=3, ge=1, le=3, strict=True)


class SourceLookupArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)
    ]


class EvidenceSearchArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: QueryString
    result_limit: int = ResultLimit


class EvidenceSearchHit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)
    ]
    source_title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    source_url: HttpUrl
    excerpt: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)
    ]
    relevance_score: float = Field(strict=True, ge=0, allow_inf_nan=False)


SearchHits = Annotated[list[EvidenceSearchHit], Field(min_length=0, max_length=3)]


class SourceLookupResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)
    ]
    source_title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    source_url: HttpUrl
    content: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)
    ]


class EvidenceSearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: QueryString
    hits: SearchHits


class ToolError(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
    ]
    code: Literal[
        "invalid_arguments",
        "execution_failed",
        "invalid_result",
        "not_found",
        "tool_not_allowed",
    ]
    retryable: bool


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def source_lookup(arguments: SourceLookupArguments) -> SourceLookupResult | ToolError:
    chunk_id = arguments.chunk_id
    for fixture in _EVIDENCE_FIXTURES:
        if fixture["chunk_id"] == chunk_id:
            return SourceLookupResult(
                chunk_id=fixture["chunk_id"],
                source_title=fixture["source_title"],
                source_url=fixture["source_url"],
                content=fixture["content"],
            )

    return ToolError(message="No results found", code="not_found", retryable=False)


def evidence_search(arguments: EvidenceSearchArguments) -> EvidenceSearchResult:
    query = arguments.query
    tokenized_query = _tokenize(query)
    hits: list[EvidenceSearchHit] = []
    for fixture in _EVIDENCE_FIXTURES:
        tokenized_fixture = _tokenize(f'{fixture["source_title"]} {fixture["excerpt"]}')
        relevance_score = float(len(tokenized_query & tokenized_fixture))
        if relevance_score > 0:
            hit = EvidenceSearchHit(
                chunk_id=fixture["chunk_id"],
                source_title=fixture["source_title"],
                source_url=fixture["source_url"],
                excerpt=fixture["excerpt"],
                relevance_score=relevance_score,
            )
            hits.append(hit)

    hits.sort(key=lambda hit: (-hit.relevance_score, hit.chunk_id))
    return EvidenceSearchResult(hits=hits[: arguments.result_limit], query=query)


def execute_evidence_search(
    raw_arguments: object,
) -> EvidenceSearchResult | ToolError:
    try:
        arguments = EvidenceSearchArguments.model_validate(raw_arguments)
    except ValidationError:
        return ToolError(
            message="Tool arguments failed validation.",
            code="invalid_arguments",
            retryable=False,
        )
    return evidence_search(arguments)


def execute_source_lookup(
    raw_arguments: object,
) -> SourceLookupResult | ToolError:
    try:
        arguments = SourceLookupArguments.model_validate(raw_arguments)
    except ValidationError:
        return ToolError(
            message="Tool arguments failed validation.",
            code="invalid_arguments",
            retryable=False,
        )
    return source_lookup(arguments)


_TOOL_REGISTRY = [
    {"tool_name": "evidence_search", "tool_function": execute_evidence_search},
    {"tool_name": "source_lookup", "tool_function": execute_source_lookup},
]


def execute_tool(
    tool_name: str, raw_arguments: object
) -> EvidenceSearchResult | SourceLookupResult | ToolError:
    for tool in _TOOL_REGISTRY:
        if tool["tool_name"] == tool_name:
            return tool["tool_function"](raw_arguments)
    return ToolError(
        message="Tool not allowed",
        code="tool_not_allowed",
        retryable=False,
    )


async def execute_tool_async(
    tool_name: str, raw_arguments: object
) -> EvidenceSearchResult | SourceLookupResult | ToolError:
    return await asyncio.to_thread(
        execute_tool,
        tool_name,
        raw_arguments,
    )
