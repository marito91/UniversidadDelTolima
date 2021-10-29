import hashlib, sqlite3
import os

from flask import Flask, jsonify, redirect, render_template, request, session, flash
from werkzeug.utils import escape 
from forms.formularios import Actividades, Asignaturas, Login, Registro, Notas, VerNotas, BuscarEstudiante, VerActividades, VerAsignaturas, Feedback, FeedbackEstudiante, updatePassword



app = Flask(__name__)
app.secret_key = os.urandom(20)



#---------------------------------------------- APIs INICIO Sesion ----------------------------------------------#
@app.route("/", methods=["GET", "POST"])
def index():


    frm = Login()
    
    if frm.validate_on_submit():
        
        username =escape(frm.username.data)
        password =escape(frm.password.data)
    
        # encriptar contraseña
        encrip=hashlib.sha256(password.encode())
        pass_enc=encrip.hexdigest()

        with sqlite3.connect("unitolima.db") as con:

            con.row_factory = sqlite3.Row
            # Crea un cursor para manipular la base de datos
            cursor = con.cursor()
            # Prepara la sentencia SQL
            cursor.execute("SELECT id_usuario, nombre, apellidos, numero_documento, password, perfil_id FROM usuario WHERE numero_documento = ? AND password = ?", [username, pass_enc])
            row = cursor.fetchone()
            if row:
               
                session["id_usuario"] = row["id_usuario"]
                session["activeSesion"]=True
                session["nombres"]= row["nombre"]+" "+row["apellidos"] # este tambien lo puedo utilizar para enviar el nombre - consultar sesiones varias
                perfil_id= row["perfil_id"]


                if perfil_id == "1":
                    
                    session["perfil"] = "Admin"
                    # typeUser="Admin"
                elif perfil_id == "2":
                    session["perfil"] = "Docente"
                    # typeUser="Docente"
                elif perfil_id == "3":
                    session["perfil"] = "Estudiante"
                    # typeUser="Estudiante"

                # print(session["perfil"] )    
            else:
                return render_template("index.html", frm=frm,estado="Usuario invalido, vuelva a ingresar datos correctos 🚨")

            
    
        
           
    
    if "id_usuario" in session: #si encuentra el usuario y se activa la sesion, le da ingreso al sistema
        return redirect("/inicio")

    else: # aqui es donde comenzaria
        return render_template("index.html", frm=frm, estado="Bienvenido, por favor ingrese su usuario y contraseña 🚀🌍")

# #---------------------------------------------- API LOGOUT / LOGIN -----------------------------------------------#

# Cierre sesion
@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()
    return render_template("logout.html")


