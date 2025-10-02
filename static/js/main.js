// Funciones principales del sistema de ventas

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funciones
    initializeFormValidation();
    initializeProductCalculator();
    initializeDataTables();
    initializeAlerts();
    
    // Animaciones de entrada
    animateElements();
});

// Validación de formularios
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Por favor, completa todos los campos requeridos', 'error');
            }
        });
    });
}

function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Calculadora de productos en ventas
function initializeProductCalculator() {
    const productoSelect = document.getElementById('id_producto');
    const cantidadInput = document.getElementById('cantidad');
    const precioDisplay = document.getElementById('precio-display');
    const totalDisplay = document.getElementById('total-display');
    const stockDisplay = document.getElementById('stock-display');
    
    if (productoSelect && cantidadInput) {
        productoSelect.addEventListener('change', updateProductInfo);
        cantidadInput.addEventListener('input', calculateTotal);
    }
}

function updateProductInfo() {
    const productoSelect = document.getElementById('id_producto');
    const productoId = productoSelect.value;
    
    if (!productoId) {
        clearProductInfo();
        return;
    }
    
    // Realizar petición AJAX para obtener información del producto
    fetch(`/api/producto/${productoId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showAlert('Error al obtener información del producto', 'error');
                return;
            }
            
            updateProductDisplay(data);
            calculateTotal();
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error de conexión', 'error');
        });
}

function updateProductDisplay(data) {
    const precioDisplay = document.getElementById('precio-display');
    const stockDisplay = document.getElementById('stock-display');
    
    if (precioDisplay) {
        precioDisplay.textContent = `$${data.precio.toFixed(2)}`;
    }
    
    if (stockDisplay) {
        stockDisplay.textContent = `Stock: ${data.stock}`;
        stockDisplay.className = data.stock < 10 ? 'badge badge-warning' : 'badge badge-success';
    }
    
    // Actualizar el máximo de cantidad
    const cantidadInput = document.getElementById('cantidad');
    if (cantidadInput) {
        cantidadInput.max = data.stock;
    }
}

function calculateTotal() {
    const cantidadInput = document.getElementById('cantidad');
    const precioDisplay = document.getElementById('precio-display');
    const totalDisplay = document.getElementById('total-display');
    
    if (!cantidadInput || !precioDisplay || !totalDisplay) return;
    
    const cantidad = parseInt(cantidadInput.value) || 0;
    const precioText = precioDisplay.textContent.replace('$', '');
    const precio = parseFloat(precioText) || 0;
    
    const total = cantidad * precio;
    totalDisplay.textContent = `Total: $${total.toFixed(2)}`;
    
    // Validar stock
    const stockDisplay = document.getElementById('stock-display');
    if (stockDisplay) {
        const stock = parseInt(stockDisplay.textContent.replace('Stock: ', ''));
        if (cantidad > stock) {
            cantidadInput.classList.add('is-invalid');
            showAlert(`Cantidad excede el stock disponible (${stock})`, 'warning');
        } else {
            cantidadInput.classList.remove('is-invalid');
        }
    }
}

function clearProductInfo() {
    const precioDisplay = document.getElementById('precio-display');
    const totalDisplay = document.getElementById('total-display');
    const stockDisplay = document.getElementById('stock-display');
    
    if (precioDisplay) precioDisplay.textContent = '$0.00';
    if (totalDisplay) totalDisplay.textContent = 'Total: $0.00';
    if (stockDisplay) stockDisplay.textContent = 'Stock: 0';
}

// Inicializar tablas con funcionalidad de búsqueda
function initializeDataTables() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        addSearchFunctionality(table);
        addSortFunctionality(table);
    });
}

function addSearchFunctionality(table) {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Buscar...';
    searchInput.className = 'form-control mb-3';
    
    table.parentNode.insertBefore(searchInput, table);
    
    searchInput.addEventListener('input', function() {
        filterTable(table, this.value);
    });
}

function filterTable(table, searchTerm) {
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matches = text.includes(searchTerm.toLowerCase());
        row.style.display = matches ? '' : 'none';
    });
}

function addSortFunctionality(table) {
    const headers = table.querySelectorAll('th');
    
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => sortTable(table, index));
    });
}

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        // Intentar comparar como números
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Comparar como texto
        return aText.localeCompare(bText);
    });
    
    // Limpiar tbody y agregar filas ordenadas
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

// Sistema de alertas
function initializeAlerts() {
    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            fadeOut(alert);
        }, 5000);
    });
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fade-in`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="close" onclick="this.parentElement.remove()">
            <span>&times;</span>
        </button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        fadeOut(alert);
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alert-container';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1000';
    container.style.maxWidth = '400px';
    
    document.body.appendChild(container);
    return container;
}

// Animaciones
function animateElements() {
    const elements = document.querySelectorAll('.card, .stat-card');
    
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.6s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function fadeOut(element) {
    element.style.transition = 'opacity 0.5s ease';
    element.style.opacity = '0';
    
    setTimeout(() => {
        if (element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }, 500);
}

// Confirmación de eliminación
function confirmDelete(message = '¿Estás seguro de que deseas eliminar este elemento?') {
    return confirm(message);
}

// Formatear números como moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Validar email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validar teléfono
function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone);
}

// Función para exportar datos (placeholder)
function exportData(format = 'csv') {
    showAlert('Función de exportación en desarrollo', 'info');
}

// Función para imprimir reportes
function printReport() {
    window.print();
}

// Actualizar stock en tiempo real
function updateStockDisplay() {
    const stockElements = document.querySelectorAll('[data-stock]');
    
    stockElements.forEach(element => {
        const stock = parseInt(element.dataset.stock);
        
        if (stock < 5) {
            element.classList.add('badge-danger');
            element.classList.remove('badge-warning', 'badge-success');
        } else if (stock < 10) {
            element.classList.add('badge-warning');
            element.classList.remove('badge-danger', 'badge-success');
        } else {
            element.classList.add('badge-success');
            element.classList.remove('badge-danger', 'badge-warning');
        }
    });
}

// Función para generar gráficos (placeholder para futuras mejoras)
function initializeCharts() {
    // Aquí se pueden agregar librerías como Chart.js para gráficos
    console.log('Charts initialization placeholder');
}

// Función para backup de datos
function backupData() {
    showAlert('Creando backup...', 'info');
    // Implementar lógica de backup
}

// Eventos globales
document.addEventListener('click', function(e) {
    // Confirmación para botones de eliminar
    if (e.target.classList.contains('btn-danger') && e.target.textContent.includes('Eliminar')) {
        if (!confirmDelete()) {
            e.preventDefault();
        }
    }
});

// Función para modo oscuro (futuro)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Cargar preferencias del usuario
function loadUserPreferences() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
}

// Función de utilidad para debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

