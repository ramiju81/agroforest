function openUserModal() {
    document.getElementById('userModal').style.display = 'flex';
}

function closeUserModal() {
    document.getElementById('userModal').style.display = 'none';
}

function generarUsername() {
    const rol = document.getElementById('rol').value;
    const nombre1 = document.querySelector('[name=nombre1]').value.toUpperCase();
    const apellido1 = document.querySelector('[name=apellido1]').value.toUpperCase();
    if (nombre1 && apellido1) {
        const usuario = `${rol}_${nombre1.slice(0, 2)}${apellido1.slice(0, 2)}`;
        document.getElementById('username').value = usuario;
    }
}

document.getElementById('userForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const datos = Object.fromEntries(formData.entries());
    datos.fecha_creacion = new Date().toISOString();

    // Simulación de envío
    console.log('Usuario registrado:', datos);
    alert('Usuario registrado exitosamente');
    this.reset();
    closeUserModal();
});

window.onload = () => {
    const rol = localStorage.getItem('rol');
    if (rol === 'AD') {
        document.getElementById('adminLinks')?.style.setProperty('display', 'block');
    }
};
