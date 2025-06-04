from django import forms
from django.forms import inlineformset_factory
from applications.administracion.models import Pedido, PedidoItem # Importamos modelos de administracion

class SurtirItemForm(forms.ModelForm):
    # Este campo es para ingresar la cantidad que se va a surtir EN ESTA OPERACIÓN
    cantidad_a_surtir_ahora = forms.IntegerField(
        label="Cantidad a Surtir Ahora",
        min_value=0, # Puede ser 0 si no se surte nada de este ítem en esta operación
        required=False, # Hacemos que no sea estrictamente requerido a nivel de form field
                        # La lógica de la vista manejará si se procesa o no.
        widget=forms.NumberInput(attrs={'class': 'form-control quantity-to-fulfill', 'placeholder': '0'})
    )

    class Meta:
        model = PedidoItem
        fields = ['cantidad_a_surtir_ahora'] # Solo este campo es editable por el usuario en este form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el campo 'cantidad_a_surtir_ahora' sugiera la cantidad pendiente
        if self.instance and self.instance.pk:
            pendiente = self.instance.cantidad_pedida - self.instance.cantidad_surtida
            self.fields['cantidad_a_surtir_ahora'].widget.attrs['max'] = pendiente
            self.fields['cantidad_a_surtir_ahora'].initial = pendiente # Sugerir surtir todo lo pendiente
            # Si no quieres valor inicial, comenta la línea de arriba.
        else: # Si es un formset extra (no debería pasar si extra=0 y tenemos instancia)
            self.fields['cantidad_a_surtir_ahora'].widget.attrs['max'] = 0


    def clean_cantidad_a_surtir_ahora(self):
        cantidad_a_surtir = self.cleaned_data.get('cantidad_a_surtir_ahora')
        if cantidad_a_surtir is None: # Si es False y no 0, Python lo trata como None
            cantidad_a_surtir = 0
            
        if cantidad_a_surtir < 0:
            raise forms.ValidationError("La cantidad a surtir no puede ser negativa.")

        # Validamos contra la cantidad pendiente del ítem de la instancia
        if self.instance and self.instance.pk:
            cantidad_pedida = self.instance.cantidad_pedida
            cantidad_ya_surtida = self.instance.cantidad_surtida
            cantidad_pendiente = cantidad_pedida - cantidad_ya_surtida
            
            if cantidad_a_surtir > cantidad_pendiente:
                raise forms.ValidationError(
                    f"No puedes surtir más de la cantidad pendiente ({cantidad_pendiente})."
                )
        # La validación contra el stock del almacén se hará en la vista.
        return cantidad_a_surtir


# Formset para manejar los ítems a surtir de un Pedido específico
SurtirItemFormSet = inlineformset_factory(
    Pedido,              # Modelo padre
    PedidoItem,          # Modelo hijo (los ítems del pedido)
    form=SurtirItemForm, # El formulario que acabamos de definir para cada ítem
    extra=0,             # No mostrar formularios extra vacíos, solo los ítems existentes del pedido
    can_delete=False     # No permitimos eliminar ítems desde esta pantalla de surtido
)