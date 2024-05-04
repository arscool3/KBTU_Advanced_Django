FROM python:3.11

WORKDIR /endterm

COPY ./requirements.txt .

RUN pip install --upgrade pip


RUN pip install -r requirements.txt
#
#COPY start.dramatiq.sh /start.dramatiq.sh
#RUN chmod +x /start.dramatiq.sh
#
#COPY ./start.fastapi.sh /start.fastapi.sh
#RUN chmod +x /start.fastapi.sh
#
#COPY ./start.journal.sh /start.journal.sh
#RUN chmod +x /start.journal.sh

COPY . ./