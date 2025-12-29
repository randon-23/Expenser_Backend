from rest_framework import serializers
from .models import Transaction, TransactionType, SubCategory, FinancialAccount
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.urls import reverse

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

    def validate_transaction_type_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Transaction type name must be at least 3 characters long.")
        
        if TransactionType.objects.filter(transaction_type_name=value).exists():
            raise serializers.ValidationError("Transaction type name must be unique.")
        return value
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})
        
class SubCategorySerializer(serializers.ModelSerializer):
    transaction_type = TransactionTypeSerializer(read_only=True)
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all(),
        source='transaction_type',
        write_only=True
    )

    class Meta:
        model = SubCategory
        fields = '__all__'

    def validate_subcategory_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Subcategory name must be at least 3 characters long.")
        
        if SubCategory.objects.filter(subcategory_name=value).exists():
            raise serializers.ValidationError("Subcategory name must be unique.")
        return value
    
    def validate_transaction_type(self, value):
        if value is None:
            raise serializers.ValidationError("Transaction type must be provided for the subcategory.")
        return value
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})

class FinancialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = '__all__'

    def validate_financial_account_name(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError("Financial account name must be at least 3 characters long.")
        
        if FinancialAccount.objects.filter(financial_account_name=value).exists():
            raise serializers.ValidationError("Financial account name must be unique.")
        return value
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})
        
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})

class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = TransactionTypeSerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    account_impacted = FinancialAccountSerializer(read_only=True)
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all(),
        source='transaction_type',
        write_only=True,
        required=True
    )
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(),
        source='subcategory',
        write_only=True,
        required=True
    )
    account_impacted_id = serializers.PrimaryKeyRelatedField(
        queryset=FinancialAccount.objects.all(),
        source='account_impacted',
        write_only=True,
        required=True
    )
    class Meta:
        model = Transaction
        fields = '__all__'
    
    def validate_transaction_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Transaction date cannot be in the future.")
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
    
    def validate(self, data):
        transaction_type = data.get('transaction_type')
        subcategory = data.get('subcategory')
        if subcategory and transaction_type:
            if subcategory.transaction_type.transaction_type_id != transaction_type.transaction_type_id:
                raise serializers.ValidationError(
                    {"subcategory": "Subcategory transaction type must match transaction transaction type."}
                )
        return data
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})
        
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error encountered:{str(e)}"})