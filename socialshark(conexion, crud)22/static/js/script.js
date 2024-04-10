var settingsmenu = document.querySelector(".settings-menu");
var darkBtn = document.getElementById("dark-btn");

function settingsMenuToggle(){
    settingsmenu.classList.toggle("settings-menu-height");
}

darkBtn.onclick = function(){
    darkBtn.classList.toggle("dark-btn-on");
    document.body.classList.toggle("dark-theme");
}

function toggleOptionsMenu(id) {
    var menu = document.getElementById('options-menu-' + id);
    menu.style.display = (menu.style.display === 'none' || menu.style.display === '') ? 'block' : 'none';
}

function mostrarFormulario(id) {
    // Lógica para mostrar el formulario de edición
    document.getElementById('form_' + id).style.display = 'block';
}

function eliminarPublicacion(id) {
    // Lógica para eliminar la publicación
    // Debes enviar una solicitud al servidor para eliminar la publicación con el ID proporcionado
    // Por ejemplo, puedes usar AJAX para enviar una solicitud DELETE al servidor
}

function toggleOptionsMenu(id) {
    var menu = document.getElementById('options-menu-' + id);
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
}
