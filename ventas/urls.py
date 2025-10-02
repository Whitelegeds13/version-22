from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registro, name='register'),
    
    # Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
    
    # Productos
    path('productos/', views.ProductoListView.as_view(), name='producto_lista'),
    path('productos/crear/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
    
    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_lista'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    
    # Tiendas
    path('tiendas/', views.TiendaListView.as_view(), name='tienda_lista'),
    path('tiendas/crear/', views.TiendaCreateView.as_view(), name='tienda_crear'),
    
    # Lugares de Entrega
    path('lugares-entrega/', views.LugarEntregaListView.as_view(), name='lugar_entrega_lista'),
    path('lugares-entrega/crear/', views.LugarEntregaCreateView.as_view(), name='lugar_entrega_crear'),
    path('lugares-entrega/<int:pk>/editar/', views.LugarEntregaUpdateView.as_view(), name='lugar_entrega_editar'),
    
    # Ventas
    path('ventas/', views.VentaListView.as_view(), name='venta_lista'),
    path('ventas/crear/', views.VentaCreateView.as_view(), name='venta_crear'),
    
    # API
    path('api/producto/<int:producto_id>/', views.api_producto_info, name='api_producto_info'),
    
    # Reportes
    path('reportes/ganancias/', views.reportes_ganancias, name='reportes_ganancias'),
    path('reportes/productos/', views.reportes_productos, name='reportes_productos'),
]
