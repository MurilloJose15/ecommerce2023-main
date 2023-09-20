from django.contrib import admin

from .models import Pedido, ItemPedido


class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    raw_id_fields = ['produto']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sobrenome', 'email', 'pago', 'criado', 'atualizado']
    list_filter = ['pago', 'criado', 'atualizado']
    inlines = [ItemPedidoInLine]
