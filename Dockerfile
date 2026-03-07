FROM python:3.12-alpine

WORKDIR /app

ENV POETRY_VERSION=2.1.3
ENV POETRY_VENV=/opt/poetry-venv

ENV PATH="$POETRY_VENV/bin:$PATH"

RUN python3 -m venv $POETRY_VENV &&  
  $POETRY_VENV/bin/pip install -U pip setuptools &&  
  $POETRY_VENV/bin/pip install poetry==$POETRY_VERSION &&  
  poetry config virtualenvs.create false 

COPY pyproject.toml poetry.lock* .

RUN poetry install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]