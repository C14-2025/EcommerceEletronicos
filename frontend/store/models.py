from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
