# Установите базовый образ Python
FROM python:3.9

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте файл зависимостей в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте исходный код вашего приложения в контейнер
COPY . .

# Задайте команду для запуска приложения с флагом --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
