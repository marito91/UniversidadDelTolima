var eliminando;

function cambiaRuta(ruta) {
    form = document.querySelector("form")
    form.action = ruta;
    eliminando   = false;
    if (ruta == "/usuario/eliminar/delete") {
        eliminando = true
    }
}

function confirmarBorrado() {
    if (eliminando) {
        let resp = confirm("Desea eliminar el registro?")
        return resp;
    }
    return true;    
}