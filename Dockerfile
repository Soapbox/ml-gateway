# Base image
FROM python:3.7

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install project dependencies
WORKDIR /app/ml-gateway
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of API files into container
COPY . /app/ml-gateway

CMD [ "/bin/sh", "-c", "uvicorn api.main:app --reload --port 8500 --host 0.0.0.0" ]
