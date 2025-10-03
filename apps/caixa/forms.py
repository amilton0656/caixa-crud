from django import forms

from .models import Movimento


class MovimentoForm(forms.ModelForm):
    class Meta:
        model = Movimento
        fields = ['obra', 'centro_custos', 'data', 'sinal', 'historico']
        widgets = {
            'obra': forms.Select(attrs={'class': 'form-select'}),
            'centro_custos': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sinal': forms.Select(attrs={'class': 'form-select'}),
            'historico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o movimento'}),
        }
