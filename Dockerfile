FROM python:3.12.8-slim-bookworm
LABEL authors="Ernesto Crespo <ernesto@asistensi.com>"


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app
COPY .env /app/

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
#CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
CMD ["uv", "run","--env-file", ".env", "python3", "run.py"]