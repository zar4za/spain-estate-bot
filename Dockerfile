FROM python:3.10
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY appsettings.json appsettings.json

WORKDIR /app
COPY ./src .

CMD ["python", "-u", "./main.py"]