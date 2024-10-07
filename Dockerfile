FROM python:3.12.1-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . /app/

CMD ["poetry", "run", "python", "main.py"]
