# 🍯 Sistema de Ventas TurrónSystem

Un sistema completo de gestión de ventas desarrollado en Python con Flask, diseñado especialmente para la venta de turrones y productos dulces.

## 📋 Características

### ✨ Funcionalidades Principales
- **Autenticación de usuarios** - Sistema de login y registro seguro
- **Dashboard interactivo** - Estadísticas en tiempo real y métricas clave
- **Gestión de clientes** - CRUD completo para administrar clientes
- **Gestión de productos** - Control de inventario con alertas de stock bajo
- **Gestión de categorías** - Organización de productos por categorías
- **Gestión de tiendas** - Administración de múltiples puntos de venta
- **Lugares de entrega** - Configuración de puntos de entrega
- **Sistema de ventas** - Registro de ventas con actualización automática de stock
- **Reportes de ganancias** - Análisis detallado de ingresos y rendimiento

### 🎨 Características Técnicas
- **Frontend moderno** - Diseño responsivo con CSS3 y JavaScript
- **Backend robusto** - Flask con SQLite para máxima compatibilidad
- **Interfaz intuitiva** - UX/UI optimizada para facilidad de uso
- **Validaciones** - Validación tanto en frontend como backend
- **Alertas en tiempo real** - Sistema de notificaciones para el usuario
- **Búsqueda y filtrado** - Funcionalidad de búsqueda en todas las tablas

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o descargar el proyecto
```bash
# Si tienes el proyecto en un repositorio
git clone [URL_DEL_REPOSITORIO]
cd TurronProyectDavid-main

# O simplemente descomprime el archivo ZIP en tu directorio preferido
```

### Paso 2: Crear entorno virtual (recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
TurronProyectDavid-main/
│
├── app.py                     # Aplicación principal Flask
├── requirements.txt           # Dependencias del proyecto
├── README.md                 # Este archivo
│
├── instance/
│   └── sistema_ventas.db     # Base de datos SQLite (se crea automáticamente)
│
├── templates/                # Plantillas HTML
│   ├── base.html            # Plantilla base
│   ├── login.html           # Página de inicio de sesión
│   ├── register.html        # Página de registro
│   ├── dashboard.html       # Dashboard principal
│   ├── clientes.html        # Gestión de clientes
│   ├── productos.html       # Gestión de productos
│   ├── categorias.html      # Gestión de categorías
│   ├── tiendas.html         # Gestión de tiendas
│   ├── lugares_entrega.html # Gestión de lugares de entrega
│   ├── ventas.html          # Gestión de ventas
│   ├── ganancias.html       # Reportes de ganancias
│   └── ...                  # Otras plantillas
│
└── static/                  # Archivos estáticos
    ├── css/
    │   └── style.css        # Estilos CSS
    └── js/
        └── main.js          # JavaScript principal
```

## 🗄️ Base de Datos

El sistema utiliza SQLite con las siguientes tablas:

### Usuarios
- `id_usuario` (PK)
- `nombre`
- `email`
- `password`
- `fecha_registro`

### Clientes
- `id_cliente` (PK)
- `nombre`
- `apellido`
- `telefono`
- `direccion`
- `fecha_registro`

### Productos
- `id_producto` (PK)
- `nombre`
- `descripcion`
- `precio`
- `stock`
- `id_categoria` (FK)
- `fecha_creacion`

### Categorías
- `id_categoria` (PK)
- `nombre_categoria`

### Tiendas
- `id_tienda` (PK)
- `nombre_tienda`
- `ubicacion`
- `fecha_creacion`

### Lugares de Entrega
- `id_lugar` (PK)
- `nombre_lugar`
- `direccion`
- `fecha_creacion`

### Ventas
- `id_venta` (PK)
- `fecha`
- `cantidad`
- `precio_unitario`
- `total`
- `id_cliente` (FK)
- `id_producto` (FK)
- `id_tienda` (FK)
- `id_lugar` (FK)

## 🔧 Uso del Sistema

### 1. Primer Acceso
1. Ejecuta la aplicación con `python app.py`
2. Ve a `http://localhost:5000`
3. Haz clic en "Regístrate aquí" para crear tu primera cuenta
4. Completa el formulario de registro
5. Inicia sesión con tus credenciales

### 2. Configuración Inicial
1. **Categorías**: Crea categorías para tus productos (ej: Turrones, Dulces, Chocolates)
2. **Tiendas**: Registra tus puntos de venta
3. **Lugares de Entrega**: Configura los lugares donde entregas productos
4. **Productos**: Agrega tu inventario con precios y stock inicial
5. **Clientes**: Registra tus clientes

### 3. Operación Diaria
1. **Registrar Ventas**: Ve a "Ventas" → "Nueva Venta"
2. **Monitorear Stock**: El dashboard muestra productos con stock bajo
3. **Ver Reportes**: Accede a reportes de ganancias para análisis
4. **Gestionar Inventario**: Actualiza productos según necesidades

## 🎯 Funcionalidades Destacadas

### Dashboard Inteligente
- Estadísticas en tiempo real
- Alertas de stock bajo
- Ventas recientes
- Accesos rápidos

### Sistema de Ventas Avanzado
- Cálculo automático de totales
- Validación de stock disponible
- Actualización automática de inventario
- Información en tiempo real del producto

### Reportes Completos
- Ganancias totales y por período
- Análisis por producto
- Productos más vendidos
- Participación de mercado

### Interfaz Moderna
- Diseño responsivo para móviles y desktop
- Animaciones suaves
- Iconos intuitivos
- Búsqueda y filtrado en tablas

## 🛠️ Personalización

### Cambiar Colores del Tema
Edita el archivo `static/css/style.css` y modifica las variables de color:
```css
/* Colores principales */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Agregar Nuevas Funcionalidades
1. Agrega nuevas rutas en `app.py`
2. Crea las plantillas HTML correspondientes en `templates/`
3. Actualiza el menú de navegación en `templates/base.html`

### Modificar la Base de Datos
1. Actualiza el esquema en la función `init_db()` en `app.py`
2. Agrega las nuevas rutas y funciones necesarias
3. Crea las plantillas para las nuevas funcionalidades

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Validación de sesiones
- Protección CSRF básica
- Validación de datos de entrada

## 📱 Compatibilidad

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: Desktop, tablet, móvil
- **Sistemas Operativos**: Windows, macOS, Linux

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask
# o
pip install -r requirements.txt
```

### Error: "Database is locked"
1. Cierra todas las instancias de la aplicación
2. Elimina el archivo `instance/sistema_ventas.db`
3. Reinicia la aplicación (se creará una nueva base de datos)

### La aplicación no carga en el navegador
1. Verifica que Python esté ejecutándose sin errores
2. Confirma que el puerto 5000 no esté ocupado
3. Intenta acceder a `http://127.0.0.1:5000` en lugar de `localhost`

## 🚀 Mejoras Futuras

- [ ] Exportación de reportes a PDF/Excel
- [ ] Sistema de backup automático
- [ ] Notificaciones por email
- [ ] API REST para integración con otros sistemas
- [ ] Gráficos interactivos con Chart.js
- [ ] Sistema de roles y permisos
- [ ] Modo oscuro
- [ ] Integración con sistemas de pago

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de estar usando Python 3.7 o superior

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Gracias por usar TurrónSystem! 🍯**

*Desarrollado con ❤️ para pequeños y medianos negocios de productos dulces.*
