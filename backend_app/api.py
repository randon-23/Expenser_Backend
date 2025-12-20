from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

@api_view(['GET'])
def get_overview(request):
    api_urls = {
        "transaction_types": {
            "List": "/api/transaction-types/",
            "Detail": "/api/transaction-types/<int:pk>/",
        },
        "subcategories": {
            "List": "/api/subcategories/",
            "Detail": "/api/subcategories/<int:pk>/",
        },
        "accounts": {
            "List": "/api/accounts/",
            "Detail": "/api/accounts/<int:pk>/",
        },
        "transactions": {
            "List": "/api/transactions/",
            "Detail": "/api/transactions/<uuid:transaction_id>/",
            "FilterByDate": "/api/transactions/?from=<yyyy-mm-dd>&to=<yyyy-mm-dd>/",
        },
        "reports": {
            "Monthly": "/api/reports/monthly/?year=<yyyy>&month=<mm>/",
        },
    }
    return Response(api_urls)

#functions are either collection based (Entire type) or detial based (specific ID)

@api_view(['GET', 'POST'])
def transaction_type_list(request):
    if request.method =='GET':
        types = TransactionType.objects.all()
        serializer = TransactionTypeSerializer(types, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transaction_type_detail(request, id):
    try:
        obj = TransactionType.objects.get(pk=id)
    except TransactionType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionTypeSerializer(obj)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        # PUT full update PATCH partial update semantic wise
        serializer = TransactionTypeSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)