from django import forms
from .models import Reporte, Imagen, Comentario

class ReporteForm(forms.ModelForm):
    class Meta:
        model   = Reporte
        fields  = ['titulo', 'descripcion', 'categoria', 'latitud', 'longitud']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Hueco en la calle 5 con carrera 8'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el problema con detalle...'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'latitud':  forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }

class ImagenForm(forms.ModelForm):
    class Meta:
        model  = Imagen
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe un comentario...'
            })
        }