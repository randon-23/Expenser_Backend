from django.shortcuts import render
from .models import *
from .serializers import *
from .reports import generate_monthly_report
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'DELETE'])
def transaction_type_detail(request, transaction_type_id):
    try:
        obj = TransactionType.objects.get(pk=transaction_type_id)
    except TransactionType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionTypeSerializer(obj)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = TransactionTypeSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'POST'])
def subcategory_list(request):
    if request.method =='GET':
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'DELETE'])
def subcategory_detail(request, subcategory_id):
    try:
        obj = SubCategory.objects.get(pk=subcategory_id)
    except SubCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubCategorySerializer(obj)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = SubCategorySerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'POST'])
def financial_account_list(request):
    if request.method =='GET':
        accounts = FinancialAccount.objects.all()
        serializer = FinancialAccountSerializer(accounts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FinancialAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def financial_account_detail(request, financial_account_id):
    try:
        obj = FinancialAccount.objects.get(pk=financial_account_id)
    except FinancialAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FinancialAccountSerializer(obj)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = FinancialAccountSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'POST'])
def transaction_list(request):
    #Only GET requests with from/to date filters are allowed - no full list retrieval
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        if 'from' in request.GET or 'to' in request.GET:
            if 'from' in request.GET and 'to' in request.GET:
                from_date = request.GET['from']
                to_date = request.GET['to']
                transactions = transactions.filter(transaction_date__range=[from_date, to_date])
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif 'from' in request.GET:
                from_date = request.GET['from']
                transactions = transactions.filter(transaction_date__gte=from_date)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif 'to' in request.GET:
                to_date = request.GET['to']
                transactions = transactions.filter(transaction_date__lte=to_date)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Require from or to date parameters to return transactions"})
        
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def transaction_detail(request, transaction_id):
    try:
        obj = Transaction.objects.get(pk=transaction_id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionSerializer(obj)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = TransactionSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
def monthly_report(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')

        if not year or not month:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Year and month parameters are required."})
        
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Year and month must be integers."}
            )
        
        trxs = generate_monthly_report(year, month)
        return Response(trxs, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)