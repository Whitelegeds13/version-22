from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario, Venta, Producto


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crear perfil de usuario automáticamente cuando se crea un usuario"""
    if created:
        PerfilUsuario.objects.create(usuario=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guardar el perfil de usuario cuando se guarda el usuario"""
    if hasattr(instance, 'perfilusuario'):
        instance.perfilusuario.save()


@receiver(pre_save, sender=Venta)
def actualizar_stock_producto(sender, instance, **kwargs):
    """Actualizar el stock del producto cuando se registra una venta"""
    if instance.pk is None:  # Nueva venta
        producto = instance.producto
        if producto.stock >= instance.cantidad:
            producto.stock -= instance.cantidad
            producto.save()
        else:
            raise ValueError(f"Stock insuficiente. Stock disponible: {producto.stock}")


@receiver(pre_save, sender=Venta)
def calcular_total_venta(sender, instance, **kwargs):
    """Calcular el total de la venta automáticamente"""
    instance.total = instance.cantidad * instance.precio_unitario
