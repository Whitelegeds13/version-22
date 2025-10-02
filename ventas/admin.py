from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Categoria, Cliente, Producto, Tienda, LugarEntrega, Venta, PerfilUsuario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria', 'fecha_creacion']
    search_fields = ['nombre_categoria']
    list_filter = ['fecha_creacion']
    ordering = ['nombre_categoria']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'telefono', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'telefono']
    list_filter = ['fecha_registro']
    ordering = ['nombre', 'apellido']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ['nombre_tienda', 'ubicacion', 'fecha_creacion']
    search_fields = ['nombre_tienda', 'ubicacion']
    list_filter = ['fecha_creacion']
    ordering = ['nombre_tienda']


@admin.register(LugarEntrega)
class LugarEntregaAdmin(admin.ModelAdmin):
    list_display = ['nombre_lugar', 'direccion', 'fecha_creacion']
    search_fields = ['nombre_lugar', 'direccion']
    list_filter = ['fecha_creacion']
    ordering = ['nombre_lugar']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'stock_bajo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['categoria', 'fecha_creacion']
    ordering = ['nombre']
    list_editable = ['precio', 'stock']
    
    def stock_bajo(self, obj):
        return obj.stock_bajo
    stock_bajo.boolean = True
    stock_bajo.short_description = 'Stock Bajo'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('categoria')


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'cliente', 'producto', 'cantidad', 'precio_unitario', 'total', 'tienda', 'usuario']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'producto__nombre']
    list_filter = ['fecha', 'tienda', 'lugar_entrega', 'usuario']
    ordering = ['-fecha']
    readonly_fields = ['total']
    date_hierarchy = 'fecha'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'cliente', 'producto', 'tienda', 'lugar_entrega', 'usuario'
        )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva venta
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


# Inline para PerfilUsuario en el admin de User
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


# Extender el UserAdmin para incluir el perfil
class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Personalizar el admin site
admin.site.site_header = "TurrónSystem - Administración"
admin.site.site_title = "TurrónSystem Admin"
admin.site.index_title = "Panel de Administración"