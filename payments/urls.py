from django.urls import path
from .views import PaymentCreateView, PaymentStatusView

urlpatterns = [
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
    #path('api/v1/payments/<uuid:pk>/', PaymentStatusView.as_view(), name='payment-status'),
    path('api/v1/payments/<str:payment_id>/', PaymentStatusView.as_view(), name='payment-status'),

    #path('payments/<int:pk>/status/', PaymentStatusView.as_view(), name='payment-status'),


]
