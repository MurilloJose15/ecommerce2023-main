from decimal import Decimal

from django.conf import settings

from loja.models import Produto


class Carrinho(object):

    def __init__(self, request):
        """
        Inicializa o carrinho de compras
        """
        self.session = request.session
        carrinho = self.session.get(settings.CARRINHO_SESSION_ID)
        if not carrinho:
            carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}
        self.carrinho = carrinho

    def addProduto(self, produto, quantidade=1, alterarquantidade=False):
        """
        Adiciona um produto ao carrinho de compras ou atualiza sua quantidade
        :param produto: o produto a ser inserido ou atualizado a quantidade
        :param quantidade: a quantidade do produto a ser adicionado
        :param alterarquantidade: quando necessário a alteração da quantidade do produto
        :return:
        """
        idprod = str(produto.id)
        if idprod not in self.carrinho:
            self.carrinho[idprod] = {'quantidade': 0,
                                     'preco': str(produto.preco)}
        if alterarquantidade:
            self.carrinho[idprod]['quantidade'] = quantidade
        else:
            self.carrinho[idprod]['quantidade'] += quantidade
        self._salvar()

    def _salvar(self):
        self.session.modified = True


    def removerProduto(self, produto):
        """
        Remove um produto do carrinho de compras
        :param produto: o produto a ser excluído
        :return: sem retorno
        """
        idprod = str(produto.id)
        if idprod in self.carrinho:
            del self.carrinho[idprod]
            self._salvar()

    def __iter__(self):
        """
        Itera sobre os itens do carrinho e obtem os produtos do banco de dados
        :return:
        """
        idsprodutos = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=idsprodutos)
        carrinho = self.carrinho.copy()
        for p in produtos:
            carrinho[str(p.id)]['produto'] = p
        for item in carrinho.values():
            item['preco'] = Decimal(item['preco'])
            item['preco_total'] = item['preco'] * item['quantidade']
            yield item

    def __len__(self):
        """
        Soma a quantidade de itens que o carrinho possui
        :return: A quantidade de itens do carrinho
        """
        return sum(item['quantidade'] for item in self.carrinho.values())

    def get_preco_total(self):
        return sum(Decimal(item['preco']) * item['quantidade'] for item in self.carrinho.values())

    def limpar(self):
        del self.session[settings.CARRINHO_SESSION_ID]
        self._salvar()