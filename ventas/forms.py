from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Producto, Categoria, Tienda, LugarEntrega, Venta, PerfilUsuario


class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado para registro de usuarios"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ClienteForm(forms.ModelForm):
    """Formulario para clientes"""
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección'
            }),
        }


class ProductoForm(forms.ModelForm):
    """Formulario para productos"""
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].empty_label = "Seleccione una categoría"


class CategoriaForm(forms.ModelForm):
    """Formulario para categorías"""
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            }),
        }


class TiendaForm(forms.ModelForm):
    """Formulario para tiendas"""
    class Meta:
        model = Tienda
        fields = ['nombre_tienda', 'ubicacion']
        widgets = {
            'nombre_tienda': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la tienda'
            }),
            'ubicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la ubicación'
            }),
        }


class LugarEntregaForm(forms.ModelForm):
    """Formulario para lugares de entrega"""
    class Meta:
        model = LugarEntrega
        fields = ['nombre_lugar', 'direccion']
        widgets = {
            'nombre_lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del lugar'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección'
            }),
        }


class VentaForm(forms.ModelForm):
    """Formulario para ventas"""
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad', 'tienda', 'lugar_entrega']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_cliente'
            }),
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'id': 'id_cantidad',
                'placeholder': '1'
            }),
            'tienda': forms.Select(attrs={
                'class': 'form-control'
            }),
            'lugar_entrega': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)
        self.fields['tienda'].queryset = Tienda.objects.all()
        self.fields['lugar_entrega'].queryset = LugarEntrega.objects.all()
        
        # Labels personalizados
        self.fields['cliente'].empty_label = "Seleccione un cliente"
        self.fields['producto'].empty_label = "Seleccione un producto"
        self.fields['tienda'].empty_label = "Seleccione una tienda"
        self.fields['lugar_entrega'].empty_label = "Seleccione un lugar de entrega"
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')
        
        if producto and cantidad:
            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f'Stock insuficiente. Stock disponible: {producto.stock}'
                )
        
        return cantidad


class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para perfil de usuario"""
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'fecha_nacimiento', 'foto_perfil']
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su teléfono'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class BusquedaForm(forms.Form):
    """Formulario para búsquedas"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...',
            'id': 'search-input'
        })
    )
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
