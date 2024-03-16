FROM python:3.12
WORKDIR /stalku
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./stalku /stalku
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
