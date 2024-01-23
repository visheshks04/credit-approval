def calculate_monthly_installment(amount, interest_rate, tenure):
    return 0 ## TODO


def get_credit_rating(customer_id):
    return 50 ## TODO

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