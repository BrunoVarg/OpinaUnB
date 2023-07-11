from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .forms import LoginForm, RegisterForm
from .cruds.usuario import check_login, get_matricula, get_image, edit_user, delete_user, User
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

    if request.session.get('user_id'):
        vals = get_matricula(con, pk)
        img = get_image(con, pk)
        user = User(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], img)
        context= {}
        context["user"] = user
        return render(request, "minhaconta.html", context)
    else:
        return redirect('login')

def register(request):
    if request.method == "GET":
        form = RegisterForm()
    
    else:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            matricula = request.POST["matricula"]
            nome = request.POST["nome"]
            email = request.POST["email"]
            curso = request.POST["curso"]
            senha = request.POST["senha"]
            confirmacao = request.POST["confirmacao"]
            imagem = request.FILES["imagem"].read()

            if confirmacao != senha:
                messages.error(request, "Confirmação de Senha incorreta")
            else:
                create_user(con, matricula, False, nome, email, curso, senha, imagem)
                messages.success(request, "Conta criada com sucesso.")
                return redirect('index')

    return render(request, "register.html", {"forms":form})

def editar(request, pk):
    if request.session.get("user_id"):
            return redirect('index')

    if request.method == "GET":
        vals = get_matricula(con, pk)
        form = RegisterForm()
        matricula = vals[0]
        form.initial['matricula'] = vals[0]
        form.initial['nome'] = vals[2]
        form.initial['email'] = vals[3]
        form.initial['curso'] = vals[4]
        form.initial['senha'] = vals[5]
        imagem = get_image(con, pk)
    else:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            matricula = request.POST["matricula"]
            nome = request.POST["nome"]
            email = request.POST["email"]
            curso = request.POST["curso"]
            senha = request.POST["senha"]
            confirmacao = request.POST["confirmacao"]
            imagem = None

            if request.FILES.get("imagem"):
                if request.FILES["imagem"]:
                    imagem = request.FILES["imagem"].read()
            print(imagem)
            if confirmacao != senha:
                messages.error(request, "Confirmação de Senha incorreta")
            else:
                print(matricula, nome, email, curso, senha, imagem)
                edit_user(con, matricula, False, nome, email, curso, senha, imagem)
                messages.success(request, "Conta editada com sucesso.")
                return redirect(reverse('minha_conta', args=[matricula]))
    return render(request, "editar.html", {"forms":form, "matricula":matricula, "imagem":imagem})

def delete(request, pk):
    if request.session.get("user_id"):
        return redirect('index')
    delete_user(con, pk)
    messages.success(request, "Conta deletada com sucesso.")
    if request.session.get("pk"):
        del request.session["pk"]
    return redirect('index')