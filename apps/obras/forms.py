from django import forms

from .models import Obra


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nome', 'endereco', 'municipio']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da obra'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Município'}),
        }
