from django import forms
from django.utils.safestring import mark_safe

class GraysCaleForm(forms.Form):
    img = forms.ImageField(
        label="Seleccionar imagen",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
class FilterForm(forms.Form):
    FILTER_CHOICES = [
        ('low_pass', 'Filtro Pasa Bajos'),
        ('high_pass', 'Filtro Pasa Altos'), 
        ('band_pass', 'Filtro Pasa Bandas'),
    ]
    
    img = forms.ImageField(
        required=False,
        label="Seleccionar imagen",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    filter_type = forms.ChoiceField(
        label="Tipo de filtro",
        choices=FILTER_CHOICES,
        widget=forms.RadioSelect,
        initial='low_pass'
    )
    cutoff = forms.IntegerField(
        label="Cutoff",
        min_value=1,
        max_value=1000,
        initial=50,
        widget=forms.NumberInput(attrs={
            'class': 'cutoff-slider',
            'type': 'range',
            'min': '1',
            'max': '200',
            'value': '30',
        })
    )
    cutoff2 = forms.IntegerField(
        label="Cutoff Externo",
        min_value=1,
        max_value=1000,
        initial=70,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'cutoff-slider',
            'type': 'range',
            'min': '1',
            'max': '200',
            'value': '60',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que las labels sean seguras para HTML
        self.fields['cutoff'].label = mark_safe("Cutoff: <span id='cutoffValue' class='cutoff-value'>50</span>")
        self.fields['cutoff2'].label = mark_safe("Cutoff Externo: <span id='cutoff2Value' class='cutoff-value'>70</span>")
    
class CompressionForm(forms.Form):
    img = forms.ImageField(
        label="Seleccionar imagen",
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        required=False
    )
    
    compression_percentage = forms.IntegerField(
        label="Porcentaje de compresión",
        min_value=1,
        max_value=95,
        initial=50,
        widget=forms.NumberInput(attrs={
            'class': 'compression-slider',
            'type': 'range',
            'min': '1',
            'max': '95',
            'value': '50',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que la label sea segura para HTML
        self.fields['compression_percentage'].label = mark_safe(
            "Porcentaje de compresión: <span id='compressionValue' class='compression-value'>50</span>%"
        )