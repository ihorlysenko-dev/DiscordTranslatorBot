FROM python:3.11.2

WORKDIR /DiscordTranslateBot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./main.py"]