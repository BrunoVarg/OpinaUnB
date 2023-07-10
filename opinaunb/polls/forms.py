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
    matricula = forms.IntegerField(label="Matrícula", required=True, widget=FormControlTextInput)
    senha = forms.CharField(label="Senha", max_length=200, widget=FormControlTextInput(is_password=True))

class RegisterForm(forms.Form):
    matricula = forms.IntegerField(label="Matrícula", required=True, widget=FormControlTextInput)
    nome = forms.CharField(label="Nome", max_length=200, widget=FormControlTextInput)
    email = forms.EmailField(label="E-mal", max_length=200, widget=FormControlTextInput)
    curso = forms.CharField(label = "Curso", max_length=200, widget=FormControlTextInput)
    senha = forms.CharField(label='Senha', widget=FormControlTextInput(is_password=True))
    confirmacao = forms.CharField(label='Confirmação de Senha', widget=FormControlTextInput(is_password=True))

