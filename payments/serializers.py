# from rest_framework import serializers
# from .models import Payment
# class PaymentSerializer(serializers.ModelSerializer):
#     full_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Payment
#         fields = [
#             'id', 'reference', 'full_name', 'email', 'phone_number',
#             'amount', 'currency', 'state', 'country',
#             'status', 'created_at'
#         ]

#     def get_full_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"

from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 'email', 
            'amount', 'state', 'country', 'status', 'payment_id', 'created_at','reference'
        ]
        read_only_fields = ['id', 'status', 'payment_id', 'created_at', 'reference']
