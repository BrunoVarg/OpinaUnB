from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm, FilterAvaliacao, FilterTurma
from .cruds.denuncias import get_all_denuncias, get_denuncia_avaliacao, create_denuncia, call_denuncia
from .cruds.usuario import check_login, get_matricula, get_image, edit_user, delete_user, User, check_admin
from .cruds.avaliacao_turmas import get_all_turmas, get_professor_by_disciplina, get_name_by_cod_disciplina, get_all_turmas_prof_disc, get_all_avaliacoes, get_num_turma, get_id_turma, create_avaliacao_turmas, get_avaliacoes_turmas, update_avaliacao_turma, delete_avaliacao_turma
from .cruds.avaliacao_professor import get_all_avaliacoes_professores, create_avaliacao_professor, get_avaliacoes_professores, update_avaliacao, delete_avaliacao, get_nota
from .cruds.filter import get_disciplinas_departamento, get_all_disciplinas, get_all_professores, get_name_by_cod_dep, get_prof_filtered, get_prof_by_codigo, get_one_prof_by_codigo, get_turmas_filtered
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
            if(check_admin(con, matricula)):
                request.session["admin"] = True
            return redirect('login')
        else:
            messages.error(request, "Senha incorreta.")

    return render(request, "login.html", {"forms":form})

def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
        if request.session.get('admin'):
            del request.session["admin"]
    return redirect('index')

def minha_conta(request, pk:int):

    if request.session.get('user_id'):
        vals = get_matricula(con, pk)
        img = get_image(con, pk)
        user = User(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], img)
        context= {}
        context["user"] = user
        return render(request, "usuario_read.html", context)
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

    return render(request, "usuario_register.html", {"forms":form})

def editar(request, pk):
    if not request.session.get("user_id"):
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
    return render(request, "usuario_edit.html", {"forms":form, "matricula":matricula, "imagem":imagem})

