# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"
FROM python:3.10

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

    # Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1 \
    # Don't create `.pyc` files:
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR ${WORKDIR}
COPY . .
RUN poetry install --only main

CMD ["./.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
