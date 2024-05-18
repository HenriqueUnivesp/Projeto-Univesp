from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['register_prefeitura', 'coluna_1234']
        widgets = {
            'coluna_1234': forms.PasswordInput(),
        }

        