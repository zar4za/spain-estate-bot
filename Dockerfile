FROM python:3.10
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY ./src ./app

WORKDIR /app
CMD ["python", "-u", "./main.py"]