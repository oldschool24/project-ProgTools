FROM python:3.8-slim-buster
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]