# Ruta de inicio
@app.route("/inicio", methods=["GET"])
def inicio():

    
    if "id_usuario" in session:
        
        return render_template("inicio.html", UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------


# #--------------------------------------------- APIs REGISTROS Y USUARIOS --------------------------------#

# # Registro de usuarios 
@app.route("/usuario/administrar", methods=["GET", "POST"])
def administrar():
    
    if "id_usuario" in session and session["perfil"]=="Admin":
        frm = Registro()
        return render_template("administraccion_usuario.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html") 

# # Ruta para buscar usuarios 
@app.route("/usuario/administrar/get", methods=["GET", "POST"])
def get_usuario():
    frm = Registro()
    if "id_usuario" in session and session["perfil"]=="Admin":
        documento = frm.buscador.data
        # if frm.validate_on_submit:
        #     if frm.consulta:
        with sqlite3.connect("unitolima.db") as con:
            
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario WHERE numero_documento = ?", [documento])
            row = cursor.fetchone()
            
            if row:
                # print(row["numero_documento"])
                # frm.documento.data = int(row["numero_documento"])
                frm.nombres.data = row["nombre"]
                frm.apellidos.data = row["apellidos"]
                frm.tipoDocumento.data = row["tipo_documento"]
                frm.documento.data = int(documento)
                perfil = row["perfil_id"]
                if perfil == "1":
                    frm.perfil.data = "SUPERADMIN"
                elif perfil == "2":
                    frm.perfil.data = "DOCENTE"
                elif perfil == "3":
                    frm.perfil.data = "ESTUDIANTE"
                frm.direccion.data = row["direccion"]
                frm.departamento.data = row["departamento"]
                frm.ciudad.data = row["ciudad"]
                frm.telefono.data = row["telefono_fijo"]
                frm.celular.data = row["celular"]
                frm.email.data = row["email"]
                frm.observaciones.data = row["observaciones"]
            else:
                frm.nombres.data = ""
                frm.apellidos.data = ""
                frm.tipoDocumento.data = ""
                frm.documento.data = ""
                
                if frm.perfil.data == "ESTUDIANTE" or frm.perfil.data== "DOCENTE" or frm.perfil.data == "SUPERADMIN":
                    frm.perfil.data = ""
                # elif perfil == "2":
                #     frm.perfil.data = ""
                # elif perfil == "3":
                #     frm.perfil.data = ""
                frm.direccion.data = ""
                frm.departamento.data = ""
                frm.ciudad.data = ""
                frm.telefono.data = ""
                frm.celular.data = ""
                frm.email.data = ""
                frm.observaciones.data = ""
                flash("No se ha encontrado el usuario 🚧")
            
        return render_template("administraccion_usuario.html", frm=frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# # Ruta para registrar usuarios 
@app.route("/usuario/administrar/save", methods=["GET", "POST"])
def registro_usuario():
    frm = Registro()
    if "id_usuario" in session and session["perfil"]=="Admin":     
    
        # Se capturan los elementos del formulario
        #usuario = frm.usuario.data
        #id = frm.id.data
        doctype = frm.tipoDocumento.data
        documento = frm.buscador.data

        perfil = frm.perfil.data
        # Se asigna el perfil como Dios manda
        if frm.perfil.data == "SUPERADMIN":
            perfil = "1"
        elif frm.perfil.data == "DOCENTE":
            perfil = "2"
        elif frm.perfil.data == "ESTUDIANTE":
            perfil = "3"

        nombres = frm.nombres.data
        apellidos = frm.apellidos.data
        direccion = frm.direccion.data
        departamento = frm.departamento.data
        ciudad = frm.ciudad.data
        telefono = frm.telefono.data
        celular = frm.celular.data
        correo = frm.email.data
        observaciones = frm.observaciones.data
        password = str(frm.buscador.data)

        # if frm.guardar:
        #     # Cifrar contraseña
        encrp = hashlib.sha256(password.encode())
        pass_enc = encrp.hexdigest()
        # Conecta a base de datos
        with sqlite3.connect("unitolima.db") as con:
            # Crea un cursor para manipular la base de datos
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario WHERE numero_documento = ?", [documento])
            # Si existe un usuario
            if cursor.fetchone():
                flash ("Usuario ya se encuentra registrado")
            # Si no que guarde uno
            else:
                # Prepara la sentencia SQL
                cursor.execute("INSERT INTO usuario (nombre, apellidos, tipo_documento, numero_documento, direccion, departamento, ciudad, telefono_fijo, celular, email, observaciones, perfil_id, password, activo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [nombres, apellidos, doctype, documento, direccion, departamento, ciudad, telefono, celular, correo, observaciones, perfil, pass_enc, True]) # NO SE DEBE CONCATENAR NUNCA
                # Ejecuta la sentencia SQL
                con.commit()
                # Si el usuario es un estudiante, se va a agregar a la lista de asignaturas a espera de que se le asigne una materia
                if perfil == "3":
                    nombre = nombres + " " + apellidos
                    cursor2 = con.cursor()
                    cursor2.execute("SELECT id_usuario FROM usuario WHERE numero_documento = ?", [documento])
                    list = cursor2.fetchone()
                    id = list[0]
                    cursor3 = con.cursor()
                    cursor3.execute("INSERT INTO usuario_asignatura (nombre, perfil_id_fk, id_usuario) VALUES (?,?,?)", [nombre, perfil, id ])
                    con.commit()
                flash ("Guardado con exito ✔")
        return render_template("administraccion_usuario.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")    

# # Ruta para editar usuarios    
@app.route("/usuario/administrar/update", methods=["GET", "POST"])
def editar_usuario():

    frm = Registro()
    if "id_usuario" in session and session["perfil"]=="Admin":

        # if frm.validate_on_submit():
        # Se capturan los elementos del formulario
        #barra_busqueda = frm.buscador.data
        doctype = frm.tipoDocumento.data
        documento = frm.buscador.data

        perfil = frm.perfil.data
        # Se asigna el perfil como Dios manda
        if frm.perfil.data == "SUPERADMIN":
            perfil = "1"
        elif frm.perfil.data == "DOCENTE":
            perfil = "2"
        elif frm.perfil.data == "ESTUDIANTE":
            perfil = "3"

        nombres = frm.nombres.data
        apellidos = frm.apellidos.data
        direccion = frm.direccion.data
        departamento = frm.departamento.data
        ciudad = frm.ciudad.data
        telefono = frm.telefono.data
        celular = frm.celular.data
        correo = frm.email.data
        observaciones = frm.observaciones.data
        asignatura = frm.asignatura.data

        # if frm.editar:
        # print("actualizar")
        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("UPDATE usuario SET nombre = ?, apellidos = ?, tipo_documento = ?, numero_documento = ?, direccion = ?, departamento = ?, ciudad = ?, telefono_fijo = ?, celular = ?, email = ?, observaciones = ?, perfil_id = ? WHERE numero_documento = ? ", [nombres, apellidos, doctype, documento, direccion, departamento, ciudad, telefono, celular, correo, observaciones, perfil, documento])
            con.commit()
            if con.total_changes > 0:
                flash("Datos de usuario actualizados ✔")  
            else:
                flash("No se pudo editar el usuario 🚧")
            if asignatura != "":
                cursor2 = con.cursor()
                cursor2.execute("SELECT id_usuario FROM usuario WHERE numero_documento = ?", [documento])
                list = cursor2.fetchone()
                id = list[0]
                cursor3 = con.cursor()
                cursor3.execute("UPDATE usuario_asignatura SET asignatura_id = ? WHERE id_usuario = ? ", [asignatura, id])
                con.commit()

        return render_template("administraccion_usuario.html", frm=frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    
    else:
        return render_template("logout.html")

# # Ruta para ver usuarios en el caso del admin
@app.route("/usuario/ver", methods=["GET", "POST"])
def ver_usuario():
    frm = Registro()
    if "id_usuario" in session:
        documento = frm.documento.data
        if frm.validate_on_submit:
            if frm.consulta:
                with sqlite3.connect("unitolima.db") as con:
                    
                    con.row_factory = sqlite3.Row
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM usuario WHERE numero_documento = ?", [documento])
                    row = cursor.fetchone()
                    
                    if row:
                        frm.nombres.data = row["nombre"]
                        frm.apellidos.data = row["apellidos"]
                        frm.tipoDocumento.data = row["tipo_documento"]
                        # frm.documento.data = int(documento)
                        perfil = row["perfil_id"]
                        if perfil == "1":
                           frm.perfil.data = "SUPERADMIN"
                        elif perfil == "2":
                           frm.perfil.data = "DOCENTE"
                        elif perfil == "3":
                           frm.perfil.data = "ESTUDIANTE"
                        frm.direccion.data = row["direccion"]
                        frm.departamento.data = row["departamento"]
                        frm.ciudad.data = row["ciudad"]
                        frm.telefono.data = row["telefono_fijo"]
                        frm.celular.data = row["celular"]
                        frm.email.data = row["email"]
                        frm.observaciones.data = row["observaciones"]
                    else:
                        frm.nombres.data = ""
                        frm.apellidos.data = ""
                        frm.tipoDocumento.data = ""
                        frm.documento.data = ""
                        perfil = ""
                        if perfil == "1":
                            frm.perfil.data = ""
                        elif perfil == "2":
                            frm.perfil.data = ""
                        elif perfil == "3":
                            frm.perfil.data = ""
                        frm.direccion.data = ""
                        frm.departamento.data = ""
                        frm.ciudad.data = ""
                        frm.telefono.data = ""
                        frm.celular.data = ""
                        frm.email.data = ""
                        frm.observaciones.data = ""
                        flash("No se ha encontrado el usuario")
            
        return render_template("ver_usuario.html", frm=frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# Ruta para eliminar usuarios
@app.route("/usuario/administrar/delete", methods=["GET", "POST"])
def eliminarUser():
    
    if "id_usuario" in session and session["perfil"]=="Admin":
        frm = Registro()
        documento = frm.buscador.data
        with sqlite3.connect("unitolima.db") as con:
            # Crea un cursor para manipular la base de datos
            cursor = con.cursor()
            cursor.execute("DELETE FROM usuario WHERE numero_documento = ?", [documento])
            con.commit()
            if con.total_changes > 0:
                flash("Usuario eliminado")      
            else:
                frm.nombres.data = ""
                frm.apellidos.data = ""
                frm.tipoDocumento.data = ""
                frm.documento.data = ""
                perfil = ""
                if perfil == "1":
                    frm.perfil.data = ""
                elif perfil == "2":
                    frm.perfil.data = ""
                elif perfil == "3":
                    frm.perfil.data = ""
                frm.direccion.data = ""
                frm.departamento.data = ""
                frm.ciudad.data = ""
                frm.telefono.data = ""
                frm.celular.data = ""
                frm.email.data = ""
                frm.observaciones.data = ""
                flash("No se pudo eliminar el usuario")
        
        return render_template("administraccion_usuario.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"] )
    
    else:
        return render_template("logout.html")

# # Ruta para buscar usuarios
@app.route("/usuario/eliminar/get", methods=["GET", "POST"])
def buscarEliminar():
    if "id_usuario" in session:
        frm = Registro()
        documento = frm.buscador.data
        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario WHERE numero_documento = ?", [documento])
            row = cursor.fetchone()
            if row:
                frm.nombres.data = row["nombre"]
                frm.apellidos.data = row["apellidos"]
                frm.tipoDocumento.data = row["tipo_documento"]
                frm.documento.data = row["numero_documento"]
                perfil = row["perfil_id"]
                if perfil == "1":
                    frm.perfil.data = "SUPERADMIN"
                elif perfil == "2":
                    frm.perfil.data = "DOCENTE"
                elif perfil == "3":
                    frm.perfil.data = "ESTUDIANTE"
                frm.direccion.data = row["direccion"]
                frm.departamento.data = row["departamento"]
                frm.ciudad.data = row["ciudad"]
                frm.telefono.data = row["telefono_fijo"]
                frm.celular.data = row["celular"]
                frm.email.data = row["email"]
                frm.observaciones.data = row["observaciones"]
                flash("Usuario encontrado")
            else:
                frm.nombres.data = ""
                frm.apellidos.data = ""
                frm.tipoDocumento.data = ""
                frm.documento.data = ""
                perfil = ""
                if perfil == "1":
                    frm.perfil.data = ""
                elif perfil == "2":
                    frm.perfil.data = ""
                elif perfil == "3":
                    frm.perfil.data = ""
                frm.direccion.data = ""
                frm.departamento.data = ""
                frm.ciudad.data = ""
                frm.telefono.data = ""
                frm.celular.data = ""
                frm.email.data = ""
                frm.observaciones.data = ""
                flash("No se ha encontrado el usuario")

                
        return render_template("eliminar_usuario.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"] )
    else:
        return render_template("logout.html")

# Ruta para ver estudiantes para el caso del profesor
@app.route("/estudiante/ver", methods=["GET", "POST"])
def ver_estudiante():
    frm = Registro()
    if "id_usuario" in session : 
    
        documento = frm.documento.data
        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario WHERE numero_documento = ?", [documento])
            row = cursor.fetchone() 
            if row:
                frm.nombres.data = row["nombre"]
                frm.apellidos.data = row["apellidos"]
                frm.tipoDocumento.data = row["tipo_documento"]
                frm.documento.data = row["numero_documento"]
                perfil = row["perfil_id"]
                if perfil == "1":
                    frm.perfil.data = "SUPERADMIN"
                elif perfil == "2":
                    frm.perfil.data = "DOCENTE"
                elif perfil == "3":
                    frm.perfil.data = "ESTUDIANTE"
                frm.direccion.data = row["direccion"]
                frm.departamento.data = row["departamento"]
                frm.ciudad.data = row["ciudad"]
                frm.telefono.data = row["telefono_fijo"]
                frm.celular.data = row["celular"]
                frm.email.data = row["email"]
                frm.observaciones.data = row["observaciones"]
            else:
                frm.nombres.data = ""
                frm.apellidos.data = ""
                frm.tipoDocumento.data = ""
                frm.documento.data = ""
                perfil = ""
                if perfil == "1":
                    frm.perfil.data = ""
                elif perfil == "2":
                    frm.perfil.data = ""
                elif perfil == "3":
                    frm.perfil.data = ""
                frm.direccion.data = ""
                frm.departamento.data = ""
                frm.ciudad.data = ""
                frm.telefono.data = ""
                frm.celular.data = ""
                frm.email.data = ""
                frm.observaciones.data = ""
                flash("No se ha encontrado el usuario 🚧")
    
        return render_template("ver_usuario.html",frm=frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------


# #------------------------------------------ APIs ACTIVIDADES ------------------------------------------------------------------#

# # Ruta 1 crear actividad
@app.route("/actividad/registrar", methods=["GET", "POST"])
def crear_actividad():
    frm = Actividades()
    if "id_usuario" in session:
        if frm.validate_on_submit(): 
            id_actividad = frm.id_actividad.data
            nombre_actividad = frm.nombre_actividad.data
            id_asignatura_fk = frm.id_asignatura_fk.data   # de un listado me guarde el seleccionado
            instrucciones_actividad = frm.instrucciones_actividad.data
            tipo_actividad = frm.tipo_actividad.data
            if frm.registrar_actividad:
                if id_actividad != "1" and id_actividad != "2" and id_actividad != "3":
                    flash("ID de actividad inválido. Seleccione el número de la actividad (1, 2, 3)")
                else:                      
                    with sqlite3.connect("unitolima.db") as con:
                        # Crea un cursor para manipular la base de datos
                        cursor = con.cursor()
                        cursor.execute("SELECT * FROM actividad WHERE actividad_id = ? AND id_asignatura_fk = ?", [int(id_actividad), id_asignatura_fk])
                        # Si existe un la asignatura
                        if cursor.fetchone():
                            flash (f"La actividad {id_actividad} ya se encuentra registrada para la asignatura {id_asignatura_fk} en la base de datos.")
                        # Si no que guarde uno
                        else:
                            # Prepara la sentencia SQL
                            cursor.execute("INSERT INTO actividad (actividad_id, nombre_actividad, id_asignatura_fk, tipo_actividad, instrucciones_actividad) VALUES (?,?,?,?,?)", [int(id_actividad), nombre_actividad, id_asignatura_fk, tipo_actividad, instrucciones_actividad])
                            # Ejecuta la sentencia SQL
                            con.commit()
                            flash ("Guardado con exito")

        return render_template("crear_actividad.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
        

# # Ruta 2 detalle actividad
@app.route("/actividad/detalle", methods=["GET", "POST"])
def ver_actividad():
    frm = VerActividades()
    if "id_usuario" in session:
        id = frm.id_actividad.data
        asig = frm.id_asignatura_fk.data
        #if frm.validate_on_submit(): 
        if frm.consultar:
            with sqlite3.connect("unitolima.db") as con:
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute("SELECT * FROM actividad WHERE id_asignatura_fk = ? and actividad_id = ?", [asig, id])
                row = cursor.fetchone()
                print(row)
                if row:
                    frm.id_asignatura_fk.data = row["id_asignatura_fk"]
                    frm.instrucciones_actividad.data = row["instrucciones_actividad"]
                    frm.tipo_actividad.data = row["tipo_actividad"]
                    frm.nombre_actividad.data = row["nombre_actividad"]
                    flash("Actividad encontrada.")
                else:
                    frm.id_asignatura_fk.data = ""
                    frm.instrucciones_actividad.data = ""
                    frm.tipo_actividad.data = ""
                    frm.nombre_actividad.data = ""
                    flash("La actividad solicitada no fue encontrada.")
        
        return render_template("detalle_actividad.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#



# #------------------------------------------- APIs BUSCADOR ----------------------------------------------#

# # Ruta Buscar
@app.route("/buscador", methods=["GET", "POST"])
def buscar():
    frm = BuscarEstudiante()
    if "id_usuario" in session:
        codigo = frm.codigo.data
        # Se conecta a base de datos
        if frm.validate_on_submit():
            if frm.buscar:
                with sqlite3.connect("unitolima.db") as con:
                    con.row_factory = sqlite3.Row
                    cursor = con.cursor()
                    cursor2 = con.cursor()
                    cursor3 = con.cursor()
                    cursor4 = con.cursor()
                    cursor.execute("SELECT id_usuario, nombre, apellidos FROM usuario WHERE id_usuario = ?", [codigo])
                    cursor2.execute("SELECT nota_final, asignatura_id FROM nota WHERE usuario_id = ?", [codigo])
                    cursor3.execute("SELECT * FROM usuario WHERE id_usuario = ?", [codigo])
                    cursor4.execute("SELECT * FROM comentario WHERE usuario_id = ?", [codigo])
                    row = cursor.fetchone()
                    row2 = cursor2.fetchone()
                    row4 = cursor4.fetchone()
                    if row and row2:
                        frm.codigo.label = row[0]
                        frm.nombre.label = row[1] + " " + row[2]
                        frm.nota.label = str("{0:.2f}".format(row2[0]))
                        frm.asignatura.label = str(row2[1])
                        frm.retroalimentacion.label = row4[1]
                        flash("Usuario encontrado")
                    else:
                        flash(f"El usuario {codigo} no cuenta con una retroalimentación aún.")


        return render_template("buscador.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
    
# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#


# #---------------------------------------------- APIs NOTAS -----------------------------------------------#

# Ruta VER NOTAS
@app.route("/notas/visualizar", methods=["GET", "POST"])
def ver_notas():
    frm = VerNotas()
    if "id_usuario" in session:
        if frm.validate_on_submit():
            asignatura = frm.materias.data
            if asignatura == "":
                frm.a1.data = ""
                frm.n1.data = ""
                frm.a2.data = ""
                frm.n2.data = ""
                frm.a3.data = ""
                frm.n3.data = ""
                frm.notaFinal.data = ""
                frm.materias.label = ""
                flash("Por favor ingrese un ID de asignatura")
            else:
                with sqlite3.connect("unitolima.db") as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT actividad_id, tipo, valor_nota, asignatura_id FROM nota WHERE usuario_id = ?", [session["id_usuario"]])
                    #row = cursor.fetchone()
                    #rows = cursor.fetchall()
                    a = 0
                    b = 0
                    c = 0
                    for row in cursor.fetchall():               
                        if row:
                            if row[0] == 1:
                                frm.materias.label = row[3]
                                frm.a1.label = row[1]
                                frm.n1.label = row[2]
                                a = row[2]
                            if row[0] == 2:
                                frm.materias.label = row[3]
                                frm.a2.label = row[1]
                                frm.n2.label = row[2]
                                b = row[2]
                            if row[0] == 3:
                                frm.materias.label = row[3]
                                frm.a3.label = row[1]
                                frm.n3.label = row[2]
                                c = row[2]
                            elif row[0] != 1 and row[0] != 2 and row[0] != 3:
                                flash("No se encontraron calificaciones registradas")
                    promedio = (a+b+c)/3
                    frm.notaFinal.data = str("{0:.2f}".format(promedio))
                    

        return render_template("ver_notas.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# Ruta de los docentes para ver notas de los estudiantes y poner nota final
@app.route("/notas/visualizar/docente", methods=["GET", "POST"])
def ver_notas_docente():
    frm = VerNotas()
    if "id_usuario" in session:
        if frm.validate_on_submit():
            estudiante = frm.estudiantes.data
            if estudiante == "":
                frm.a1.data = ""
                frm.n1.data = ""
                frm.a2.data = ""
                frm.n2.data = ""
                frm.a3.data = ""
                frm.n3.data = ""
                frm.notaFinal.data = ""
                frm.estudiantes.label = "" #str(session["id_usuario"])
                flash("Por favor ingrese un ID de Estudiante")
            else:
                with sqlite3.connect("unitolima.db") as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT actividad_id, tipo, valor_nota, usuario_id FROM nota WHERE usuario_id = ?", [int(estudiante)])
                    cursorNombre = con.cursor()
                    cursorNombre.execute("SELECT nombre FROM usuario_asignatura WHERE id_usuario = ?", [int(estudiante)])
                    list = cursorNombre.fetchone()
                    if list != None:
                        nombre = list[0]
                        frm.estudiantes.label = nombre
                    else:
                        flash("Usuario no encontrado")
                    
                    a = 0
                    b = 0
                    c = 0
                    #frm.estudiantes.label = nombre
                    for row in cursor.fetchall():               
                        if row:
                            if row[0] == 1:
                                #frm.estudiantes.label = nombre
                                frm.a1.label = row[1]
                                frm.n1.label = row[2]
                                a = row[2]
                            if row[0] == 2:
                                #frm.estudiantes.label = nombre
                                frm.a2.label = row[1]
                                frm.n2.label = row[2]
                                b = row[2]
                            if row[0] == 3:
                                #frm.estudiantes.label = nombre
                                frm.a3.label = row[1]
                                frm.n3.label= row[2]
                                c = row[2]
                            elif row[0] != 1 and row[0] != 2 and row[0] != 3:
                                flash("No se encontraron calificaciones registradas")
                    promedio = (a+b+c)/3
                    frm.notaFinal.data = str("{0:.2f}".format(promedio))

                    # Prepara sentencia para asignar nota final al estudiante
                    cursor.execute("UPDATE nota SET nota_final = ? WHERE usuario_id = ?", [promedio, int(estudiante)])
                    con.commit()
                    

        return render_template("ver_notas_docente.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# Ruta INGRESAR NOTAS
@app.route("/notas/ingresar", methods=["GET", "POST"])
def notas():
    frm = Notas() 
    if "id_usuario" in session: 
        if frm.validate_on_submit():
            asignatura = frm.codigo.data
            usuario = frm.estudiante.data
            actividad = frm.actividad.data
            tipo = frm.tipo.data
            nota = frm.nota.data


            if frm.ingresar:
                # Conecta a base de datos
                with sqlite3.connect("unitolima.db") as con:
                    # Crea un cursor para manipular la base de datos
                    cursor = con.cursor()
                    cursor2 = con.cursor()
                    cursor3 = con.cursor()
                    # Se preparan las sentencias
                    cursor3.execute("SELECT id_usuario FROM usuario WHERE id_usuario = ? AND perfil_id = ?", [int(usuario), "3"])
                    cursor2.execute("SELECT * FROM asignatura WHERE id_asignatura = ?", [asignatura])
                    cursor.execute("SELECT * FROM nota WHERE usuario_id = ? AND actividad_id = ?", [int(usuario), int(actividad)])
                    list = cursor3.fetchone()
                    if list != None:
                        id = list[0]
                        print(id) #Revision de funcionamiento
                    else:
                        flash("Usuario no encontrado")

                    # Si existe el usuario
                    if list != None:
                        # Si existe la asignatura
                        if cursor2.fetchone():
                            # Si el usuario ya tiene registrada la actividad.
                            if cursor.fetchone():
                                flash ("El estudiante ya cuenta con una calificación para esta actividad.")
                            # Si no que guarde la calificación
                            else:
                                # Prepara la sentencia SQL
                                cursor.execute("INSERT INTO nota (usuario_id, actividad_id, valor_nota, asignatura_id, tipo) VALUES (?,?,?,?,?)", [id, int(actividad), float(nota), int(asignatura), tipo])
                                # Ejecuta la sentencia SQL
                                con.commit()
                                flash ("Calificación guardada con éxito")
                        else:
                            flash ("Esta asignatura no existe.")
                    else:
                        flash(f"El usuario {usuario} no se encuentra registrado o no figura como estudiante.")

        return render_template("ingresar_notas.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#


# #---------------------------------------------- APIs ASIGNATURAS -----------------------------------------------#

# # Ruta 1 - Atterizaje para administrar asignaturas
@app.route("/asignaturas/administracion", methods=["GET", "POST"])
def administrar_asignatura():
    if "id_usuario" in session:
        
        frm = Asignaturas()    
        return render_template ("registrar_asignaturas_superadmin.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# # Ruta 2 - Ver asignaturas (Dentro de administrar)
@app.route("/asignaturas/get", methods=["GET", "POST"])
def buscar_asignatura():
    if "id_usuario" in session:
        frm = Asignaturas()
        codigo = frm.codigo.data
        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM asignatura WHERE id_asignatura = ?", [codigo])
            row = cursor.fetchone()
            if row:
                frm.asignatura.data = row["nombre_asignatura"]
                frm.tipo.data = row["tipo"]
                frm.descripcion.data = row["descripcion"]

                
                flash("Asignatura encontrada")
            else:
                frm.asignatura.data = ""
                frm.tipo.data = ""
                frm.descripcion.data =""
                flash("No se ha encontrado la asignatura")

        
            
        return render_template ("registrar_asignaturas_superadmin.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# # Ruta 3 - Registrar asignaturas
@app.route("/asignaturas/registrar", methods=["GET", "POST"])
def registrar_asignatura():
    if "id_usuario" in session:
        frm = Asignaturas()
        codigo = frm.codigo.data
        asignatura=frm.asignatura.data
        tipo=frm.tipo.data
        descripcion=frm.descripcion.data

        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("INSERT INTO asignatura (id_asignatura, nombre_asignatura, tipo, descripcion) VALUES (?,?,?,?)", [codigo, asignatura, tipo, descripcion])  
            # row = cursor.fetchone()
            if con.total_changes>0:
                flash("Asignatura registrada")
            else:
                flash("No se ha registrado la asignatura")

        
            
        return render_template ("registrar_asignaturas_superadmin.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# # Ruta 4 - Editar Asignaturas
@app.route("/asignaturas/editar", methods=["GET", "POST"])
def editar_asignatura():
    if "id_usuario" in session:
        frm=Asignaturas()
        codigo= escape(frm.codigo.data)
        asignatura=escape(frm.asignatura.data)
        tipo=escape(frm.tipo.data)
        descripcion=escape(frm.descripcion.data) 
            
        with sqlite3.connect("unitolima.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE asignatura SET nombre_asignatura= ?, tipo= ?, descripcion=? WHERE id_asignatura= ?",[asignatura,tipo,descripcion,codigo])
            con.commit()
            if con.total_changes>0:
                flash("asignatura actualizado")
            else:
                flash("no se pudo actualizar")



        return render_template("registrar_asignaturas_superadmin.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"] )
    else:
        return render_template("logout.html")

# # Ruta 5 - Eliminar Asignaturas
@app.route("/asignaturas/eliminar", methods=["GET", "POST"])
def eliminar_asignatura():
    if "id_usuario" in session:
        frm = Asignaturas()
        codigo = frm.codigo.data
        with sqlite3.connect("unitolima.db") as con:
            # Crea un cursor para manipular la base de datos
            cursor = con.cursor()
            cursor.execute("DELETE FROM asignatura WHERE id_asignatura = ?", [codigo])
            con.commit()
            if con.total_changes > 0:
                flash("Asignatura eliminada")      
            else:
                flash("No se pudo eliminar la asignatura")


        return render_template("registrar_asignaturas_superadmin.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# # Ruta 6 - Ver Asignaturas (Pestaña especializada para estudiantes y docentes)
@app.route("/asignaturas/vertodos", methods=["GET", "POST"])
def ver_asignatura():
    if "id_usuario" in session:
        frm = VerAsignaturas()
        if frm.validate_on_submit():
            codigo = frm.codigo.data
            usuarios = []
            with sqlite3.connect("unitolima.db") as con:
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor2 = con.cursor()
                cursor.execute("SELECT * FROM asignatura WHERE id_asignatura = ?", [codigo])
                cursor2.execute("SELECT nombre FROM usuario_asignatura WHERE asignatura_id = ?", [codigo])
                row = cursor.fetchone()
                row2 = cursor2.fetchall()
                for user in row2:
                    for i in user:
                        usuarios.append(i)
                print(usuarios)
                if row:
                    frm.asignatura.data = row["nombre_asignatura"]
                    frm.tipo.data = row["tipo"]
                    frm.descripcion.data = row["descripcion"]
                    for i in usuarios:
                        frm.estudiantes.data += i + ", "
                    flash("Asignatura encontrada")
                else:
                    frm.asignatura.data = ""
                    frm.tipo.data = ""
                    frm.descripcion.data =""
                    frm.estudiantes.data =""
                    flash("No se ha encontrado la asignatura")

        return render_template("ver_asignaturas.html", frm = frm ,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
    
# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#


#------------------------------------------ APIs FEEDBACK ---------------------------------------------#

# Ruta para retroalimentacion para docentes
@app.route("/feedback/docente", methods=["GET", "POST"])
def feedback_teacher():
    if "id_usuario" in session:
        frm = Feedback()
        if frm.validate_on_submit():
            asignatura = frm.asignatura.data
            actividad = frm.actividad.data
            estudiante = frm.estudiante.data
            feedback = frm.feedback.data

            if frm.guardar:
                # Conecta a base de datos
                with sqlite3.connect("unitolima.db") as con:
                    # Crea un cursor para manipular la base de datos
                    cursor = con.cursor()
                    # Se preparan las sentencias
                    cursor.execute("SELECT descripcion FROM comentario WHERE usuario_id = ? AND actividad_id = ? AND asignatura_id = ?", [estudiante, actividad, asignatura])                  
                    # Si el usuario ya tiene registrada la actividad.
                    if cursor.fetchone():
                        flash ("El estudiante ya cuenta con una retroalimentación para esta actividad.")
                    # Si no que guarde la calificación
                    else:
                        # Prepara la sentencia SQL
                        cursor.execute("INSERT INTO comentario (usuario_id, actividad_id, asignatura_id, descripcion) VALUES (?,?,?,?)", [estudiante, actividad, asignatura, feedback])
                        # Ejecuta la sentencia SQL
                        con.commit()
                        flash ("Comentario guardado con éxito.")

        return render_template("retroalimentacion_docente.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# Ruta para retroalimentacion estudiante
@app.route("/feedback/estudiante", methods=["GET", "POST"])
def feedback_student():
    if "id_usuario" in session:
        frm = FeedbackEstudiante()
        if frm.validate_on_submit():
            asignatura = frm.asignatura.data
            

            if frm.ver:
                # Conecta a base de datos
                with sqlite3.connect("unitolima.db") as con:
                    # Crea un cursor para manipular la base de datos
                    cursor = con.cursor()
                    # Se preparan las sentencias
                    cursor.execute("SELECT actividad_id, descripcion, nombre_actividad, id_comentario FROM comentario WHERE asignatura_id = ? AND usuario_id = ?", [asignatura, session["id_usuario"]])                  
                    for row in cursor.fetchall():               
                            if row:
                                if row[0] == 1:
                                    frm.a1.label = row[2]
                                    frm.f1.label = row[1]
                                if row[0] == 2:
                                    frm.a2.label = row[2]
                                    frm.f2.label = row[1]
                                if row[0] == 3:
                                    frm.a3.label = row[2]
                                    frm.f3.label = row[1]
                                elif row[0] != 1 and row[0] != 2 and row[0] != 3:
                                    flash("No se encontraron comentarios registrados")

        return render_template("retroalimentacion_estudiante.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------ APIs OTROS ---------------------------------------------#

# # Ruta para ver datos de la persona que inicio sesion
@app.route("/misdatos", methods=["GET"])
def misdatos():

    if "id_usuario" in session:
        
        sinAsignatura = "Sin asignatura"

        with sqlite3.connect("unitolima.db") as con:
            
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", [session["id_usuario"]])

            cursorAsignatura = con.cursor()
            cursorAsignatura.execute("SELECT asignatura_id FROM usuario_asignatura WHERE id_usuario = ?", [session["id_usuario"]])
            id_asignatura = cursorAsignatura.fetchone()
            if id_asignatura != None:
                id = id_asignatura[0]
                cursorNombre = con.cursor()
                cursorNombre.execute("SELECT nombre_asignatura FROM asignatura WHERE id_asignatura = ?", [id])
                rowAsignatura = cursorNombre.fetchone()
                if rowAsignatura != None:
                    asignatura = rowAsignatura[0]
                else:
                    asignatura = sinAsignatura
            else:
                asignatura = sinAsignatura

            
            
            row = cursor.fetchone()
            
 
            tipoDocumento = "CC"

            documento = str(row["numero_documento"])

            ciudad = row["ciudad"]

            celular= row["celular"]

            email= row["email"]

            


        return render_template("misdatos.html",UserName=session["nombres"],
        TypeUser=session["perfil"],
        ActiveSesion=session["activeSesion"],
        tipo_documento=tipoDocumento,
        documento=documento,
        celular=celular,
        correo=email,
        ciudad=ciudad,
        inscrito=asignatura
         )
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------#

# # Ruta para ver datos de la persona que inicio sesion
@app.route("/misdatos/password", methods=["GET","POST"])
def updatePass():
    # frm=updatePassword()
    if "id_usuario" in session:
   
        frm=updatePassword()
        if frm.validate_on_submit():
            passViejo=frm.password.data
            passnew1=frm.passwordNew1.data
            passnew2=frm.passwordNew2.data
            iduser=int(session["id_usuario"])
            print( iduser, type(iduser))
            print( session["id_usuario"], type(session["id_usuario"]))
            # print(passnew1)
            # print(passnew2)
            if passnew1 == passnew2:

                encrip=hashlib.sha256(passViejo.encode())
                pass_enc=encrip.hexdigest()
                with sqlite3.connect("unitolima.db") as con:
                    con.row_factory = sqlite3.Row
                    cursor = con.cursor()
                    cursor.execute("SELECT password FROM usuario WHERE id_usuario = ?",[iduser])
                        #                cursor2.execute("SELECT usuario_id FROM nota WHERE asignatura_id = ?", [codigo])
                        #                row2 = cursor2.fetchone()
                        #                cursor3.execute("SELECT nombre, apellidos FROM usuario WHERE id_usuario = ?", [row2])
                    row = cursor.fetchone()
                        #                row3 = cursor3.fetchall()
                    
                    if row["password"] == pass_enc:
                        encripNew=hashlib.sha256(passnew2.encode())
                        passNewEncrip=encripNew.hexdigest()
                        cursor2 = con.cursor()
                        cursor2.execute("UPDATE usuario SET password = ? WHERE  id_usuario = ? ", [passNewEncrip,iduser])
                        con.commit()
                        if con.total_changes > 0:
                            flash("contraseña cambiada satisfactoriamente ✔🔐")  
                        else:
                            flash("No se pudo cambiar la contraseña 🔒")

                    else:
                        
                        flash("Contraseña ingresada no es correcta 🔒")
            else:
                flash("revisar contraseña nueva, no coinciden 🔒")


        
        return render_template("update_password.html",frm=frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------#        

if __name__=="__main__":
    app.run(debug=True)


