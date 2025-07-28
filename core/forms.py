

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             help_text='Ingresa una dirección de correo válida.') # <-- Puedes traducir o dejarlo vacío
    first_name = forms.CharField(max_length=30, required=False, label='Nombre',
                                 help_text='') # <-- Quitar help_text
    last_name = forms.CharField(max_length=150, required=False, label='Apellido',
                                help_text='') # <-- Quitar help_text

    telefono = forms.CharField(max_length=20, required=False, label='Teléfono',
                               help_text='') # <-- Quitar help_text
    direccion = forms.CharField(max_length=255, required=False, label='Dirección',
                                help_text='') # <-- Quitar help_text
    ciudad = forms.CharField(max_length=100, required=False, label='Ciudad',
                             help_text='') # <-- Quitar help_text

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') + UserCreationForm.Meta.fields[2:]

        # Opcional: Para el username y password, que son campos del UserCreationForm.Meta
        # Aquí puedes establecer help_texts específicos o anularlos por completo
        help_texts = {
            'username': '', # Esto anula el help_text predeterminado del username
            'password': '', # Esto anula el help_text predeterminado de la contraseña
            'password2': '', # Esto anula el help_text predeterminado de la confirmación de contraseña
        }
        # Si quieres traducir los labels o dejarlos con los que ya pusiste
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
            'password2': 'Confirmar Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }


    # ¡ESTE ES EL MÉTODO SAVE MODIFICADO!
    def save(self, commit=True):
        user = super().save(commit=False) # Guarda el usuario pero no lo comitea a la DB aún
        user.email = self.cleaned_data['email'] # Asigna el email
        user.first_name = self.cleaned_data.get('first_name') # Asigna nombre
        user.last_name = self.cleaned_data.get('last_name') # Asigna apellido

        if commit:
            user.save() # Guarda el usuario en la DB. Esto dispara la señal para crear UserProfile.

            # Ahora, en lugar de CREAR un UserProfile, lo OBTENEMOS y ACTUALIZAMOS.
            # La señal ya se encargó de crearlo.
            user_profile = user.userprofile # Accede al perfil que ya fue creado por la señal
            user_profile.telefono = self.cleaned_data.get('telefono')
            user_profile.direccion = self.cleaned_data.get('direccion')
            user_profile.ciudad = self.cleaned_data.get('ciudad')
            user_profile.save() # Guarda los cambios en el UserProfile

        return user
