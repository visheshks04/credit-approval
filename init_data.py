import pandas as pd
from datetime import date
import json

customer_fixture = []
loan_fixture = []

customer_data = pd.read_excel('customer_data.xlsx')

for index, row in customer_data.iterrows():
    customer_fixture.append({
        "model": "creditapproval.customer",
        "pk": row['Customer ID'],
        "fields": {
            "first_name": row['First Name'],
            "last_name": row['Last Name'],
            "age": row['Age'],
            "phone_number": row['Phone Number'],
            "monthly_income": int(row['Monthly Salary'])
        }
    })



loan_data = pd.read_excel('loan_data.xlsx')

for index, row in loan_data.iterrows():
    loan_fixture.append({
        "model": "creditapproval.loan",
        "pk": row['Loan ID'],
        "fields": {
            "loan_amount": int(row['Loan Amount']),
            "tenure": int(row['Tenure']),
            "interest_rate": float(row['Interest Rate']),
            "customer": row['Customer ID'],
            "monthly_installment": int(row['Monthly payment']),
            "start_date": str(row['Date of Approval'].date())
        }
    })

with open('creditapproval/fixtures/customer.json', 'w') as json_file:
    json.dump(customer_fixture, json_file, indent=2)

with open('creditapproval/fixtures/loan.json', 'w') as json_file:
    json.dump(loan_fixture, json_file, indent=2)
