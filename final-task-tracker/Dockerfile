FROM python:3.11

WORKDIR /final

COPY ./requirements.txt .

RUN pip install --upgrade pip


RUN pip install -r requirements.txt

COPY ./start.fastapi.sh /start.fastapi.sh
RUN chmod +x /start.fastapi.sh

COPY ./start.journal.sh /start.journal.sh
RUN chmod +x /start.journal.sh

COPY . ./
