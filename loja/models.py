from django.db import models


class ProdDisponiveisManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(disponivel=True)

class Categoria(models.Model):
    nome = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    objects = models.Manager()
    disponiveis = ProdDisponiveisManager()
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    disponivel = models.BooleanField(default=True)
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nome',)
        index_together = (('id','slug'),)
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome