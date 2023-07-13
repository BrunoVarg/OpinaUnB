from django import forms
from .cruds.filter import get_all_departamentos, get_all_disciplinas, get_all_professores
from .cruds.avaliacao_turmas import get_periodos
from .connection import Connection
con = Connection()

class FormControlTextInput(forms.TextInput):
    def __init__(self, is_password=False, *args, **kwargs):
        if is_password:
            attrs = kwargs.setdefault('attrs', {})
            attrs['type'] = 'password'
        attrs = kwargs.setdefault('attrs', {})
        attrs['class'] = attrs.get('class', '') + ' form-control'
        super().__init__(*args, **kwargs)

class LoginForm(forms.Form):
    matricula = forms.IntegerField(label="Matrícula", widget=FormControlTextInput, required=True)
    senha = forms.CharField(label="Senha", max_length=200, widget=FormControlTextInput(is_password=True), required=True)

class RegisterForm(forms.Form):
    matricula = forms.IntegerField(label="Matrícula", widget=FormControlTextInput, required=True)
    nome = forms.CharField(label="Nome", max_length=200, widget=FormControlTextInput, required=True)
    email = forms.EmailField(label="E-mail", max_length=200, widget=FormControlTextInput, required=True)
    curso = forms.CharField(label = "Curso", max_length=200, widget=FormControlTextInput, required=True)
    senha = forms.CharField(label='Senha', widget=FormControlTextInput(is_password=True), required=True)
    confirmacao = forms.CharField(label='Confirmação de Senha', widget=FormControlTextInput(is_password=True), required=True)
    imagem = forms.ImageField(label="Imagem", required=False)


class FilterAvaliacao(forms.Form):
    options1 = [(x, y) for x, y in get_all_departamentos(con)]
    options1.insert(0, (None, "--------------"))
    departamento = forms.ChoiceField(label="Departamento", choices=options1, widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    options1 = [(x[0], x[1]) for x in get_all_disciplinas(con)]
    options1.insert(0, (None, "--------------"))
    disciplina = forms.ChoiceField(label="Disciplina", choices=options1, widget=forms.Select(attrs={'class': 'form-select form-select-lg'}), required=False)

    options1 = [(x[0], x[1]) for x in get_all_professores(con)]
    options1.insert(0, (None, "--------------"))
    professor = forms.ChoiceField(label="Professores", choices=options1, widget=forms.Select(attrs={'class': 'form-select form-select-lg'}), required=False)

class FilterTurma(forms.Form):
    def __init__(self, disciplina, professor, *args, **kwargs):
        super(FilterTurma, self).__init__(*args, **kwargs)
        self.disciplina = disciplina
        self.professor = professor
        self.fields['periodo'] = forms.ChoiceField(label="Periodo", choices=self.get_periodos(), widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))
        self.fields['turma'] = forms.ChoiceField(label="Turma", choices=[(None, "---")], widget=forms.Select(attrs={'class': 'form-select form-select-lg'}), required=False)

    def get_periodos(self):
        # Use self.disciplina e self.professor para obter os periodos desejados
        periodos = [(x[0], x[0]) for x in get_periodos(con, self.disciplina, self.professor)]
        periodos = list(set(periodos))
        periodos.insert(0, (None, "-----"))
        return periodos
        
    