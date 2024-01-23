from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register, name="register"),
    path("check-eligibility/", check_eligibility, name="check-eligibility"),
    path("create-loan/", create_loan, name="create-loan"),
    path("view-loan/<int:loan_id>/", view_loan, name="view-loan"),
    path("view-loans/<int:customer_id>/", view_loans, name="view-loans")
]
