# The Self-Teaching Humanoid — back end + front-end surfaces + simulated robot.
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3", "-m", "backend.app"]
