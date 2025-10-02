from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Categoria(models.Model):
    """Modelo para categorías de productos"""
    nombre_categoria = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la categoría")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre_categoria']
    
    def __str__(self):
        return self.nombre_categoria


class Cliente(models.Model):
    """Modelo para clientes"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre', 'apellido']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Tienda(models.Model):
    """Modelo para tiendas"""
    nombre_tienda = models.CharField(max_length=200, verbose_name="Nombre de la tienda")
    ubicacion = models.TextField(blank=True, null=True, verbose_name="Ubicación")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"
        ordering = ['nombre_tienda']
    
    def __str__(self):
        return self.nombre_tienda


class LugarEntrega(models.Model):
    """Modelo para lugares de entrega"""
    nombre_lugar = models.CharField(max_length=200, verbose_name="Nombre del lugar")
    direccion = models.TextField(verbose_name="Dirección")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Lugar de entrega"
        verbose_name_plural = "Lugares de entrega"
        ordering = ['nombre_lugar']
    
    def __str__(self):
        return self.nombre_lugar


class Producto(models.Model):
    """Modelo para productos"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Categoría"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def stock_bajo(self):
        """Indica si el producto tiene stock bajo (menos de 10 unidades)"""
        return self.stock < 10
    
    @property
    def precio_formateado(self):
        """Retorna el precio formateado con símbolo de moneda"""
        return f"${self.precio:,.2f}"


class Venta(models.Model):
    """Modelo para ventas"""
    fecha = models.DateTimeField(default=timezone.now, verbose_name="Fecha de venta")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio unitario"
    )
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Total"
    )
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,
        verbose_name="Cliente"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    tienda = models.ForeignKey(
        Tienda, 
        on_delete=models.CASCADE,
        verbose_name="Tienda"
    )
    lugar_entrega = models.ForeignKey(
        LugarEntrega, 
        on_delete=models.CASCADE,
        verbose_name="Lugar de entrega"
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Usuario que registró la venta"
    )
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.producto.nombre} - {self.cliente.nombre_completo}"
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular el total automáticamente"""
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    @property
    def total_formateado(self):
        """Retorna el total formateado con símbolo de moneda"""
        return f"${self.total:,.2f}"


class PerfilUsuario(models.Model):
    """Modelo para extender la información del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    foto_perfil = models.ImageField(
        upload_to='perfiles/', 
        blank=True, 
        null=True, 
        verbose_name="Foto de perfil"
    )
    
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"