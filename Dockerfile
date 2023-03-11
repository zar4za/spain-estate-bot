FROM python:3.10
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY appsettings.json appsettings.json

WORKDIR /src
COPY ./src .

CMD ["python", "-u", "./main.py"]