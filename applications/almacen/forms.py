from django import forms
from .models import Producto
from applications.proveedores.models import Proveedor

class ProductoForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all().order_by('nombre'),
        required=False, # Hazlo no requerido si en el modelo es blank=True, null=True
        label="Proveedor",
        widget=forms.Select(attrs={'class': 'form-control-select'})
    )
    cantidad_a_agregar = forms.IntegerField(
        label="Cantidad a Agregar al Stock",
        required=False,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10'})
    )

    class Meta:
        model = Producto
        fields = [
            'numero_orden_compra',
            'proveedor',
            'nombre_producto',
            'cantidad', # Esta es la cantidad TOTAL actual
        ]
        widgets = {
            'numero_orden_compra': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }
        labels = {
            'numero_orden_compra': "No. Orden de Compra (para esta transacción)",
            'nombre_producto': "Nombre del Producto",
            'cantidad': "Cantidad Total Actual en Stock",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: # Editando una instancia existente
            self.fields['cantidad'].widget.attrs['readonly'] = True
        else: # Creando una nueva instancia
            # Si el campo 'cantidad_a_agregar' se definió en la clase del formulario directamente (como ahora),
            # y no en Meta.fields, entonces existe en self.fields.
            if 'cantidad_a_agregar' in self.fields:
                 del self.fields['cantidad_a_agregar']
            if 'readonly' in self.fields['cantidad'].widget.attrs:
                del self.fields['cantidad'].widget.attrs['readonly']

    def clean_nombre_producto(self):
        nombre = self.cleaned_data.get('nombre_producto')
        
        # Si estamos editando (self.instance.pk existe) y el nombre no ha cambiado
        # (o solo cambió el case, y usamos iexact para la comparación), es válido.
        if self.instance and self.instance.pk:
            if self.instance.nombre_producto.lower() == nombre.lower(): # Comparamos en minúsculas
                return nombre # El nombre es el mismo (o solo cambió el case), lo permitimos para la instancia actual.

        # Si es una nueva instancia O el nombre ha cambiado en una instancia existente:
        # Verificamos si ya existe otro producto con este nombre (insensible a mayúsculas/minúsculas).
        # Si estamos editando, excluimos la instancia actual de esta búsqueda.
        query = Producto.objects.filter(nombre_producto__iexact=nombre)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        
        if query.exists():
            raise forms.ValidationError(
                "Ya existe un Producto de Almacén con este Nombre del Producto.",
                code='unique'
            )
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance or not self.instance.pk: # Es un formulario de creación
            cantidad_inicial = cleaned_data.get('cantidad')
            if cantidad_inicial is not None and cantidad_inicial < 0:
                self.add_error('cantidad', 'La cantidad inicial debe ser un número positivo o cero.')
        
        if 'cantidad_a_agregar' in cleaned_data: # Solo si el campo está presente
            cantidad_agregada = cleaned_data.get('cantidad_a_agregar')
            if cantidad_agregada is not None and cantidad_agregada < 0:
                self.add_error('cantidad_a_agregar', 'La cantidad a agregar no puede ser negativa.')
                
        return cleaned_data