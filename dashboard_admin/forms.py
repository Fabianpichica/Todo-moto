# dashboard_admin/forms.py
from django import forms
from .models import Categoria # Importamos el modelo Categoria
from productos.models import Producto # Importamos el modelo Producto si es necesario

class CategoriaForm(forms.ModelForm):
        """
        Formulario para crear y editar objetos Categoria.
        Basado en ModelForm para facilitar la interacción con el modelo.
        """
        class Meta:
            model = Categoria
            fields = ['nombre', 'descripcion'] # Campos del modelo que queremos en el formulario
            widgets = {
                'nombre': forms.TextInput(attrs={
                    'class': 'form-control-custom', # Usamos tu clase CSS personalizada
                    'placeholder': 'Nombre de la categoría'
                }),
                'descripcion': forms.Textarea(attrs={
                    'class': 'form-control-custom', # Usamos tu clase CSS personalizada
                    'rows': 4,
                    'placeholder': 'Descripción de la categoría (opcional)'
                }),
            }
            labels = {
                'nombre': 'Nombre de la Categoría',
                'descripcion': 'Descripción',
            }

        def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            import re
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
                raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
            return nombre


class ProductoForm(forms.ModelForm):
        """
        Formulario para crear y editar objetos Producto.
        """
        class Meta:
            model = Producto
            # Asegúrate de que estos campos coincidan con tu modelo Producto en productos/models.py
            fields = ['nombre', 'descripcion', 'precio', 'imagen', 'stock', 'disponible', 'categoria']
            widgets = {
                'nombre': forms.TextInput(attrs={
                    'class': 'form-control-custom',
                    'placeholder': 'Nombre del producto'
                }),
                'descripcion': forms.Textarea(attrs={
                    'class': 'form-control-custom',
                    'rows': 4,
                    'placeholder': 'Descripción detallada del producto'
                }),
                'precio': forms.NumberInput(attrs={
                    'class': 'form-control-custom',
                    'placeholder': 'Ej: 99.99',
                    'step': '0.01' # Para permitir decimales
                }),
                'stock': forms.NumberInput(attrs={
                    'class': 'form-control-custom',
                    'placeholder': 'Cantidad en stock'
                }),
                'disponible': forms.CheckboxInput(attrs={
                    'class': 'form-check-input-custom'
                }),
                'categoria': forms.Select(attrs={
                    'class': 'form-control-custom'
                }),
                # 'imagen' no necesita un widget especial si es ImageField, Django lo maneja por defecto para file input
            }
            labels = {
                'nombre': 'Nombre del Producto',
                'descripcion': 'Descripción',
                'precio': 'Precio',
                'imagen': 'Imagen del Producto',
                'stock': 'Stock',
                'disponible': 'Disponible para Venta',
                'categoria': 'Categoría',
            }

        def clean_precio(self):
            precio = self.cleaned_data.get('precio')
            if precio is not None:
                if precio < 0:
                    raise forms.ValidationError('El precio no puede ser negativo.')
                if precio == 0:
                    raise forms.ValidationError('El precio no puede ser cero.')
            return precio

        def clean_stock(self):
            stock = self.cleaned_data.get('stock')
            if stock is not None and stock < 0:
                raise forms.ValidationError('El stock no puede ser negativo.')
            return stock

        def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            import re
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
                raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
            return nombre

        def clean_imagen(self):
            imagen = self.cleaned_data.get('imagen')
            if imagen:
                from django.core.exceptions import ValidationError
                import imghdr
                # Validar extensión y tipo de archivo
                valid_mimetypes = ['jpeg', 'png', 'gif', 'bmp', 'webp']
                tipo = imghdr.what(imagen)
                if tipo not in valid_mimetypes:
                    raise ValidationError('Solo se permiten archivos de imagen (jpeg, png, gif, bmp, webp).')
                # Validar tamaño (ahora: 5MB máximo)
                if imagen.size > 5*1024*1024:
                    raise ValidationError('La imagen no puede superar los 5MB.')
            return imagen

