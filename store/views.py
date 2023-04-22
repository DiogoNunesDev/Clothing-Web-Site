from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from store.models import Produto
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
            print("existe")
            # reverse: quando estou dentro dos templates vai procurar o index e vai gerar o url correspondente
            return HttpResponseRedirect(reverse('home'))
        else:
            print("Nao existe")
            return render(request, 'login.html', {'msg_erro':'Credenciais inválidas, tente novamente.'})
    else:
        #Mostrar o formulario de login
        return render(request, 'login.html')


def redirectLogin(request):
    return render(request, 'login.html')

def signup_view(request):
    name = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=name, password=password)
    print("ok")

def redirectSignup(request):
    return render(request, 'signup.html')

def addProduct(request):
    if request.user.staff:
        print("ok")
    else:
        return redirect('login_view')

def sweatshirts_view(request):
    return render(request, 'sweatshirts.html')