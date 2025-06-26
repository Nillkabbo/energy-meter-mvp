FROM python:3.9 as base
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . /code

# Create run scripts
RUN echo '#!/bin/bash\ncd /code && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload' > /run-dev.sh && \
    echo '#!/bin/bash\ncd /code && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000' > /run.sh && \
    chmod +x /run*.sh

FROM base as prod
ENV ENV=prod
CMD ["/run.sh"]

FROM base as test
ENV ENV=test
CMD ["/run.sh"]

FROM base as dev
ENV ENV=dev
CMD ["/run-dev.sh"] 