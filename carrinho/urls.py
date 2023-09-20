from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarrinhoDetalhe.as_view(), name='carrinhodetalhe'),
    path('add/<int:idprod>/', views.CarrinhoAdd.as_view(), name='carrinhoadd'),
    path('remove/<int:idprod>/', views.CarrinhoRemove.as_view(), name='carrinhoremove'),
]