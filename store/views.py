from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from store.models import Produto, Utilizador, Staff
from django.urls import reverse


def home(request):
    return render(request, 'home.html')

def full_collection(request):
    product_list = Produto.objects.all()
    context = {'product_list': product_list}
    return render(request, 'full_collection.html', context)

def cart_view(request):
    return render(request, 'cart.html')


def login_view(request):

    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            # reverse: quando estou dentro dos templates vai procurar o index e vai gerar o url correspondente
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'msg_erro':'Credenciais inválidas, tente novamente.'})
    else:
        #Mostrar o formulario de login
        return render(request, 'login.html')


def redirectLogin(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=name, password=password, email=email)
        user.save()
        primeiro_nome = request.POST['primeiro_nome']
        apelido = request.POST['apelido']
        data_nascimento = request.POST['data_nascimento']
        morada = request.POST['morada']
        numero_telemovel = request.POST['numero_telemovel']
        num_cartao_cidadao = request.POST['num_cartao_cidadao']
        nif = request.POST['nif']
        utilizador = Utilizador(user=user, primeiro_nome=primeiro_nome, apelido=apelido, data_nascimento=data_nascimento, morada=morada,
                                numero_telemovel=numero_telemovel, num_cartao_cidadao=num_cartao_cidadao, nif=nif, num_pontos=0, email=email)
        utilizador.save()
        login(request, user)
        return render(request, 'home.html')


def redirectSignup(request):
    return render(request, 'signup.html')


def addStaff(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=name, password=password, email=email)
        user.save()
        primeiro_nome = request.POST['primeiro_nome']
        apelido = request.POST['apelido']
        data_nascimento = request.POST['data_nascimento']
        morada = request.POST['morada']
        numero_telemovel = request.POST['numero_telemovel']
        num_cartao_cidadao = request.POST['num_cartao_cidadao']
        staff = Staff(user=user, primeiro_nome=primeiro_nome, apelido=apelido, data_nascimento=data_nascimento, morada=morada,
                        numero_telemovel=numero_telemovel, num_cartao_cidadao=num_cartao_cidadao, email=email)
        staff.save()
        return render(request, 'home.html')
    return render(request, 'addStaff.html')

def redirectAddStaff(request):
    return render(request, 'addStaff.html')


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'msg_erro':'Utilizador não autenticado'})

    return render(request, 'profile.html')

def addProduct(request):
    if request.user.staff:
        tamanho = request.POST['tamanho']
        cor = request.POST['cor']
        preco = request.POST['preco']
        num_pontos = request.POST['num_pontos']
        categoria = request.POST['categoria']
        referencia = request.POST['referencia']
        Produto.makeProduct(tamanho, cor, preco, num_pontos, categoria)
    else:
        return redirect('login_view')

def redirectAddProduct(request):
    return render(request, 'addProduct.html')


def sweatshirts_view(request):
    product_list = Produto.objects.filter(categoria='Sweatshirt').order_by('cor')
    arr_produto_unico = []
    cores_vistas = set()
    for product in product_list:
        if product.cor not in cores_vistas:
            cores_vistas.add(product.cor)
            arr_produto_unico.append(product)
    context = {'product_list': arr_produto_unico}
    return render(request, 'sweatshirts.html', context)


def tshirts_view(request):
    product_list = Produto.objects.filter(categoria='T-Shirt').order_by('cor')
    arr_produto_unico = []
    cores_vistas = set()
    for product in product_list:
        if product.cor not in cores_vistas:
            cores_vistas.add(product.cor)
            arr_produto_unico.append(product)
    context = {'product_list': arr_produto_unico}
    return render(request, 'sweatshirts.html', context)



