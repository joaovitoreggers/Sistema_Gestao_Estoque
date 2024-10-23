from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
import stripe
from .models import Payment, Company

# Configure a chave secreta da Stripe
stripe.api_key = "sk_test_51Q84WcGCcu8ObJFYddt3hcdCpMaCNVNfIwKucxqW0Z0NGoOagsSMYqcHAxNaejH7gCzHje4VTk9pFrNm0viXg8lz00xc7YTHV3"

class PaymentView(View):
    def get(self, request):
        return render(request, 'payment_form.html')

class BasePaymentView(View):
    def process_payment(self, request, payment_method):
        amount = float(request.POST.get('amount', 0))  # Valor informado pelo usuário
        user = request.user
        company_id = request.POST.get('company_id')  # ID da companhia
        company = get_object_or_404(Company, id=company_id)

        # Adiciona a taxa de R$1,00
        total_amount = amount + 1.00  # Taxa de R$1,00

        try:
            # Cria um Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Valor em centavos
                currency='brl',
                payment_method_types=[payment_method],
                transfer_data={
                    'destination': company.stripe_account_id,  # ID da conta da empresa na Stripe
                },
            )

            # Registre o pagamento no banco de dados
            payment = Payment.objects.create(user=user, amount=amount, payment_method=payment_method, company=company)
            return JsonResponse({'success': True, 'client_secret': intent.client_secret})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class BoletoPaymentView(BasePaymentView):
    def post(self, request):
        return self.process_payment(request, 'boleto')

class PixPaymentView(BasePaymentView):
    def post(self, request):
        return self.process_payment(request, 'pix')

class CardPaymentView(BasePaymentView):
    def post(self, request):
        return self.process_payment(request, 'card')

class CashPaymentView(View):
    def post(self, request):
        amount = float(request.POST.get('amount', 0))  # Valor informado pelo usuário
        user = request.user
        company_id = request.POST.get('company_id')  # ID da companhia
        company = get_object_or_404(Company, id=company_id)

        # Adiciona a taxa de R$1,00
        total_amount = amount + 1.00  # Taxa de R$1,00

        # Registre o pagamento como recebido em dinheiro
        payment = Payment.objects.create(user=user, amount=amount, payment_method='cash', status='succeeded', company=company)
        return JsonResponse({'success': True})
