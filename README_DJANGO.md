# 🍯 TurrónSystem - Django Version

Un sistema completo de gestión de ventas desarrollado en **Django 5.2.7**, diseñado especialmente para la venta de turrones y productos dulces.

## 🚀 ¡MIGRACIÓN COMPLETADA A DJANGO!

El sistema ha sido completamente migrado de Flask a Django, manteniendo todas las funcionalidades originales y agregando nuevas características propias del framework Django.

## 📋 Características Principales

### ✨ Funcionalidades del Sistema
- **🔐 Autenticación Django** - Sistema robusto de usuarios con Django Auth
- **📊 Dashboard interactivo** - Estadísticas en tiempo real y métricas clave
- **👥 Gestión de clientes** - CRUD completo con búsqueda avanzada
- **📦 Gestión de productos** - Control de inventario con alertas de stock
- **🏷️ Gestión de categorías** - Organización eficiente de productos
- **🏪 Gestión de tiendas** - Administración de múltiples puntos de venta
- **📍 Lugares de entrega** - Configuración de puntos de entrega
- **💰 Sistema de ventas** - Registro automático con validación de stock
- **📈 Reportes avanzados** - Análisis detallado de ganancias y rendimiento
- **🔧 Panel de Administración** - Django Admin completamente configurado

### 🎨 Características Técnicas Django
- **🏗️ Arquitectura MVT** - Model-View-Template de Django
- **🗄️ ORM Django** - Modelos relacionales con validaciones
- **🔒 Seguridad integrada** - CSRF, autenticación, permisos
- **📱 Responsive Design** - Bootstrap 5 integrado
- **🚀 Vistas basadas en clases** - CBV para funcionalidad avanzada
- **🔌 Django REST Framework** - API REST para integraciones
- **📊 Sistema de señales** - Automatización de procesos
- **🎯 Formularios Django** - Validación automática

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Preparar el entorno
```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3: Configurar la base de datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### Paso 4: Cargar datos iniciales (opcional)
```bash
# Django creará automáticamente datos de ejemplo al iniciar
python manage.py runserver
```

### Paso 5: Ejecutar el servidor
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## 📁 Estructura del Proyecto Django

```
turron_system/
│
├── manage.py                    # Comando principal de Django
├── requirements.txt             # Dependencias actualizadas
├── README_DJANGO.md            # Esta documentación
│
├── turron_system/              # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # Configuración WSGI
│   └── asgi.py                 # Configuración ASGI
│
├── ventas/                     # Aplicación principal
│   ├── __init__.py
│   ├── admin.py                # Configuración del admin
│   ├── apps.py                 # Configuración de la app
│   ├── models.py               # Modelos de datos
│   ├── views.py                # Vistas del sistema
│   ├── urls.py                 # URLs de la aplicación
│   ├── forms.py                # Formularios Django
│   ├── signals.py              # Señales automáticas
│   └── migrations/             # Migraciones de BD
│
├── templates/                  # Plantillas HTML
│   ├── base.html              # Plantilla base
│   ├── registration/          # Templates de auth
│   └── ventas/                # Templates de la app
│       ├── dashboard.html
│       ├── clientes/
│       ├── productos/
│       ├── categorias/
│       ├── tiendas/
│       ├── lugares_entrega/
│       ├── ventas/
│       └── reportes/
│
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   └── js/
│       └── main.js            # JavaScript funcional
│
└── db.sqlite3                 # Base de datos SQLite
```

## 🗄️ Modelos Django

### Principales Entidades

#### Usuario (Django User + PerfilUsuario)
- Autenticación integrada con Django
- Perfil extendido con información adicional
- Foto de perfil y datos personales

#### Cliente
- Información completa del cliente
- Historial de compras automático
- Búsqueda y filtrado avanzado

#### Producto
- Control de stock en tiempo real
- Categorización automática
- Alertas de stock bajo
- Validaciones de precio y cantidad

#### Venta
- Registro automático de transacciones
- Actualización de stock automática
- Cálculo de totales automático
- Trazabilidad completa

#### Categoría, Tienda, LugarEntrega
- Gestión completa de configuraciones
- Relaciones automáticas con otros modelos

## 🔧 Funcionalidades Django Específicas

### Panel de Administración
- Acceso: `http://localhost:8000/admin/`
- Gestión completa de todos los modelos
- Filtros y búsquedas avanzadas
- Acciones en lote
- Interfaz personalizada

