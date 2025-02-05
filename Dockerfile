FROM python:3.11.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 13001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "13001", "--reload"]
