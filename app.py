from flask import Flask, render_template, redirect, request
# PRUEBA
app = Flask(__name__)


lista_usuarios = ["Carlos", "Mario", "Julian", "Amaury", "Daniel"]
lista_actividades = {
    1: "Algoritmos",
    2: "Condicionales",
    3: "Ciclos",
    4: "Bases de datos",
    5: "Desarrollo de Apps/Web",
    6: "Proyecto Full Stack"
}
lista_asignaturas = {
    "FU":"Fundamentos de Programacion",
    "PB":"Programacion Basica",
    "DS":"Desarrollo de Software"
}

    
loggedin = False

#---------------------------------------------- API INICIO ----------------------------------------------#
@app.route("/", methods=["GET"])
@app.route("/inicio", methods=["GET"])
def inicio():
    # Si el usuario ya inicio sesion entonces --> Vista principal
    #Sino --> Bienvenida
    return render_template("inicio.html", loggedin=loggedin)
#--------------------------------------------------------------------------------------------------------#


#---------------------------------------------- API LOGIN -----------------------------------------------#
# Entrada
@app.route("/login", methods=["GET", "POST"])
def login():
    global loggedin
    if request.method == "GET":
        return render_template("index.html")
    else:
        loggedin = True
        return redirect("/dashboard")


# Salida
@app.route("/logout", methods=["GET", "POST"])
def logout():
    loggedin = False
    return redirect("/login")
#--------------------------------------------------------------------------------------------------------#

#--------------------------------------------- API REGISTRO ---------------------------------------------#
@app.route("/registro", methods=["GET", "POST"])
def registro():
    return render_template("registro.html")
#--------------------------------------------------------------------------------------------------------#


#------------------------------------------- APIs DASHBOARD ---------------------------------------------#
@app.route("/dashboard", methods=["GET", "POST"])
def user_info():
    return render_template("dashboard.html") 
#--------------------------------------------------------------------------------------------------------#


#------------------------------------------ APIs ACTIVIDADES ---------------------------------------------#
# Ruta 1
@app.route("/actividad", methods=["GET", "POST"])
def crear_actividad():
    return render_template("crear_actividad.html")

# Ruta 2
@app.route("/actividad/detalle", methods=["GET", "POST"])
def actividad_detalle():
    return render_template("detalle_actividad.html")
#--------------------------------------------------------------------------------------------------------#


#------------------------------------------- APIs BUSCADOR ----------------------------------------------#
# Ruta 1
@app.route("/buscador/<id_usuario>", methods=["GET"])
def buscar(id_usuario):
    if id_usuario == "superadmin":
        return render_template("superadmin_buscar.html")
    else:
        return render_template("docente_buscar.html")
#--------------------------------------------------------------------------------------------------------#


#---------------------------------------------- APIs NOTAS -----------------------------------------------#
# Ruta 1
@app.route("/notas/visualizar", methods=["GET", "POST"])
def ver_notas():
    return render_template("ver_notas.html")

# Ruta 2
@app.route("/notas/ingresar", methods=["GET", "POST"])
def notas():
    return render_template("ingresar_notas.html")
#--------------------------------------------------------------------------------------------------------#


#------------------------------------------ APIs FEEDBACK ---------------------------------------------#
# Ruta 1
@app.route("/feedback/estudiante", methods=["GET"])
def feedback_student():
    return render_template("retroalimentacion_estudiante.html")

# Ruta 2
@app.route("/feedback/docente", methods=["GET","POST"])
def feedback_docente():
    return render_template("retroalimentacion_docente.html")
#--------------------------------------------------------------------------------------------------------#


if __name__=="__main__":
    app.run(debug=True)






#    try:
#        id_actividad = int(id_actividad)
#    except Exception as e:
#        id_actividad = 0
#    if id_actividad in lista_actividades:
#        return f"Estas viendo la actividad: {id_actividad}" #Se despliega la info de la actividad llamada
#    else:
#        return f"La actividad ({id_actividad}) no existe"