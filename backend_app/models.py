from django.db import models
from django.core.exceptions import ValidationError
import uuid


class TransactionType(models.Model):
    transaction_type_id = models.AutoField(primary_key=True)
    transaction_type_name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_type_name


class SubCategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=100)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    description = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subcategory_name


class FinancialAccount(models.Model):
    SAVINGS = "SAVINGS"
    CREDIT_CARD = "CREDIT_CARD"
    CURRENT = "CURRENT"
    INVESTMENTS = "INVESTMENTS"
    PENSION_PLAN = "PENSION_PLAN"

    FINANCIAL_ACCOUNT_TYPES = [
        (SAVINGS, "Savings"),
        (CREDIT_CARD, "Credit card"),
        (CURRENT, "Current"),
        (INVESTMENTS, "Investments"),
        (PENSION_PLAN, "Pension plan"),
    ]

    financial_account_id = models.AutoField(primary_key=True)
    financial_account_name = models.CharField(max_length=75)
    financial_account_type = models.CharField(
        max_length=50,
        choices=FINANCIAL_ACCOUNT_TYPES,
        default=CURRENT,
    )

    def __str__(self):
        return self.financial_account_name


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    account_impacted = models.ForeignKey(
        FinancialAccount,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.subcategory and self.transaction_type:
            if self.subcategory.transaction_type.transaction_type_id != self.transaction_type.transaction_type_id:
                raise ValidationError(
                    {"subcategory": "Subcategory transaction type must match transaction transaction type."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_date} {self.amount} ({self.subcategory})"
