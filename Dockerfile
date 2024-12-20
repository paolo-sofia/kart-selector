# Your Python version
FROM python:3.12-slim as taipy

# Web port of the application

#RUN groupadd -r taipy && useradd -r -m -g taipy taipy
#USER taipy

#WORKDIR /home/taipy
#ENV PATH="${PATH}:/home/taipy/.local/bin"
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health


ENTRYPOINT ["streamlit", "run", "sorteggio_piazzola.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Start up command
#ENTRYPOINT [ "gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "--bind=0.0.0.0:5000", "--timeout", "0" ]
#CMD [ "main:app" ]
#ENTRYPOINT [ "python", "main.py", "-P", "5000", "-H", "0.0.0.0", "--no-reloader" ]
#CMD python main.py -P 5000 -H 0.0.0.0 --debug
