# urls.py
from django.urls import path
from .views import PaymentView, BoletoPaymentView, PixPaymentView, CardPaymentView, CashPaymentView

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment_form'),  # Página do formulário de payment
    path('payment/boleto/', BoletoPaymentView.as_view(), name='boleto_payment'),  # payment via Boleto
    path('payment/pix/', PixPaymentView.as_view(), name='pix_payment'),  # payment via Pix
    path('payment/card/', CardPaymentView.as_view(), name='card_payment'),  # payment via Cartão
    path('payment/cash/', CashPaymentView.as_view(), name='cash_payment'),  # payment em Dinheiro
]
