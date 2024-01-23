from .models import *
from .serializers import LoanSerializer
from django.shortcuts import get_object_or_404

def calculate_monthly_installment(amount, interest_rate, tenure):
    if amount > 0 and interest_rate > 0 and tenure > 0:

        monthly_interest_rate = (interest_rate / 100) / 12
        monthly_installment = (amount * interest_rate) / (1 - (1 + interest_rate) ** -tenure)

        return round(monthly_installment, 2)
    
    return None


def get_credit_rating(customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    loans = Loan.objects.filter(customer=customer)
    serializer = LoanSerializer(loans, many=True)

    n_loans = len(serializer.data)
    sum_of_loans = sum([int(loan['loan_amount']) for loan in serializer.data])
    
    if sum_of_loans > customer.monthly_income*36:
        return 0
    elif sum_of_loans > customer.monthly_income*27:
        return 25
    elif sum_of_loans > customer.monthly_income*18:
        return 50
    elif sum_of_loans > customer.monthly_income*9 and n_loans < 3:
        return 90
    else:
        return 75
    
    ## Wrote a dummy logic for credit rating for now

    return 0


def check_loan_eligibility(customer_id, interest_rate, loan_amount, tenure):
    credit_rating = get_credit_rating(customer_id)
    corrected_interest_rate = interest_rate

    if credit_rating > 50:
        approval = True
    elif credit_rating > 30:
        corrected_interest_rate = 12
        approval = True
    elif credit_rating > 10:
        corrected_interest_rate = 16
        approval = True
    else:
        approval = False


    return {
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": calculate_monthly_installment(
            loan_amount,
            corrected_interest_rate,
            tenure
        )
    }