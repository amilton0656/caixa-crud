from django import forms

from .models import CentroCusto


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descricao'}),
        }
