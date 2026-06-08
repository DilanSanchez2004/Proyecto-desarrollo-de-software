document.addEventListener('DOMContentLoaded', () => {
    // --- Edit Modal ---
    const modal = document.getElementById('editModal');
    const editForm = document.getElementById('editForm');
    const closeBtn = modal && modal.querySelector('.modal-close');

    if (closeBtn) {
        closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
    }
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });

    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-editar');
        if (!btn) return;

        const id = btn.dataset.id;
        document.getElementById('edit_nombre').value = btn.dataset.nombre;
        document.getElementById('edit_descripcion').value = btn.dataset.descripcion;
        document.getElementById('edit_precio').value = btn.dataset.precio;
        document.getElementById('edit_id_categoria').value = btn.dataset.categoria;
        document.getElementById('edit_imagen_url').value = btn.dataset.imagen;
        document.getElementById('edit_disponible').checked = btn.dataset.disponible === 'true';

        editForm.action = '/admin/productos/' + id + '/editar';
        modal.style.display = 'flex';
    });

    // --- Toggle Disponible ---
    document.body.addEventListener('change', (e) => {
        const toggle = e.target.closest('.toggle-disponible');
        if (!toggle) return;

        const id = toggle.dataset.id;
        fetch('/admin/productos/' + id + '/toggle', { method: 'POST' })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!data.ok) {
                    toggle.checked = !toggle.checked;
                    alert('Error al cambiar disponibilidad');
                }
            })
            .catch(function() {
                toggle.checked = !toggle.checked;
                alert('Error de conexión');
            });
    });
});