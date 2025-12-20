from django.urls import path
from . import api

urlpatterns = [
    path('', api.get_overview, name='api-overview'),
    path('transactions-type-list/', api.transaction_type_list, name='transaction-type-list'),
    path('transaction-type-detail/<int:transaction_type_id>', api.transaction_type_detail, name='transaction-type-detail')
]