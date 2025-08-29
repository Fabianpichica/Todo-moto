# Manual de Usuario Administrador raber biker

## Introducción
Este manual está dirigido a los administradores de la tienda raber biker. Explica cómo gestionar productos, categorías, pedidos, clientes y el inventario desde el panel de administración.

---

## 1. Acceso al panel de administración
- Ingresa con tu usuario y contraseña de administrador.
- Solo usuarios con permisos de staff/admin pueden acceder al panel.

---

## 2. Gestión de productos
- Accede a "Gestión de Productos" para ver, crear, editar o eliminar productos.
- Puedes modificar precios, stock, imágenes y descripciones.
- Recuerda actualizar el stock tras cada venta o ingreso de inventario.

---

## 3. Gestión de categorías
- En "Gestión de Categorías" puedes crear nuevas categorías, editar nombres y eliminar las que no se usen.
- Asigna productos a categorías para facilitar la navegación de los clientes.

---

## 4. Gestión de pedidos
- En "Pedidos de Clientes" puedes ver el historial de pedidos realizados.
- Consulta el estado de cada pedido (pendiente, pagado, enviado, etc.).
- Descarga facturas en PDF y verifica los datos del cliente y productos comprados.
- Cambia el estado del pedido según el avance (por ejemplo, de "Pendiente" a "Enviado").

---

## 5. Gestión de clientes
- En "Gestión de Clientes" puedes ver la lista de usuarios registrados.
- Consulta sus datos de contacto y el historial de compras.
- Edita información relevante si es necesario.

---

## 6. Gestión de inventario
- Accede a "Gestión de Inventario" para registrar entradas y salidas de productos.
- Cada movimiento queda registrado con motivo, cantidad y usuario responsable.
- Mantén actualizado el stock para evitar ventas de productos agotados.

---

## 7. Reportes y estadísticas
- El panel de reportes muestra estadísticas de ventas, productos más vendidos y actividad reciente.
- Usa esta información para tomar decisiones comerciales y de inventario.

---

## 8. Envío de facturas y notificaciones
- El sistema envía automáticamente facturas por correo tras cada pedido.
- Si un cliente reporta no haber recibido la factura, verifica el estado del pedido y el correo registrado.

---

## 9. Seguridad y buenas prácticas
- No compartas tu usuario y contraseña de administrador.
- Cierra sesión al terminar tu gestión.
- Revisa periódicamente los permisos de los usuarios staff.

---

## 10. Soporte técnico
- Para problemas técnicos, contacta al desarrollador o escribe a raberbikes@gmail.com.

---

## 11. Checklist de seguridad y despliegue
- Cambia `DEBUG = False` en producción.
- Configura `ALLOWED_HOSTS` con el dominio real.
- Activa cookies seguras (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) cuando uses HTTPS.
- Usa variables de entorno para claves y contraseñas.
- Revisa los permisos de usuarios staff/admin periódicamente.
- No publiques la clave secreta ni contraseñas en repositorios.
- Usa una base de datos robusta en producción (no SQLite).
- Sirve archivos estáticos y media correctamente.
- Mantén Django y dependencias actualizadas.

---

¡Gracias por gestionar raber biker!
