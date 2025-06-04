from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=150, required=False, label="Apellidos")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono")
    # email = forms.EmailField(label="Correo Electrónico")

    ROLE_CHOICES = [
        ('permiso_total', 'Permiso total al sistema'),
        ('administrativo', 'Administrativo'),
        ('operativo', 'Operativo'),
        ('jefe_de_piso', 'Jefe de piso'), # Nueva opción
        ('admin_secundario', 'Administrador secundario'), # Nueva opción
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        required=True, 
        label="Rol del Usuario",
        widget=forms.RadioSelect
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('nombre', 'apellidos', 'telefono', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        selected_role = self.cleaned_data.get('role')

        # Resetear flags por si acaso, excepto para superuser
        user.is_staff = False
        user.is_superuser = False

        if selected_role == 'permiso_total':
            user.is_superuser = True
            user.is_staff = True 
        elif selected_role == 'administrativo':
            user.is_staff = True 
        elif selected_role == 'operativo':
            user.is_staff = True 
        elif selected_role == 'jefe_de_piso': # Nuevo rol
            user.is_staff = True
        elif selected_role == 'admin_secundario': # Nuevo rol
            user.is_staff = True
        
        if commit:
            user.save() # Guardar el usuario primero con sus flags
            
            # Limpiar grupos previos por si se está reasignando un rol (más relevante en un UserChangeForm)
            # Para UserCreationForm, esto asegura que solo se asignen los grupos correctos desde el inicio.
            user.groups.clear() 
            
            # Asignar a grupos
            if selected_role == 'administrativo':
                group, _ = Group.objects.get_or_create(name='Administrativo')
                user.groups.add(group)
            elif selected_role == 'operativo':
                group, _ = Group.objects.get_or_create(name='Operativo')
                user.groups.add(group)
            elif selected_role == 'jefe_de_piso':
                group, _ = Group.objects.get_or_create(name='Jefe de piso')
                user.groups.add(group)
            elif selected_role == 'admin_secundario':
                group, _ = Group.objects.get_or_create(name='Administrador secundario')
                user.groups.add(group)
        return user