def delete(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    
    delete_user(con, pk)
    messages.success(request, "Conta deletada com sucesso.")
    if request.session.get("pk"):
        del request.session["pk"]
    return redirect('index')

def professor(request):
    if not request.session.get("user_id"):
        return redirect('index')
    
    page = request.GET.get('page')
    resultados = []
    deps = []
    if request.method == "GET":
        form = FilterAvaliacao()

        # all professores
        profs = get_all_professores(con)

        profs = [(x[0], x[1], get_name_by_cod_dep(x[2])[0], get_nota(con, x[0])) for x in get_all_professores(con)]
        paginator = Paginator(profs, 15)
        resultados = paginator.get_page(page)
    else:
        form = FilterAvaliacao(request.POST)
        profs = get_prof_filtered(request.POST["departamento"], request.POST["disciplina"], request.POST["professor"])
        profs = [get_prof_by_codigo(x[0]) for x in profs]
        profs = [(x[0][0], x[0][1], get_name_by_cod_dep(x[0][2])[0], get_nota(con, x[0][0])) for x in profs]
        profs = list(set(profs))
        paginator = Paginator(profs, 15)
        resultados = paginator.get_page(page)

    context = {}
    context["forms_filter"] = form
    context["object"] = resultados

    return render(request, "professor.html", context)

def professor_read(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    context = {}

    my_id = request.session["user_id"]
    profs = get_all_avaliacoes_professores(con, pk)
    # id, imagem, nome_usuario, comentario, data, nota
    lista = [(x[0], get_image(con, x[3]), get_matricula(con, x[3])[2], x[1], x[7], x[6], (int(x[3]) == int(my_id))) for x in profs]

    if request.method == "POST":

        # Cria um novo comentario
        comentario , matricula, professor, nota = request.POST["message"], my_id, pk, request.POST["rating"]

        create_avaliacao_professor(con, comentario, matricula, professor, nota)
        messages.success(request, "Avaliação criada com sucesso.")

    prof = get_one_prof_by_codigo(pk)

    context["nome_prof"] = prof[1]
    context["dep"] = get_name_by_cod_dep(prof[2])[0]
    context["nota"] = get_nota(con, prof[0])
    context["users"] = lista
    context["my_image"] = get_image(con, my_id)
    context["pk"] = pk
    context["my_id"] = my_id
    return render(request, 'professor_read.html', context)

def editar_avaliacao_professor(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    
    context = {}
    my_id = request.session["user_id"]
    imagem = get_image(con, my_id)
    current = get_avaliacoes_professores(con, pk)
    comentario = current[1]
    nota = current[6]

    id_prof = current[5]

    
    context["pk"] = pk
    context["my_image"] = imagem
    context["comentario"] = comentario
    context["nota"] = nota

    if request.method == "POST":
        comentario , matricula, professor, nota = request.POST["message"], my_id, id_prof, request.POST["rating"]
        update_avaliacao(con, pk, comentario, matricula, professor, nota)
        messages.success(request, "Comentário editado com sucesso.")

        return redirect(reverse('professor_read', args=[id_prof]))

    
    # id, imagem, comentario, nota
    
    return render(request, 'avaliacao_professor_edit.html', context)

def delete_avaliacao_prof(request, pk, pk2):
    if not request.session.get("user_id"):
        return redirect('index')
    
    delete_avaliacao(con, pk)
    messages.success(request, "Comentário deletado com sucesso.")
    return redirect(reverse('professor_read', args=[pk2]))

""" Filtro -> Departamento -> Disciplina """
def turma(request):
    if not request.session.get("user_id"):
        return redirect('index')
    
    page = request.GET.get('page')
    resultados = []
    deps = []
    if request.method == "GET":
        form = FilterAvaliacao()
        # all turmas
        turmas = []
        # mostrar id_dep, dep, id_disc, disc, id_prof, prof, media
        #turmas = [(x[9], get_name_by_cod_dep(x[9])[0], x[8], get_name_by_cod_disciplina(con, x[8])[0], x[7], get_prof_by_codigo(x[7])[0][1], 0) for x in turmas]
        paginator = Paginator(turmas, 15)
        resultados = paginator.get_page(page)
    else:
        form = FilterAvaliacao(request.POST)
        turmas = get_turmas_filtered(request.POST["departamento"], request.POST["disciplina"], request.POST["professor"])
        turmas = [(x[9], get_name_by_cod_dep(x[9])[0], x[8], get_name_by_cod_disciplina(con, x[8])[0], x[7], get_prof_by_codigo(x[7])[0][1], 0) for x in turmas]
        turmas = list(set(turmas))
        paginator = Paginator(turmas, 15)
        resultados = paginator.get_page(page)

    context = {}
    context["forms_filter"] = form
    context["object"] = resultados

    return render(request, "turmas.html", context)


def filtro_disciplina(request):
    """ Filtra a partir do campo A """
    campo_a_value = request.GET.get('id_departamento')

    if campo_a_value:
        options = [(x[0], x[1]) for x in get_disciplinas_departamento(con, campo_a_value)]
    else:
        options = [(x[0], x[1]) for x in get_all_disciplinas(con)]
    
    options = list(set(options))
    options.insert(0, (None, "--------------"))

    return render(request, 'filtro_choice.html', {'options': options})

def filtro_professor(request):
    """
    Filtra a partir do B
    """
    campo_b_value = request.GET.get('id_disciplina')
    options = get_all_professores(con)
    if campo_b_value:
        options = [(x[7], get_prof_by_codigo(x[7])[0][1]) for x in get_professor_by_disciplina(con, campo_b_value)]
    options = list(set(options))
    options.insert(0, (None, "--------------"))
    return render(request, 'filtro_choice.html', {'options': options})

# pk = codigo_disc, pk1 = codigo_prof
def turma_read(request, pk, pk1):
    if not request.session.get("user_id"):
        return redirect('index')
    context = {}

    my_id = request.session["user_id"]
    turmas = get_all_turmas_prof_disc(con, pk1, pk)
    id_turmas = [x[0] for x in turmas]
    lista = []
    print(id_turmas)
    for x in id_turmas:
        av = get_all_avaliacoes(con, x)
        lista += av
    avaliacoes = lista
    # id, imagem, nome_usuario, comentario, data, nota
    lista = [(x[0], get_image(con, x[3]), get_matricula(con, x[3])[2], x[1], x[7], x[6], (int(x[3]) == int(my_id))) for x in avaliacoes]

    if request.method == "POST":
        # Cria um novo comentario
        comentario , matricula, professor, disciplina, nota = request.POST["message"], my_id, pk1, pk, request.POST["rating"]
        # acha a turma tal que periodo

        turma = get_id_turma(con, pk, pk1, request.POST["periodo"], request.POST["turma"])[0]
        create_avaliacao_turmas(con, comentario, turma, matricula, nota)
        messages.success(request, "Avaliação de turma criada com sucesso.")
        return redirect(reverse('turma_read', args=[pk, pk1]))

    prof = get_one_prof_by_codigo(pk1)
    context["nome_prof"] = prof[1]
    context["dep"] = get_name_by_cod_dep(prof[2])[0]
    context["disc"] = get_name_by_cod_disciplina(con, pk)[0]
    context["nota"] = 0
    context["users"] = lista
    context["my_image"] = get_image(con, my_id)
    context["pk"] = pk
    context["pk1"] = pk1
    context["my_id"] = my_id
    context["form_turma"] = FilterTurma(disciplina=pk, professor=pk1)
    return render(request, 'turmas_read.html', context)

def filtro_turma(request, pk, pk1):
    """ Filtra a partir do campo A """
    campo_a_value = request.GET.get('id_periodo')

    options = []
    if campo_a_value:
        options = [(x[0], x[0]) for x in get_num_turma(con, pk, pk1, campo_a_value)]
    options = list(set(options))
    options.insert(0, (None, "---"))

    return render(request, 'filtro_choice.html', {'options': options})

def turma_edit(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    
    context = {}
    my_id = request.session["user_id"]
    imagem = get_image(con, my_id)
    
    current = get_avaliacoes_turmas(con, pk)
    comentario = current[1]
    nota = current[6]
    id_turma = current[4]
    
    context["pk"] = pk
    context["my_image"] = imagem
    context["comentario"] = comentario
    context["nota"] = nota

    if request.method == "POST":
        comentario , matricula, professor, nota = request.POST["message"], my_id, id_turma, request.POST["rating"]
        update_avaliacao_turma(con, pk, comentario, matricula, professor, nota)
        messages.success(request, "Comentário editado com sucesso.")
        return render(request, 'turmas_edit.html', context)

    # id, imagem, comentario, nota
    
    return render(request, 'turmas_edit.html', context)

def turma_delete(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    
    delete_avaliacao_turma(con, pk)
    messages.success(request, "Comentário deletado com sucesso.")
    return redirect('turmas')

def denunciar(request, pk):
    if not request.session.get("user_id"):
        return redirect('index')
    
    create_denuncia(con, pk)
    messages.success(request, "Denúncia feita com sucesso.")
    return redirect('index')

def lista_denuncias(request):
    if not request.session.get("user_id"):
        return redirect('index')
    
    all_denuncias = get_all_denuncias(con)
    print(all_denuncias)
    lista = []
    for x in all_denuncias:
        print(x)
        lista_avaliacao = get_denuncia_avaliacao(con, x[1])
        comentario = lista_avaliacao[1]
        user = get_matricula(con, lista_avaliacao[3])
        imagem = get_image(con, lista_avaliacao[3])
        tupla = (x[0], x[1], comentario, user[2], imagem, lista_avaliacao[6], user[0])
        lista.append(tupla)
    
    context = {"lista":lista}
    return render(request, 'denuncias.html', context)

def pass_denuncia(request, pk, pk1, pk2):
    call_denuncia(con, 1, pk, pk1, pk2)
    return redirect('denuncias_lista')

def delete_denuncia(request, pk, pk1, pk2):
    call_denuncia(con, 2, pk, pk1, pk2)
    return redirect('denuncias_lista')

def delete_user(request, pk, pk1, pk2):
    call_denuncia(con, 3, pk, pk1, pk2)
    return redirect('denuncias_lista')