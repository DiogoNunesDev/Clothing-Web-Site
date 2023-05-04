from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator #delimita o numero de 'digitos' (maximo numero possivel aceite)

class Produto(models.Model):
    tamanho = models.CharField(max_length=1)
    cor = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    num_pontos = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50)
    referencia = models.CharField(max_length=4)
    image = models.CharField(max_length=255, default="whiteLogo.png")
    stock = models.IntegerField(default=0)
    def __str__(self):
        return self.categoria + " - " + self.tamanho + " - " + self.cor + " -> " + str(self.preco) + "€"

    def makeProduct(tamanho, cor, preco, num_pontos, categoria, referencia, image, stock):
        product = Produto(tamanho=tamanho, cor=cor, preco=preco, num_pontos=num_pontos, categoria=categoria, referencia=referencia, image=image, stock=stock)
        product.save()

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

class CarrinhoCompras(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, default=None)
    num_itens = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return str(self.num_itens) + " - " + str(self.valor_total)

class carrinhoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(CarrinhoCompras, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.produto} (x{self.quantidade})'


class Compra(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    itens_comprados = models.ManyToManyField(carrinhoItem)
    data_compra = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Compra #{self.pk} - {self.data_compra}'



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


class Comentario(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=2000)
    data = models.DateField()
    image = models.CharField(max_length=255, default="pescadaDraw.png")

"""
Funções para dar reset a base de dados, caso seja preciso


from django.db import connection

def reset_sequence_staff(new_value):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE sqlite_sequence SET seq = {new_value} WHERE name = 'store_staff'")


def reset_sequence_user(new_value):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE sqlite_sequence SET seq = {new_value} WHERE name = 'auth_user'")


def reset_sequence_utilizador(new_value):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE sqlite_sequence SET seq = {new_value} WHERE name = 'store_utilizador'")
  

"""
