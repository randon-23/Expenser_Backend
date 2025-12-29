from django.urls import path
from . import api

urlpatterns = [
    path('', api.get_overview, name='api-overview'),
    path('transaction-type/', api.transaction_type_list, name='transaction-type-list'),
    path('transaction-type/<int:transaction_type_id>', api.transaction_type_detail, name='transaction-type-detail'),
    path('subcategory/', api.subcategory_list, name='subcategory-list'),
    path('subcategory/<int:subcategory_id>', api.subcategory_detail, name='subcategory-detail'),
    path('financial-account/', api.financial_account_list, name='financial-account-list'),
    path('financial-account/<int:financial_account_id>', api.financial_account_detail, name='financial-account-detail'),
    path('transaction/', api.transaction_list, name='transaction-list'),
    path('transaction/<uuid:transaction_id>', api.transaction_detail, name='transaction-detail'),
    path('reports/monthly/', api.monthly_report, name="monthly-report")
]