FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["sh", "-c", "sleep 3 && python app.py"]