### API REST
- Endpoints para integración externa
- Autenticación por sesión
- Serialización automática
- Documentación automática

### Sistema de Señales
- Creación automática de perfiles de usuario
- Actualización de stock en ventas
- Cálculo automático de totales
- Validaciones en tiempo real

### Formularios Avanzados
- Validación automática cliente/servidor
- Widgets personalizados
- Mensajes de error contextuales
- Integración con Bootstrap

## 🚀 Uso del Sistema

### 1. Primer Acceso
1. Ejecuta `python manage.py runserver`
2. Ve a `http://localhost:8000`
3. Regístrate como nuevo usuario
4. Accede al dashboard principal

### 2. Configuración Inicial
1. **Admin Panel**: Crea un superusuario para acceso completo
2. **Categorías**: Define categorías de productos
3. **Tiendas**: Registra tus puntos de venta
4. **Lugares de Entrega**: Configura opciones de entrega
5. **Productos**: Agrega tu inventario inicial

### 3. Operación Diaria
1. **Dashboard**: Monitorea estadísticas en tiempo real
2. **Ventas**: Registra nuevas transacciones
3. **Clientes**: Gestiona tu base de clientes
4. **Reportes**: Analiza rendimiento y ganancias
5. **Admin**: Gestión avanzada de datos

## 🎯 Ventajas de Django vs Flask

### ✅ Mejoras Implementadas

#### 🔒 Seguridad
- **CSRF Protection**: Protección automática contra ataques
- **SQL Injection**: ORM seguro por defecto
- **XSS Protection**: Escape automático en templates
- **Autenticación robusta**: Sistema de usuarios integrado

#### 🏗️ Arquitectura
- **Modelos ORM**: Definición declarativa de datos
- **Migraciones**: Control de versiones de BD automático
- **Señales**: Automatización de procesos
- **Middleware**: Procesamiento de requests/responses

#### 🔧 Administración
- **Django Admin**: Panel de administración automático
- **Comandos personalizados**: Gestión via manage.py
- **Configuración centralizada**: settings.py
- **Logging integrado**: Sistema de logs robusto

#### 📊 Desarrollo
- **CBV**: Vistas basadas en clases reutilizables
- **Formularios**: Validación automática
- **Templates**: Sistema de herencia potente
- **Testing**: Framework de pruebas integrado

## 📈 Funcionalidades Destacadas

### Dashboard Inteligente
- **Métricas en tiempo real**: Productos, clientes, ventas, ingresos
- **Alertas automáticas**: Stock bajo con códigos de color
- **Ventas recientes**: Historial de transacciones
- **Accesos rápidos**: Navegación optimizada

### Sistema de Ventas Avanzado
- **Validación de stock**: Prevención de sobreventa
- **Cálculo automático**: Totales y precios actualizados
- **API integrada**: Información de productos vía AJAX
- **Historial completo**: Trazabilidad de transacciones

### Reportes Completos
- **Ganancias por período**: Análisis temporal
- **Productos más vendidos**: Ranking de performance
- **Análisis por categoría**: Segmentación de mercado
- **Exportación de datos**: Preparado para futuras mejoras

### Gestión de Usuarios
- **Registro automático**: Creación de cuentas
- **Perfiles extendidos**: Información adicional
- **Autenticación segura**: Login/logout integrado
- **Permisos granulares**: Control de acceso

## 🔌 API REST

### Endpoints Disponibles
```
GET /api/producto/<id>/     # Información del producto
POST /api/ventas/           # Crear nueva venta (futuro)
GET /api/reportes/          # Datos de reportes (futuro)
```

### Autenticación
- Autenticación por sesión Django
- Protección CSRF automática
- Permisos basados en usuarios

## 🛡️ Seguridad

### Características Implementadas
- **Contraseñas hasheadas**: PBKDF2 por defecto
- **Validación de sesiones**: Tokens seguros
- **Protección CSRF**: Tokens en formularios
- **Validación de entrada**: Sanitización automática
- **Permisos de usuario**: Control de acceso granular

