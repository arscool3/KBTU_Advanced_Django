FROM python as builder

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /project

WORKDIR /project/core

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "fastapi_app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
