# Your Python version
FROM python:3.12-slim as taipy

# Web port of the application
EXPOSE 5000

RUN groupadd -r taipy && useradd -r -m -g taipy taipy
USER taipy

WORKDIR /home/taipy
ENV PATH="${PATH}:/home/taipy/.local/bin"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# Start up command
ENTRYPOINT [ "gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "--bind=0.0.0.0:5000", "--timeout", "0" ]
CMD [ "main:app" ]