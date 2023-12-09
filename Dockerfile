FROM python:3.11-slim
WORKDIR /white_elephant_bot
COPY . .
RUN pdm install
