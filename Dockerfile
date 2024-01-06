FROM python:3.11-alpine
RUN apk update && apk add ffmpeg
RUN apk add libmagic
RUN apk add chromaprint

COPY *.py .
COPY shazam_cli_py_master .
COPY youtube_title_parse .
COPY requirements.txt .
COPY .env .

RUN  pip install --upgrade pip && pip install -r requirements.txt

CMD ["python","./main.py"]