from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from store.models import Produto, Utilizador, Staff
from django.urls import reverse
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'home.html')

def full_collection(request):
    products = Produto.objects.all()
    unique_pairs = Produto.objects.values('referencia', 'cor').distinct().order_by('referencia', 'cor')
    product_list = []
    for pair in unique_pairs:
        product = Produto.objects.filter(cor=pair['cor'], referencia=pair['referencia'])
        product_list.append(product[0])
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
        if request.method == 'POST':
            num_items = int(request.POST.get('num_items', 0))
            tamanho = request.POST.get('tamanho', '')
            cor = request.POST.get('cor', '')
            preco = request.POST.get('preco', 0)
            num_pontos = request.POST.get('num_pontos', 0)
            categoria = request.POST.get('categoria', '')
            referencia = request.POST.get('referencia', '')
            print(referencia)
            print(num_items)
            image = cor + referencia + '.png'

            for i in range(num_items):
                Produto.makeProduct(tamanho, cor, preco, num_pontos, categoria, referencia, image)
            return render(request, 'addProduct.html', {'msg': 'Produtos Inseridos!'})
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
    return render(request, 'tshirts.html', context)

def detail_view(request,produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    context={'produto': produto}
    return render(request,'detail.html',context)

def redirectEditProfile(request):
    return render(request, 'editProfile.html')


def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        utilizador = request.user.utilizador

        if request.POST['primeiro_nome']:
            utilizador.primeiro_nome = request.POST['primeiro_nome']

        if request.POST['apelido']:
            utilizador.apelido = request.POST['apelido']

        if request.POST['data_nascimento']:
            utilizador.data_nascimento = request.POST['data_nascimento']

        if request.POST['morada']:
            utilizador.morada = request.POST['morada']

        if request.POST['email']:
            user.email = request.POST['email']
            user.save()
            utilizador.email = request.POST['email']

        if request.POST['numero_telemovel']:
            utilizador.numero_telemovel = request.POST['numero_telemovel']

        if request.POST['num_cartao_cidadao']:
            utilizador.num_cartao_cidadao = request.POST['num_cartao_cidadao']

        if request.POST['nif']:
            utilizador.nif = request.POST['nif']

        utilizador.save()

        return render(request, 'profile.html')
    else:
        return render(request, 'edit_profile.html')
