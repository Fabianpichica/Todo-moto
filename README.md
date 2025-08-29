# raber biker - Proyecto Django

## Descripción
raber biker es una tienda online desarrollada en Django para la gestión y venta de productos de motociclismo. Incluye panel de administración, gestión de inventario, pedidos, clientes y reportes.

## Características principales
- Catálogo de productos y categorías
- Carrito de compras y proceso de checkout
- Gestión de usuarios y autenticación
- Panel de administración para staff
- Gestión de inventario y reportes
- Envío automático de facturas por correo
- Validaciones de seguridad en formularios y archivos

## Requisitos
- Python 3.12+
- Django 5.2.4
- SQLite (por defecto, ideal para desarrollo y proyectos pequeños)
- pip (gestor de paquetes)

> **Nota:** SQLite es suficiente para desarrollo y proyectos pequeños. Si el proyecto crece o necesitas mayor rendimiento/concurrencia, puedes migrar fácilmente a PostgreSQL, MySQL u otra base de datos compatible con Django. Consulta la documentación oficial para migraciones.

## Instalación
1. Clona el repositorio y entra al directorio del proyecto.
2. Crea un entorno virtual:
   ```bash
   python3 -m venv env_312
   source env_312/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```
5. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
6. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Dependencias principales
- Django==5.2.4
- (Agrega aquí otras dependencias si las tienes en requirements.txt)

## Estructura del proyecto
- `core/`, `productos/`, `dashboard_admin/`, `inventario/`: Apps principales
- `media/`: Archivos subidos por usuarios
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `manual_usuario_motogm.md`: Manual para usuarios
- `manual_admin_motogm.md`: Manual para administradores

## Seguridad
- Validaciones estrictas en formularios
- Protección CSRF y cookies seguras listas para producción
- Uso de variables de entorno para datos sensibles
- Recomendaciones de seguridad en los manuales

## Despliegue
- Cambia `DEBUG = False` y configura `ALLOWED_HOSTS` en producción
- Activa cookies seguras y usa HTTPS
- Usa una base de datos robusta para producción
- Sirve archivos estáticos y media correctamente

## Contacto y soporte
- Para soporte técnico, consulta los manuales o escribe a raberbikes@gmail.com

---

¡Gracias por usar raber biker!