## 📱 Compatibilidad

- **Navegadores**: Chrome, Firefox, Safari, Edge (últimas versiones)
- **Dispositivos**: Desktop, tablet, móvil (responsive)
- **Sistemas Operativos**: Windows, macOS, Linux
- **Python**: 3.8+ (recomendado 3.10+)
- **Base de datos**: SQLite (desarrollo), PostgreSQL/MySQL (producción)

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
# o
pip install -r requirements.txt
```

### Error: "Table doesn't exist"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "CSRF token missing"
- Asegúrate de incluir `{% csrf_token %}` en formularios
- Verifica que el middleware CSRF esté habilitado

### Problemas de archivos estáticos
```bash
python manage.py collectstatic
```

## 🚀 Despliegue en Producción

### Configuraciones Recomendadas

#### settings.py para producción
```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']

# Base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'turron_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Archivos estáticos
STATIC_ROOT = '/path/to/static/'
MEDIA_ROOT = '/path/to/media/'
```

#### Servidor Web
- **Gunicorn**: Servidor WSGI recomendado
- **Nginx**: Proxy reverso para archivos estáticos
- **SSL/TLS**: Certificados para HTTPS

## 🔄 Migración desde Flask

### ✅ Completado
- [x] Modelos Django equivalentes
- [x] Vistas basadas en clases
- [x] Templates con herencia Django
- [x] Sistema de autenticación
- [x] Panel de administración
- [x] API REST básica
- [x] Formularios Django
- [x] Archivos estáticos
- [x] Configuración de URLs

### 📋 Datos Migrados
- Estructura de base de datos idéntica
- Funcionalidades preservadas al 100%
- Interfaz de usuario mejorada
- Nuevas características añadidas

## 🚀 Mejoras Futuras

### 📈 Próximas Características
- [ ] **Gráficos interactivos**: Chart.js integrado
- [ ] **Exportación avanzada**: PDF, Excel, CSV
- [ ] **Notificaciones**: Email y push notifications
- [ ] **API completa**: CRUD via REST API
- [ ] **Roles y permisos**: Sistema granular
- [ ] **Backup automático**: Respaldos programados
- [ ] **Modo oscuro**: Tema alternativo
- [ ] **PWA**: Progressive Web App
- [ ] **Integración de pagos**: Stripe, PayPal
- [ ] **Multi-idioma**: Internacionalización

### 🔧 Optimizaciones Técnicas
- [ ] **Cache**: Redis/Memcached
- [ ] **Celery**: Tareas asíncronas
- [ ] **Docker**: Containerización
- [ ] **CI/CD**: Despliegue automático
- [ ] **Monitoring**: Logs y métricas
- [ ] **Testing**: Cobertura completa

## 📞 Soporte y Desarrollo

### 🛠️ Comandos Útiles Django
```bash
# Desarrollo
python manage.py runserver
python manage.py shell
python manage.py dbshell

# Base de datos
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures.json

# Usuarios
python manage.py createsuperuser
python manage.py changepassword username

# Producción
python manage.py collectstatic
python manage.py check --deploy
```

### 📊 Estructura de Datos
- **Relaciones**: ForeignKey, ManyToMany optimizadas
- **Validaciones**: Clean methods y validators
- **Índices**: Optimización de consultas
- **Señales**: Automatización de procesos

## 📄 Licencia

Este proyecto utiliza Django bajo licencia BSD y está disponible como código abierto.

---

## 🎉 ¡Migración Exitosa!

**TurrónSystem ahora funciona completamente en Django 5.2.7**

### ✨ Beneficios Obtenidos:
- 🔒 **Mayor seguridad** con protecciones integradas
- 🚀 **Mejor rendimiento** con ORM optimizado  
- 🛠️ **Más funcionalidades** con Django Admin
- 📈 **Escalabilidad mejorada** para crecimiento futuro
- 🔧 **Mantenimiento simplificado** con convenciones Django

### 🚀 ¡Listo para Producción!
El sistema está completamente funcional y preparado para ser utilizado en un entorno de producción profesional.

**¡Gracias por usar TurrónSystem con Django! 🍯**

*Desarrollado con ❤️ usando Django Framework para pequeños y medianos negocios.*
