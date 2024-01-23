python3 manage.py makemigrations creditapproval

python3 manage.py migrate
python3 init_data.py
python3 manage.py loaddata creditapproval/fixtures/customer.json
python3 manage.py loaddata creditapproval/fixtures/loan.json

python3 manage.py runserver 0.0.0.0:8000