# Manual Unificado de Usuario y Administrador - raber biker

## Introducción
Este manual reúne la información para usuarios y administradores de la tienda online raber biker. Aquí aprenderás a comprar, gestionar tu cuenta, administrar productos, pedidos, clientes, inventario y mantener la seguridad del sistema.

---

## Sección Usuario

### 1. Registro y acceso
- Puedes comprar como usuario registrado o anónimo.
- Para registrarte, haz clic en "Registrarse" y completa el formulario. Recibirás un correo de bienvenida.
- Si ya tienes cuenta, inicia sesión con tu usuario y contraseña.

### 2. Navegación y búsqueda de productos
- Usa el menú principal para explorar categorías y productos.
- Puedes buscar productos por nombre o descripción usando la barra de búsqueda.

### 3. Carrito de compras
- Añade productos al carrito desde la página de detalle o listado.
- Puedes ver tu carrito en cualquier momento y modificar cantidades o eliminar productos.
- El sistema fusiona automáticamente tu carrito anónimo con tu cuenta al iniciar sesión.

### 4. Proceso de compra (Checkout)
- Haz clic en "Finalizar compra" para ir al checkout.
- Completa el formulario con tus datos de envío y selecciona el método de pago.
- Revisa el resumen de tu pedido antes de confirmar.

### 5. Confirmación y factura
- Tras confirmar tu pedido, recibirás un mensaje en pantalla y un correo electrónico con la factura.
- La factura incluye el logo de la tienda, tus datos, los productos comprados y el total pagado.
- Si no recibes el correo, revisa tu carpeta de spam.

### 6. Gestión de cuenta y pedidos
- Accede a "Mi cuenta" para actualizar tus datos personales y dirección de envío.
- En "Mis pedidos" puedes consultar el historial de compras y descargar facturas.
- El menú de usuario incluye la opción "Mis Favoritos" para gestionar tus productos favoritos.

### 7. Favoritos (Wishlist)
- Puedes agregar o quitar productos de tu lista de favoritos desde la página de detalle de cada producto.
- Accede a "Mis Favoritos" desde el menú de usuario para ver todos tus productos guardados.
- Desde esta sección puedes ir directamente a la página de cada producto o eliminarlos de tu lista.

### 8. Valoraciones y comentarios de productos
- Puedes dejar una valoración (de 1 a 5 estrellas) y un comentario en la página de detalle de cada producto.
- Solo los usuarios registrados pueden valorar y comentar.
- Las valoraciones y comentarios son visibles para todos los usuarios en la sección de opiniones del producto.
- Se muestra el promedio de estrellas y el número de opiniones en cada producto.

### 9. Recuperación de contraseña
- Si olvidas tu contraseña, usa la opción "¿Olvidaste tu contraseña?" para recibir instrucciones por correo.

### 10. Contacto y soporte
- Para dudas o soporte, utiliza el formulario de contacto disponible en la web.
- También puedes escribir a raberbikes@gmail.com.

### 11. Notas técnicas
- El sistema envía correos automáticos usando Gmail y una clave de aplicación.
- Si tienes problemas con la recepción de correos, verifica tu dirección y revisa el spam.

### 12. Seguridad, privacidad y validaciones
- Tus datos están protegidos y solo se usan para procesar pedidos y notificaciones.
- El sistema valida que los datos ingresados sean correctos y seguros (por ejemplo, no se permiten números negativos, ceros en precios/cantidades, ni caracteres inválidos en los formularios).
- Las imágenes subidas son verificadas para asegurar que sean del tipo y tamaño adecuado.
- Las cookies y la información de sesión están protegidas mediante protocolos seguros.
- Recuerda cerrar sesión en dispositivos compartidos para proteger tu cuenta.

---

## Sección Administrador

### 1. Acceso al panel de administración
- Ingresa con tu usuario y contraseña de administrador.
- Solo usuarios con permisos de staff/admin pueden acceder al panel.

### 2. Gestión de productos
- Accede a "Gestión de Productos" para ver, crear, editar o eliminar productos.
- Puedes modificar precios, stock, imágenes y descripciones.
- Recuerda actualizar el stock tras cada venta o ingreso de inventario.

### 3. Gestión de categorías
- En "Gestión de Categorías" puedes crear nuevas categorías, editar nombres y eliminar las que no se usen.
- Asigna productos a categorías para facilitar la navegación de los clientes.

### 4. Gestión de pedidos
- En "Pedidos de Clientes" puedes ver el historial de pedidos realizados.
- Consulta el estado de cada pedido (pendiente, pagado, enviado, etc.).
- Descarga facturas en PDF y verifica los datos del cliente y productos comprados.
- Cambia el estado del pedido según el avance (por ejemplo, de "Pendiente" a "Enviado").

### 5. Gestión de clientes
- En "Gestión de Clientes" puedes ver la lista de usuarios registrados.
- Consulta sus datos de contacto y el historial de compras.
- Edita información relevante si es necesario.

### 6. Gestión de inventario
- Accede a "Gestión de Inventario" para registrar entradas y salidas de productos.
- Cada movimiento queda registrado con motivo, cantidad y usuario responsable.
- Mantén actualizado el stock para evitar ventas de productos agotados.

### 7. Reportes y estadísticas
- El panel de reportes muestra estadísticas de ventas, productos más vendidos y actividad reciente.
- Usa esta información para tomar decisiones comerciales y de inventario.

### 8. Envío de facturas y notificaciones
- El sistema envía automáticamente facturas por correo tras cada pedido.
- Si un cliente reporta no haber recibido la factura, verifica el estado del pedido y el correo registrado.

### 9. Seguridad y buenas prácticas
- No compartas tu usuario y contraseña de administrador.
- Cierra sesión al terminar tu gestión.
- Revisa periódicamente los permisos de los usuarios staff.

### 10. Soporte técnico
- Para problemas técnicos, contacta al desarrollador o escribe a raberbikes@gmail.com.

### 11. Checklist de seguridad y despliegue
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

¡Gracias por confiar y gestionar raber biker!
