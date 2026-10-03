FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.21 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

COPY src/ ./src/

RUN uv sync --locked --no-dev

CMD ["uv", "run", "uvicorn", "docs_action_agent.api:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD [ "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" ]
