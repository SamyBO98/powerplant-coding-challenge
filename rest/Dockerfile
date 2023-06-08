#Deriving the latest base image
FROM python:latest

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8888"]