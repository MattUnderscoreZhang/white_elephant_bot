FROM python:3.11-slim
WORKDIR /white_elephant_bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .
