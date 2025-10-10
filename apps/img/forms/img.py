from django import forms

class ImgForm(forms.Form):
    img = forms.ImageField(
        label="Seleccionar imagen",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )