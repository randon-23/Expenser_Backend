from django.contrib import admin
from .models import Transaction, TransactionType, SubCategory, FinancialAccount

admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(SubCategory)
admin.site.register(FinancialAccount)

# Register your models here.
