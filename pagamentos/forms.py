from typing import Any
from django import forms


class CheckoutForm(forms.Form):
    payment_method_nonce = forms.CharField(max_length=500, widget=forms.HiddenInput, required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        if not self.cleaned_data.get('self.metodo_pagamento_nonce'):
            raise forms.ValidationError('Não foi possível processar o pagamento. Tente novamente')
        return self.cleaned_data