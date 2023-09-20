from django import forms
from .models import Pedido


class PedidoModelForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['nome', 'sobrenome', 'email', 'endereco', 'cep', 'cidade']

