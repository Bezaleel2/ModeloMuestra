from django import forms
from .models import Obra

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nombre_obra', 'encargado_obra', 'fecha_estimada_entrega', 'ubicacion']
        # Si quieres añadir todos los campos del modelo sin listarlos:
        # fields = '__all__'

        widgets = {
            'nombre_obra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Edificio Central'}),
            'encargado_obra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ing. Juan Pérez'}),
            'fecha_estimada_entrega': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' # Esto ayuda a que el navegador muestre un selector de fecha
                }
            ),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Av. Siempre Viva 123'}),
            # Si tuvieras un campo descripción (TextField):
            # 'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'nombre_obra': 'Nombre de la Obra',
            'encargado_obra': 'Responsable de la Obra',
            'fecha_estimada_entrega': 'Entrega Estimada Para',
            'ubicacion': 'Dirección o Ubicación del Proyecto',
        }