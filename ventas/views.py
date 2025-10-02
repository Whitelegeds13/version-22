from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Cliente, Producto, Categoria, Tienda, LugarEntrega, Venta
from .forms import ClienteForm, ProductoForm, CategoriaForm, TiendaForm, LugarEntregaForm, VentaForm


# Vista de inicio y dashboard
@login_required
def dashboard(request):
    """Dashboard principal con estadísticas"""
    # Estadísticas generales
    total_productos = Producto.objects.count()
    total_clientes = Cliente.objects.count()
    total_ventas = Venta.objects.count()
    ingresos_totales = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
    
    # Productos con stock bajo
    productos_stock_bajo = Producto.objects.filter(stock__lt=10).order_by('stock')[:5]
    
    # Ventas recientes
    ventas_recientes = Venta.objects.select_related(
        'cliente', 'producto', 'tienda', 'lugar_entrega'
    ).order_by('-fecha')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'ingresos_totales': ingresos_totales,
        'productos_stock_bajo': productos_stock_bajo,
        'ventas_recientes': ventas_recientes,
    }
    
    return render(request, 'ventas/dashboard.html', context)


# Vista de registro
def registro(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Vistas de Clientes
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'ventas/clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(apellido__icontains=search) |
                Q(telefono__icontains=search)
            )
        return queryset.order_by('nombre', 'apellido')


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/clientes/crear.html'
    success_url = reverse_lazy('cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente!')
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/clientes/editar.html'
    success_url = reverse_lazy('cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente!')
        return super().form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'ventas/clientes/eliminar.html'
    success_url = reverse_lazy('cliente_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)


# Vistas de Productos
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'ventas/productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria')
        search = self.request.GET.get('search')
        categoria = self.request.GET.get('categoria')
        
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(descripcion__icontains=search)
            )
        
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        return queryset.order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ventas/productos/crear.html'
    success_url = reverse_lazy('producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto creado exitosamente!')
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ventas/productos/editar.html'
    success_url = reverse_lazy('producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente!')
        return super().form_valid(form)


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'ventas/productos/eliminar.html'
    success_url = reverse_lazy('producto_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)


# Vistas de Categorías
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'ventas/categorias/lista.html'
    context_object_name = 'categorias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar conteo de productos por categoría
        for categoria in context['categorias']:
            categoria.productos_count = categoria.producto_set.count()
        return context


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'ventas/categorias/crear.html'
    success_url = reverse_lazy('categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente!')
        return super().form_valid(form)


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'ventas/categorias/editar.html'
    success_url = reverse_lazy('categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente!')
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'ventas/categorias/eliminar.html'
    success_url = reverse_lazy('categoria_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada exitosamente!')
        return super().delete(request, *args, **kwargs)


# Vistas de Tiendas
class TiendaListView(LoginRequiredMixin, ListView):
    model = Tienda
    template_name = 'ventas/tiendas/lista.html'
    context_object_name = 'tiendas'


class TiendaCreateView(LoginRequiredMixin, CreateView):
    model = Tienda
    form_class = TiendaForm
    template_name = 'ventas/tiendas/crear.html'
    success_url = reverse_lazy('tienda_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tienda creada exitosamente!')
        return super().form_valid(form)


# Vistas de Lugares de Entrega
class LugarEntregaListView(LoginRequiredMixin, ListView):
    model = LugarEntrega
    template_name = 'ventas/lugares_entrega/lista.html'
    context_object_name = 'lugares'


class LugarEntregaCreateView(LoginRequiredMixin, CreateView):
    model = LugarEntrega
    form_class = LugarEntregaForm
    template_name = 'ventas/lugares_entrega/crear.html'
    success_url = reverse_lazy('lugar_entrega_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lugar de entrega creado exitosamente!')
        return super().form_valid(form)


class LugarEntregaUpdateView(LoginRequiredMixin, UpdateView):
    model = LugarEntrega
    form_class = LugarEntregaForm
    template_name = 'ventas/lugares_entrega/editar.html'
    success_url = reverse_lazy('lugar_entrega_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lugar de entrega actualizado exitosamente!')
        return super().form_valid(form)


# Vistas de Ventas
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/ventas/lista.html'
    context_object_name = 'ventas'
    paginate_by = 20
    
    def get_queryset(self):
        return Venta.objects.select_related(
            'cliente', 'producto', 'tienda', 'lugar_entrega', 'usuario'
        ).order_by('-fecha')


class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/ventas/crear.html'
    success_url = reverse_lazy('venta_lista')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.precio_unitario = form.instance.producto.precio
        
        # Verificar stock
        producto = form.instance.producto
        if producto.stock < form.instance.cantidad:
            messages.error(
                self.request, 
                f'Stock insuficiente. Stock disponible: {producto.stock}'
            )
            return self.form_invalid(form)
        
        messages.success(self.request, 'Venta registrada exitosamente!')
        return super().form_valid(form)


# API Views
@login_required
def api_producto_info(request, producto_id):
    """API para obtener información del producto"""
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio': float(producto.precio),
            'stock': producto.stock,
            'nombre': producto.nombre
        })
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


# Vistas de Reportes
@login_required
def reportes_ganancias(request):
    """Vista de reportes de ganancias"""
    # Ganancias por mes
    ganancias_mes = Venta.objects.annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total_mes=Sum('total')
    ).order_by('-mes')[:12]
    
    # Ganancias totales
    total_ganancias = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
    
    # Productos más vendidos
    productos_vendidos = Venta.objects.values(
        'producto__nombre'
    ).annotate(
        total_vendido=Sum('cantidad'),
        ingresos=Sum('total')
    ).order_by('-total_vendido')[:10]
    
    context = {
        'ganancias_mes': ganancias_mes,
        'total_ganancias': total_ganancias,
        'productos_vendidos': productos_vendidos,
    }
    
    return render(request, 'ventas/reportes/ganancias.html', context)


@login_required
def reportes_productos(request):
    """Vista de reportes por producto"""
    productos_reporte = Venta.objects.values(
        'producto__nombre',
        'producto__precio'
    ).annotate(
        total_vendido=Sum('cantidad'),
        ingresos_totales=Sum('total'),
        precio_promedio=Sum('precio_unitario') / Count('id')
    ).order_by('-ingresos_totales')
    
    context = {
        'productos_reporte': productos_reporte,
    }
    
    return render(request, 'ventas/reportes/productos.html', context)
