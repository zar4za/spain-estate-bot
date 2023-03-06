FROM python:3.9
COPY requirements.txt .
RUN pip install --user -r requirements.txt

WORKDIR /app
COPY ./src .

CMD ["python", "-u", "./main.py"]