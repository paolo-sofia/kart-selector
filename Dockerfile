FROM python:3.13-alpine

RUN apk update && apk add py3-pyarrow && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --break-system-packages -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health


ENTRYPOINT ["streamlit", "run", "sorteggio_sessione.py", "--server.port=8501", "--server.address=0.0.0.0"]
