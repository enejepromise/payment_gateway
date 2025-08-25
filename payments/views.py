# from rest_framework import status, generics
# from rest_framework.response import Response
# from .models import Payment
# from .serializers import PaymentSerializer
# from .utils import initialize_payment, verify_payment

# class PaymentCreateView(generics.CreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         payment = serializer.save(status="pending")  # default new payment status

#         # Call your payment gateway initialization (e.g. Paystack)
#         paystack_response = initialize_payment(payment.email, payment.amount)

#         if paystack_response.get("status"):
#             payment.reference = paystack_response["data"]["reference"]
#             payment.save()

#             return Response({
#                 "payment": PaymentSerializer(payment).data,
#                 "authorization_url": paystack_response["data"]["authorization_url"],
#                 "status": "success",
#                 "message": "Payment initiated successfully. Redirect customer to authorization_url."
#             }, status=status.HTTP_201_CREATED)

#         return Response({
#             "status": "error",
#             "message": "Failed to initiate payment",
#             "details": paystack_response
#         }, status=status.HTTP_400_BAD_REQUEST)


# class PaymentDetailView(generics.RetrieveAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#     lookup_field = 'id'  # URL expects payment UUID

#     def get(self, request, *args, **kwargs):
#         payment = self.get_object()

#         # Optionally verify payment status from gateway before returning
#         verification_response = verify_payment(payment.reference)
#         if verification_response.get("status") == "success":
#             new_status = verification_response["data"]["status"]
#             if payment.status != new_status:
#                 payment.status = new_status
#                 payment.save()

#         serializer = self.get_serializer(payment)
#         return Response({
#             "payment": serializer.data,
#             "status": "success",
#             "message": "Payment details retrieved successfully."
#         }, status=status.HTTP_200_OK)
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer
from .utils import initialize_payment, verify_payment  

class PaymentCreateView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Call utility to initialize payment on Paystack
            response_data = initialize_payment(email=data['email'], amount=data['amount'])
            if response_data.get('status'):
                paystack_data = response_data.get('data', {})
                auth_url = paystack_data.get('authorization_url')
                ref = paystack_data.get('reference')
                # Create Payment instance in DB
                payment_obj = Payment.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    phone_number=data['phone_number'],
                    email=data['email'],
                    amount=data['amount'],
                    state=data['state'],
                    country=data['country'],
                    reference=ref,
                    status='created'
                )
                return Response({
                    "payment": PaymentSerializer(payment_obj).data,
                    "status": "success",
                    "message": "Payment initiated successfully.",
                    "authorization_url": auth_url
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status": "error",
                    "message": response_data.get('message', 'Payment initialization failed.')
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusView(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            # Use utility to verify payment status on Paystack
            response_data = verify_payment(payment.reference)
            if response_data.get('status'):
                paystack_status = response_data['data'].get('status')
                payment.status = paystack_status
                payment.save()
                return Response({
                    "payment": PaymentSerializer(payment).data,
                    "status": "success",
                    "message": "Payment details retrieved successfully."
                })
            else:
                return Response({
                    "status": "error",
                    "message": response_data.get('message', 'Could not verify payment status.')
                }, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"status": "error", "message": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
