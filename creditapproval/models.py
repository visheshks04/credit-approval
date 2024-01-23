from django.db import models
from datetime import date

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    monthly_income = models.IntegerField(blank=True, null=True)

    ## Calculate approved_limit dynamically 36*monthly_salary
    ## Also current_debt whenever needed can be derived

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    start_date = models.DateField(default=date.today)


    def save(self, *args, **kwargs):
        if self.monthly_installment is None:
            self.monthly_installment = self.calculate_monthly_installment()
        super().save(*args, **kwargs)
   

    def calculate_monthly_installment(self):
        if self.loan_amount > 0 and self.interest_rate > 0 and self.tenure > 0:
            monthly_interest_rate = (self.interest_rate / 100) / 12

            monthly_installment = (self.loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -self.tenure)

            return round(monthly_installment, 2)

        return None

    def __str__(self):
        return f"Loan of {self.loan_amount} for {self.customer}"

