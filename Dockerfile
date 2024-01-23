FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

RUN apt update

WORKDIR /app

COPY requirements.txt .

RUN apt install libpq-dev -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000


CMD [ "sh", "./init.sh" ]

# CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
