from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View, TemplateView
from loja.models import Produto
from .carrinho import Carrinho
from .forms import CarrinhoAddProdutoForm


class CarrinhoAdd(FormView):
    form_class = CarrinhoAddProdutoForm
    success_url = reverse_lazy('carrinhodetalhe')

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        # removi esse redirect pois ele redireciona a página antes de realizar todas as operações que preciso
        # return redirect('carrinhodetalhe')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        carrinho = Carrinho(self.request)
        carrinho.addProduto(produto=self.produto,
                            quantidade=cd['quantidade'],
                            alterarquantidade=cd['atualizar']) # Mudei o nome aqui também para bater com o nome do campo no formulário
        return super().form_valid(form)


class CarrinhoRemove(View):

    def post(self, request, *args, **kwargs):
        self.produto = Produto.objects.get(id=kwargs['idprod'])
        carrinho = Carrinho(request)
        carrinho.removerProduto(self.produto)
        return redirect('carrinhodetalhe')


class CarrinhoDetalhe(TemplateView):
    template_name = 'carrinho/detalhe.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        carrinho = Carrinho(self.request)
        for item in carrinho:
            # alterei o nome do formulário aqui
            # esse formulário servirá para o cliente alterar a quantidade diretamente no carrinho.
            item['atualizarquantform'] = CarrinhoAddProdutoForm(initial={'quantidade':item['quantidade'],
                                                                         'alterarquantidade': True})
        contexto['carrinho'] = carrinho
        return contexto