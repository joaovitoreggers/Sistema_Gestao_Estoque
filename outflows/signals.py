from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Outflow, Product

class OutflowCreateView(CreateView):
    model = Outflow
    template_name = 'outflows/outflow_create.html'
    success_url = reverse_lazy('outflow_list')

    def form_valid(self, form):
        # Captura a instância do Outflow que está sendo criada
        outflow = form.save(commit=False)

        # Itera sobre os produtos selecionados
        for product_id, quantity in zip(outflow.selected_products.split(','), outflow.quantities.split(',')):
            product = Product.objects.get(id=product_id)

            if product.quantity < int(quantity):
                # Adiciona uma mensagem de erro se a quantidade não for suficiente
                messages.error(self.request, f'Quantidade insuficiente em estoque para o produto {product.title}.')
                return self.form_invalid(form)  # Retorna o formulário inválido

            # Atualiza a quantidade do produto
            product.quantity -= int(quantity)
            product.save()

        # Salva o Outflow se todas as condições forem atendidas
        outflow.save()
        return super().form_valid(form)
