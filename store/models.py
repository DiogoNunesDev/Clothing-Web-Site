from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator #delimita o numero de 'digitos' (maximo numero possivel aceite)

class Produto(models.Model):
    tamanho = models.CharField(max_length=1)
    cor = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    num_pontos = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50)
    referencia = models.CharField(max_length=4, default="0")
    #image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.categoria + " - " + self.cor + " - " + self.tamanho + " - " + str(self.preco)

    def makeProduct(t, c, p, np, cat):
        product = Produto(tamanho=t, cor=c, preco=p, num_pontos=np, categoria=cat)
        product.save()
class CarrinhoCompras(models.Model):
    num_itens = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.num_itens) + " - " + str(self.valor_total)

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primeiro_nome = models.CharField(max_length=50)
    apelido = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=150)
    numero_telemovel = models.IntegerField(default=0, validators=[MaxValueValidator(999999999)])
    num_cartao_cidadao = models.IntegerField(default=0, validators=[MaxValueValidator(999999999)])
    nif = models.IntegerField(default=0, validators=[MaxValueValidator(999999999)])
    email = models.EmailField(max_length=150, default="defaultMail@gmail.com")
    num_pontos = models.IntegerField(default=0)
    # image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.primeiro_nome + " " + self.apelido + " - " + str(self.num_cartao_cidadao) + " - " + str(self.num_pontos)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primeiro_nome = models.CharField(max_length=50)
    apelido = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=150)
    numero_telemovel = models.IntegerField(default=0, validators=[MaxValueValidator(999999999)])
    num_cartao_cidadao = models.IntegerField(default=0, validators=[MaxValueValidator(999999999)])
    email = models.EmailField(max_length=150, default="defaulStaffMail@gmail.com")

    def __str__(self):
        return self.primeiro_nome + " " + self.apelido + " - " + str(self.num_cartao_cidadao)

