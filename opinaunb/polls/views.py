from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .forms import LoginForm, RegisterForm
from .cruds.usuario import check_login, get_matricula, User
from .connection import Connection
from django.contrib import messages

con = Connection()

from .cruds.usuario import create_user
# Create your views here.

def index(request):
    if request.session.get("user_id"):
        # is logged
        return render(request, "index.html")
    else:
        return redirect('login')

def login(request):
    if request.method == "GET":
        form = LoginForm()

        if request.session.get("user_id"):
            return redirect('index')
    else:
        form = LoginForm()
        matricula = request.POST["matricula"]
        senha = request.POST["senha"]

        if check_login(con, matricula, senha):
            request.session["user_id"] = matricula
            return redirect('login')
        else:
            messages.error(request, "Senha incorreta.")

    return render(request, "login.html", {"forms":form})

def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect('index')

def minha_conta(request, pk:int):

    vals = get_matricula(con, pk)
    user = User(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
    atributos = vars(user)
    context= {}
    context["user"] = user
    context["atributos"] = atributos
    return render(request, "minhaconta.html", context)

def register(request):
    if request.method == "GET":
        form = RegisterForm()
    
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            matricula = request.POST["matricula"]
            nome = request.POST["nome"]
            email = request.POST["email"]
            curso = request.POST["curso"]
            senha = request.POST["senha"]
            confirmacao = request.POST["confirmacao"]

            if confirmacao != senha:
                messages.error(request, "Confirmação de Senha incorreta")
            else:
                create_user(con, matricula, False, nome, email, curso, senha)
                return redirect('index')

    return render(request, "register.html", {"forms":form})