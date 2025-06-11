// Funciones comunes para el panel
document.addEventListener('DOMContentLoaded', function() {
    // Confirmación para acciones importantes
    document.querySelectorAll('.btn-danger').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Estás seguro de realizar esta acción?')) {
                e.preventDefault();
            }
        });
    });

    // Notificaciones
    function showNotification(message, type = 'success') {
        const notif = document.createElement('div');
        notif.className = `notification ${type}`;
        notif.textContent = message;
        document.body.appendChild(notif);
        
        setTimeout(() => notif.remove(), 5000);
    }
    
    // Exponer para uso global
    window.showNotification = showNotification;
});