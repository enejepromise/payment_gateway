# from django.test import TestCase

# # Create your tests here.
# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import Payment

# class PaymentAPITestCase(APITestCase):
#     def setUp(self):
#         self.payment_data = {
#             "first_name": "John",
#             "last_name": "Doe",
#             "phone_number": "1234567890",
#             "email": "john@example.com",
#             "amount": "50.00",
#             "state": "Lagos",
#             "country": "Nigeria"
#         }

#     def test_initiate_payment(self):
#         url = reverse('payment-create')
#         response = self.client.post(url, self.payment_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['status'], 'success')
#         self.assertIn('payment', response.data)
#         self.assertIn('authorization_url', response.data)

#     def test_get_payment_status(self):
#         # Create a payment instance
#         payment = Payment.objects.create(
#             first_name="Jane",
#             last_name="Smith",
#             phone_number="0987654321",
#             email="jane@example.com",
#             amount="20.00",
#             state="Abuja",
#             country="Nigeria",
#             payment_id="PAY-123",
#             status="completed"
#         )
#         url = reverse('payment-status', kwargs={'payment_id': payment.payment_id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         #url = reverse('payment-status', kwargs={'pk': payment.pk})
#         #response = self.client.get(url)
#         #self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'success')
#         self.assertEqual(response.data['payment']['customer_email'] if 'customer_email' in response.data['payment'] else response.data['payment']['email'], "jane@example.com")

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Payment

class PaymentAPITestCase(APITestCase):
    def setUp(self):
        self.payment_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "email": "john@example.com",
            "amount": "50.00",
            "state": "Lagos",
            "country": "Nigeria"
        }

    def test_initiate_payment(self):
        url = reverse('payment-create')
        response = self.client.post(url, self.payment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('payment', response.data)
        self.assertIn('authorization_url', response.data)

    @patch("payments.views.verify_payment")  
    def test_get_payment_status(self, mock_verify_payment):
        mock_verify_payment.return_value = {
            "status": True,
            "data": {"status": "success"},
            "message": "Payment verified"
        }

        payment = Payment.objects.create(
            first_name="Jane",
            last_name="Smith",
            phone_number="0987654321",
            email="jane@example.com",
            amount="20.00",
            state="Abuja",
            country="Nigeria",
            payment_id="PAY-123",
            status="created"
        )

        url = reverse('payment-status', kwargs={'payment_id': payment.payment_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['payment']['email'], "jane@example.com")
