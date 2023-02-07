FROM python:3.9
COPY requirements.txt .
RUN pip install --user -r requirements.txt

WORKDIR /source
COPY main.py .
COPY estate.py .
COPY tg.py .
COPY config.json .

CMD ["python", "-u", "./main.py"]