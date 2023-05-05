from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from store.models import Produto, Utilizador, Staff, Comentario, carrinhoItem, CarrinhoCompras, Historico
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')

def full_collection(request):
    unique_pairs = Produto.objects.values('referencia', 'cor').distinct().order_by('referencia', 'cor')
    product_list = []
    for pair in unique_pairs:
        product = Produto.objects.filter(cor=pair['cor'], referencia=pair['referencia'])
        product_list.append(product[0])

    # Produtos por página
    products_per_page = 4

    # Cria o objeto do tipo paginator
    paginator = Paginator(product_list, products_per_page)
    page_number = request.GET.get('page')

    # agrupa os produtos da página atual
    page_obj = paginator.get_page(page_number)

    context = {
        'product_list': page_obj,
    }
    return render(request, 'full_collection.html', context)

@login_required(login_url="login_view")
def cart_view(request):
    if hasattr(request.user, 'utilizador'):
        try:
            carrinho = CarrinhoCompras.objects.get(utilizador= request.user.utilizador)
            cart_items = carrinhoItem.objects.filter(carrinho=carrinho)
            produtos = []
            for item in cart_items:
                produto = Produto.objects.get(pk=item.produto.id)
                produtos.append(produto)
            context = {'items': list(cart_items.values()), 'produtos': list(produtos), 'carrinho': carrinho}
            print(list(cart_items.values()))
            return render(request, 'cart.html', context)
        except ObjectDoesNotExist:
            return render(request, 'cart.html', {'empty': 'O seu carrinho está vazio'})
    else:
        return render(request, 'login.html', {'msg': 'Não está logado como User'})

@login_required(login_url="login_view")
def addToCart(request):
    if hasattr(request.user,'utilizador'):
        if request.method == 'POST':
            tamanho = request.POST.get('tamanho', '')
            cor = request.POST.get('cor', '')
            categoria = request.POST.get('categoria', '')
            referencia = request.POST.get('referencia', '')
            produto_id = request.POST.get('produto_id', 0)

            try:
                produto = Produto.objects.filter(cor=cor, referencia=referencia, tamanho=tamanho, categoria=categoria).first()
                if not produto:
                    raise ValueError("Produto não existe")


                if produto.stock == 0:
                    messages.error(request, 'O Produto escolhido não se encontra em Stock!')
                    return redirect('detail', produto_id=produto_id)

                carrinho, created = CarrinhoCompras.objects.get_or_create(utilizador=request.user.utilizador,
                                                                          defaults={'num_itens': 0, 'valor_total': 0})

                item_do_carrinho, item_criado = carrinhoItem.objects.get_or_create(produto=produto, carrinho=carrinho)

                if not item_criado:
                    item_do_carrinho.quantidade += 1
                    item_do_carrinho.save()

                carrinho.num_itens += 1
                carrinho.valor_total += produto.preco
                carrinho.save()
                produto.stock -= 1
                produto.save()

            except ValueError:
                messages.error(request, 'O Produto escolhido não se encontra em Stock!')
                return redirect('detail', produto_id=produto_id)

            messages.success(request, 'Produto adicionado ao carrinho')
            return redirect('detail', produto_id=produto_id)
    else:
        return render(request, 'login.html', {'msg': 'Não está logado!'})


@login_required(login_url="login_view")
def finalizar_compra(request):
    if hasattr(request.user, 'utilizador'):
        if request.method == 'POST':
            try:
                utilizador = request.user.utilizador
                carrinho = CarrinhoCompras.objects.get(utilizador=utilizador)
                items_carrinho = carrinhoItem.objects.filter(carrinho=carrinho)

                #passar compra para o histórico
                for item in items_carrinho:
                    historico = Historico(utilizador=utilizador, produto= item.produto, quantidade=item.quantidade)
                    historico.save()
                    item.delete()

                carrinho.delete()

                #associar um novo carrinho ao user estando totalmente a zeros
                new_carrinho = CarrinhoCompras.objects.create(utilizador=utilizador, num_itens=0, valor_total=0)
                new_carrinho.save()

                return redirect('cart_view')
            except CarrinhoCompras.DoesNotExist:
                pass
    else:
        return render(request, 'login.html', {'msg': 'Não está logado'})

"""
            utilizador = Utilizador.objects.get(user=request.user)
            carrinho = CarrinhoCompras.objects.get(utilizador=utilizador)

            itens = carrinhoItem.objects.filter(carrinho=carrinho)

            historico_carrinho = HistoricoCarrinho(utilizador=request.user.utilizador, carrinho=carrinho)
            historico_carrinho.save()

            pontos = 0

            for item in itens:
                produto = item.produto
                quantidade_no_carrinho = item.quantidade
                produto.stock -= quantidade_no_carrinho
                pontos += produto.num_pontos
                produto.save()

                categoria_contagem[produto.categoria] += quantidade_no_carrinho
                valor_total += produto.preco * quantidade_no_carrinho

            utilizador.num_pontos += pontos
            utilizador.save()

            nova_compra = Compra.objects.create(
                utilizador=utilizador,
                data_compra=timezone.now(),
                valor_total=valor_total,
            )

            for item in itens:
                nova_compra.itens_comprados.add(item)


            return redirect('home.html')
    else:
        return render(request, 'login.html')
"""

