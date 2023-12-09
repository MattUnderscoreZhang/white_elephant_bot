FROM python:3.11-slim
WORKDIR /white_elephant_bot
COPY . .
RUN pip install pdm
RUN pdm install
CMD ["pdm", "run", "hypercorn", "main:app", "--bind", "[::]:$PORT"]
