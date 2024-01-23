from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from . import utils

from datetime import datetime, timedelta


@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        customer = serializer.save()

        response = {**serializer.data, "approved_limit": 36*customer.monthly_income}

        return Response(response, status=status.HTTP_201_CREATED) 

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_eligibility(request):
        
    try:
        response = utils.check_loan_eligibility(
            request.data['customer_id'],
            request.data['interest_rate'],
            request.data['loan_amount'],
            request.data['tenure']
        )

        return Response(response, status=status.HTTP_200_OK)
    except Exception as  e:
        return Response({"message": f"Exception occured: {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):

    try:
        eligibility_details = utils.check_loan_eligibility(
            request.data['customer_id'],
            request.data['interest_rate'],
            request.data['loan_amount'],
            request.data['tenure']
        )
        if not eligibility_details['approval']:
            return Response({'message': 'Loan is not approved because of low credit score'}, status=status.HTTP_200_OK)
        
        customer = get_object_or_404(Customer, pk=eligibility_details.get('customer_id', request.data['customer_id']))
        
        new_loan = Loan(
            loan_amount=request.data['loan_amount'],
            tenure=eligibility_details.get('tenure', request.data['tenure']),
            interest_rate=eligibility_details.get('corrected_interest_rate', request.data['interest_rate']),
            customer=customer,
            monthly_installment=eligibility_details.get('monthly_installment', None)
        )

        serializer = LoanSerializer(instance=new_loan, data={
            **request.data, **eligibility_details, "customer": CustomerSerializer(customer).data
        })

        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()

            return Response({
                'loan_id': serializer.data.get('id'),
                'customer_id': eligibility_details.get('customer_id', request.data['customer_id']),
                'loan_approved': eligibility_details.get('approval'),
                'message': f"Loan approved with an interest rate of {eligibility_details.get('corrected_interest_rate', request.data['interest_rate'])}",
                'monthly_installment': serializer.data.get('monthly_installment')
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as  e:
        return Response({"message": f"Exception occured: {e}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) 
def view_loan(request, loan_id):
    loan_instance = get_object_or_404(Loan, pk=loan_id)
    serializer = LoanSerializer(loan_instance)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        customer = get_object_or_404(Customer, pk=customer_id)
        loans = Loan.objects.filter(customer=customer)
        serializer = LoanSerializer(loans, many=True)
        current_date = datetime.today().date()
        
        response = [{
            "loan_id": loan.get('id'),
            "loan_amount": loan.get('loan_amount'),
            "interest_rate": loan.get('interest_rate'),
            "monthly_installment": loan.get('monthly_installment'),
            "repayments_left": max(0, 
                                   loan.get('tenure') 
                                   - (current_date.year - datetime.strptime(loan.get('start_date'), '%Y-%m-%d').date().year) * 12 
                                   + current_date.month - datetime.strptime(loan.get('start_date'), '%Y-%m-%d').date().month), ## Assuming the repayments are monthly
        } for loan in serializer.data]
        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": f"Exception occured: {e}"}, status=status.HTTP_400_BAD_REQUEST)
