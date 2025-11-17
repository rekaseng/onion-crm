# Pull base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System updates and installing necessary packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    tzdata \
    ttf-wqy-zenhei \
    ttf-wqy-microhei \
    wkhtmltopdf \
    build-essential \
    python3-pip \
    python3-dev

# Set timezone
ENV TZ="Asia/Singapore"

# Install Poetry
RUN pip3 install -U pip setuptools wheel
RUN pip3 install poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory in the container
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry install --no-dev  # Assumes that your production environment does not need development dependencies

# Copy the content of the local src directory to the working directory
COPY ./src/ .

# Uvicorn will listen on port 8000
EXPOSE 8000

# The ENTRYPOINT defines the command to run the app
ENTRYPOINT ["uvicorn", "main:app", "--reload",  "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]