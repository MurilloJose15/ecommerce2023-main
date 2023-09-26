from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from carrinho.carrinho import Carrinho
from pedidos.forms import PedidoModelForm
from .models import ItemPedido, Pedido


class PedidoCreateView(CreateView):
    form_class = PedidoModelForm
    success_url = reverse_lazy('resumopedido')
    template_name = 'formpedido.html'

    def form_valid(self, form):
        car = Carrinho(request=self.request)
        pedido = form.save()
        for item in car:
            ItemPedido.objects.create(pedido=pedido,
                                      produto=item['produto'],
                                      preco=item['preco'],
                                      quantidade=item['quantidade'])
        car.limpar()
        self.request.session['idpedido'] = pedido.id
        self.email_validator_pedido(pedido)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resumopedido', args=[self.object.id])

    def email_validator_pedido(self, pedido: Pedido) -> None:
        subject = 'Confirmação de pedido'
        from_email = 'pedido@loja.com'
        to = [pedido.email]
        text_content = render_to_string('email_validator_pedido.txt', {'pedido': pedido})
        html_content = render_to_string('email_validator_pedido.html', {'pedido': pedido})

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, 'text/html')
        email.send()

class ResumoPedidoTemplateView(TemplateView):
    template_name = 'resumopedido.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pedido'] = Pedido.objects.get(id=self.kwargs['idpedido'])
        return ctx

