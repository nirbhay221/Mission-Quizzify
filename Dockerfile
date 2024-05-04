FROM python:3.9-slim AS backend

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="authentication.json"

CMD ["streamlit","run","tasks/task_10/task_10.py"]