def clear_cart(request):
    if request.user.is_authenticated and hasattr(request.user,'utilizador'):
        try:
            CarrinhoCompras.objects.filter(utilizador=request.user.utilizador).delete()
        except CarrinhoCompras.DoesNotExist:
            pass
    else:
        return render(request, 'login.html', {'msg': 'Não está logado'})
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
            return render(request, 'login.html', {'msg':'Credenciais inválidas, tente novamente.'})
    else:
        #Mostrar o formulario de login
        return render(request, 'login.html')


def redirectLogin(request):
    return render(request, 'login.html')

def logout_view(request):
    clear_cart(request)
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        primeiro_nome = request.POST.get('primeiro_nome', '')
        apelido = request.POST.get('apelido', '')
        data_nascimento = request.POST.get('data_nascimento', '')
        morada = request.POST.get('morada', '')
        numero_telemovel = request.POST.get('numero_telemovel', 0)
        num_cartao_cidadao = request.POST.get('num_cartao_cidadao', 0)
        nif = request.POST.get('nif', 0)
        user = User(username=name, password=password, email=email)
        user.save()
        utilizador = Utilizador(user=user, primeiro_nome=primeiro_nome, apelido=apelido, data_nascimento=data_nascimento,
                                morada=morada, numero_telemovel=numero_telemovel, num_cartao_cidadao=num_cartao_cidadao,
                                nif=nif, num_pontos=0, email=email)
        utilizador.save()
        login(request, user)
        return redirect('home', {'msg', 'Bem vindo à Pescada Store!'})
    else:
        return render(request, 'signup.html')


def redirectSignup(request):
    if not request.user.is_authenticated:
        return render(request, 'signup.html')
    else:
        return render(request, 'home.html')

@permission_required('store.delete_staff', login_url='login_view')
def redirectDeleteStaff(request):
    staff_list = Staff.objects.all()
    context = {'staff_list': staff_list}
    return render(request, 'removeStaff.html', context)


@permission_required('store.delete_staff', login_url='login_view')
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, user_id=staff_id)
    staff.user.delete()
    messages.success(request, 'Colaborador removido com sucesso.')
    return render(request, 'removeStaff.html', )


@permission_required('store.addStaff', login_url='login_view')
def addStaff(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('username', '')
            password = request.POST.get('password','')
            email = request.POST.get('email','')
            user = User.objects.create_user(username=name, password=password, email=email)
            user.save()
            primeiro_nome = request.POST.get('primeiro_nome','')
            apelido = request.POST.get('apelido','')
            data_nascimento = request.POST.get('data_nascimento','')
            morada = request.POST.get('morada','')
            numero_telemovel = request.POST.get('numero_telemovel',0)
            num_cartao_cidadao = request.POST.get('num_cartao_cidadao',0)
            staff = Staff(user=user, primeiro_nome=primeiro_nome, apelido=apelido, data_nascimento=data_nascimento, morada=morada,
                            numero_telemovel=numero_telemovel, num_cartao_cidadao=num_cartao_cidadao, email=email)
            staff.save()
            return render(request, 'addStaff.html', {'msg': 'Staff Adicionado'})
    return render(request, 'addStaff.html', {'msg': 'Não está logado como Super User!'})

@permission_required('store.redirectAddStaff', login_url='login_view')
def redirectAddStaff(request):
    return render(request, 'addStaff.html')

@login_required(login_url="login_view")
def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'msg_erro':'Utilizador não autenticado'})
    else:
        if hasattr(request.user,'utilizador'):
            border_color = get_border_color(request.user.utilizador.num_pontos)
            return render(request, 'profile.html', {'border_color': border_color})
        else:
            return render(request, 'profile.html')

def get_border_color(num_pontos):
    if num_pontos <= 500:
        return '#cd7f32'
    elif num_pontos <= 1000:
        return '#c0c0c0'
    elif num_pontos <= 1500:
        return '#ffd700'
    elif num_pontos <= 2500:
        return '#50c878'
    else:
        return '#e0115f'

@login_required(login_url="login_view")
def removeProduct(request):
    if request.user.is_authenticated and hasattr(request.user, 'staff'):
        if request.method == 'POST':
            produto_id = request.POST.get('produto_id')
            produto = get_object_or_404(Produto, pk=produto_id)
            produto.delete()
            messages.success(request, 'Produto removido com sucesso.')
            return redirect('removeProduto')
        else:
            products = Produto.objects.all()
            return render(request, 'removeProduct.html', {'produtos': products})
    else:
        return redirect('login_view')

