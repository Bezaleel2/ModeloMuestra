from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'credito']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Aceros del Norte S.A.'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Calle, Número, Colonia, Ciudad, CP'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 33 1234 5678'}),
            # 'credito' usará el widget por defecto para BooleanField (checkbox), lo cual es apropiado.
            # Si quisieras un select con "Sí"/"No" explícitamente:
            # 'credito': forms.Select(choices=[(True, 'Sí'), (False, 'No')], attrs={'class': 'form-control'}),
        }

        labels = {
            'nombre': 'Nombre Completo o Razón Social',
            'direccion': 'Dirección Fiscal o de Contacto',
            'telefono': 'Número de Teléfono',
            'credito': '¿Se le otorga crédito a este proveedor?',
        }