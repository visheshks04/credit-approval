FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

RUN apt update

WORKDIR /app

COPY requirements.txt .

RUN apt install libpq-dev -y
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py makemigrations creditapproval
RUN python3 manage.py migrate
RUN python3 init_data.py
RUN python3 manage.py loaddata creditapproval/fixtures/customer.json
RUN python3 manage.py loaddata creditapproval/fixtures/loan.json

EXPOSE 8000

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
