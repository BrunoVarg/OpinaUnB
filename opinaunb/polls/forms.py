from django import forms

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

