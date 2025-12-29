from django.db.models import Sum
from .models import Transaction
from itertools import groupby
from operator import itemgetter

def generate_monthly_report(year, month):
    trxs = Transaction.objects.filter(
        transaction_date__year=year,
        transaction_date__month=month
    )

    totals_by_type_qs = (
        trxs.values("transaction_type__transaction_type_name")
        .annotate(total_amount=Sum("amount"))
        .order_by("transaction_type__transaction_type_name")
    )

    totals_by_subcategory_qs = (
        trxs.values(
            "transaction_type__transaction_type_name",
            "subcategory__subcategory_name",
        )
        .annotate(total_amount=Sum("amount"))
        .order_by("transaction_type__transaction_type_name",
                  "subcategory__subcategory_name")
    )

    totals_by_type = [
        {
            "transaction_type": row["transaction_type__transaction_type_name"],
            "total_amount": row["total_amount"],
        }
        for row in totals_by_type_qs
    ]

    key_fn = itemgetter("transaction_type__transaction_type_name")
    totals_by_subcategory = {}
    for trans_type, group in groupby(totals_by_subcategory_qs, key=key_fn):
        totals_by_subcategory[trans_type] = [
            {
                "subcategory": row["subcategory__subcategory_name"],
                "total_amount": row["total_amount"],
            }
            for row in group
        ]

    return {
        "year": year,
        "month": month,
        "totals_by_type": totals_by_type,
        "totals_by_subcategory": totals_by_subcategory,
    }