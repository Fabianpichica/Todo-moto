from django import forms
from .models import Producto, PedidoItem, Valoracion

class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'stock', 'disponible', 'categoria']
        widgets = {
            'stock': forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'background-color: #eee;'}),
        }

class ModificarPedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'})
        }

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.RadioSelect(choices=[(i, f'{i} estrellas') for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu opinión...'}),
        }
        labels = {
            'estrellas': 'Calificación',
            'comentario': 'Comentario',
        }

ModificarPedidoFormSet = forms.modelformset_factory(
    PedidoItem,
    form=ModificarPedidoForm,
    extra=0,
    can_delete=True
)