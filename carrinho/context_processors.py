from .carrinho import Carrinho


def carrinho(request):
    return {'carrinho': Carrinho(request)}