@login_required(login_url="login_view")
def redirectRemoveProduct(request):
    if hasattr(request.user, 'staff'):
        products = Produto.objects.all()
        return render(request, 'removeProduct.html', {'products': products})
    else:
        return render(request, 'login.html', {'msg': 'Apenas Staff'})


@login_required(login_url="login_view")
def addProduct(request):
    if request.user.is_authenticated and hasattr(request.user,'staff'):
        if request.method == 'POST':
            tamanho = request.POST.get('tamanho', '')
            cor = request.POST.get('cor', '')
            preco = request.POST.get('preco', 0)
            categoria = request.POST.get('categoria', '')
            referencia = request.POST.get('referencia', '')
            image = cor + referencia + '.png'
            stock = int(request.POST.get('stock', 0))

            if categoria == 'Long Sleeve':
                num_pontos = 40
            elif categoria == 'T-Shirt':
                num_pontos = 20
            else:
                num_pontos = 50

            try:
                produto = Produto.objects.get(cor=cor, referencia=referencia, tamanho=tamanho, num_pontos=num_pontos, categoria=categoria)
                produto.stock = produto.stock + stock
                produto.save()
                return render(request, 'addProduct.html', {'msg': 'Stock atualizado !'})
            except ObjectDoesNotExist:
                Produto.makeProduct(tamanho, cor, preco, num_pontos, categoria, referencia, image, stock)
                return render(request, 'addProduct.html', {'msg': 'Produtos Inseridos!'})

    else:
        return redirect('login_view', {'msg': 'Não está logado como Staff'})

@login_required(login_url="login_view")
def redirectAddProduct(request):
    if hasattr(request.user, 'staff'):
        return render(request, 'addProduct.html')
    else:
        return render(request, 'login.html', {'msg': 'Apenas Staff'})


def sweatshirts_view(request):
    produtos = Produto.objects.filter(categoria__in=['Long Sleeve','Sweatshirt']).order_by('cor')
    produtos_unicos = {}
    for produto in produtos:
        chave = (produto.categoria, produto.cor, produto.categoria)
        if chave not in produtos_unicos:
            produtos_unicos[chave] = produto
    context = {'product_list': list(produtos_unicos.values())}
    return render(request, 'sweatshirts.html', context)


def longSleeves_view(request):
    product_list = Produto.objects.filter(categoria='Long Sleeve').order_by('cor')
    arr_produto_unico = []
    cores_vistas = set()
    for product in product_list:
        if product.cor not in cores_vistas:
            cores_vistas.add(product.cor)
            arr_produto_unico.append(product)
    context = {'product_list': arr_produto_unico}
    return render(request, 'longSleeve.html', context)

def hoodies_view(request):
    product_list = Produto.objects.filter(categoria='Sweatshirt').order_by('cor')
    arr_produto_unico = []
    cores_vistas = set()
    for product in product_list:
        if product.cor not in cores_vistas:
            cores_vistas.add(product.cor)
            arr_produto_unico.append(product)
    context = {'product_list': arr_produto_unico}
    return render(request, 'hoodies.html', context)


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

def detail_view(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    comentarios = Comentario.objects.filter(image=produto.image).order_by('-data')
    context = {'produto': produto, 'comentarios': comentarios}
    return render(request, 'detail.html', context)

@login_required(login_url="login_view")
def redirectEditProfile(request):
    return render(request, 'editProfile.html')

@login_required(login_url="login_view")
def edit_profile(request):
    if hasattr(request.user, 'utilizador'):
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
                utilizador.email = request.POST['email']

            if request.POST['numero_telemovel']:
                utilizador.numero_telemovel = request.POST['numero_telemovel']

            if request.POST['num_cartao_cidadao']:
                utilizador.num_cartao_cidadao = request.POST['num_cartao_cidadao']

            if request.POST['nif']:
                utilizador.nif = request.POST['nif']

            if request.POST['password'] & request.POST['confirm_password']:
                if request.POST['password'] == request.POST['confirm_password']:
                    user.password = request.POST['password']
                else:
                    return render(request, 'edit_profile.html', {'msg': 'Password confirmada incorretamente'})

            user.save()
            utilizador.save()

            return render(request, 'profile.html')
        else:
            return render(request, 'edit_profile.html')
    else:
        return render(request, 'login.html', {'msg': 'não está com conta de User'})

def comentarios(request):
    comentarios = Comentario.objects.all().order_by('data')
    produtos = Produto.objects.all()
    return render(request, 'comentarios.html', context = {'comentarios_list': comentarios, 'produtos': produtos})

def comment(request):
    if not hasattr(request.user, 'utilizador'):
        return redirect('login_view', {'msg': 'Não está logado como User'})
    else:
        if request.method == 'POST':
            produto_id = request.POST.get('produto_id')
            descricao = request.POST.get('comment', '')
            utilizador = request.user.utilizador
            data = timezone.now()
            image = request.POST.get('image')
            comment = Comentario(descricao=descricao, utilizador=utilizador, data=data, image=image)
            comment.save()
            return redirect('detail', produto_id=produto_id)
