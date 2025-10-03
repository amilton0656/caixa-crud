from django import forms

from .models import Movimento


class MovimentoForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d',
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Movimento
        fields = ['obra', 'centro_custos', 'data', 'sinal', 'valor', 'historico']
        widgets = {
            'obra': forms.Select(attrs={'class': 'form-select'}),
            'centro_custos': forms.Select(attrs={'class': 'form-select'}),
            'sinal': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'historico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o movimento'}),
        }
