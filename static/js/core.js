var eliminando;

function cambiaRuta(ruta) {
    form = document.querySelector("form")
    form.action = ruta;
    eliminando   = false;
    if (ruta == "/usuario/administrar/delete" | ruta == "/usuario/administrar/update") {
        eliminando = true
    }
}

function confirmarBorrado() {
    if (eliminando) {
        let resp = confirm("¿ Esta seguro de proceder con los cambios📌?")
        return resp;
    }
    return true;    
}