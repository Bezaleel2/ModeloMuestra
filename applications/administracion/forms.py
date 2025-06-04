# applications/administracion/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, PedidoItem
from applications.almacen.models import Producto # Para el ModelChoiceField

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_creador'] # Solo el campo editable del pedido
        widgets = {
            'nombre_creador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre o departamento'}),
        }
        labels = {
            'nombre_creador': 'Pedido creado por:',
        }

class PedidoItemForm(forms.ModelForm):
    # Sobrescribimos el campo 'producto' para controlar mejor el widget y el queryset
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all().order_by('nombre_producto'),
        widget=forms.Select(attrs={'class': 'form-control-select product-selector'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control quantity-input', 'placeholder': 'Cant.'})
    )

    class Meta:
        model = PedidoItem
        fields = ['producto', 'cantidad']
        # No necesitamos labels aquí si el layout los maneja o son implícitos

# Formset para manejar múltiples PedidoItem asociados a un Pedido
# El 'extra=1' significa que por defecto se mostrará un formulario vacío para añadir un ítem.
# Puedes poner 'extra=3' si quieres 3 líneas vacías por defecto.
PedidoItemFormSet = inlineformset_factory(
    Pedido,         # Modelo padre
    PedidoItem,     # Modelo hijo (inline)
    form=PedidoItemForm, # Formulario a usar para cada ítem
    fields=['producto', 'cantidad'],
    extra=1,        # Número de formularios extra vacíos
    can_delete=True # Permite marcar ítems para ser eliminados (útil en edición)
)