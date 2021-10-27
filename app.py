import hashlib, sqlite3
import os

from flask import Flask, jsonify, redirect, render_template, request, session, flash
from werkzeug.utils import escape 
from forms.formularios import Actividades, Asignaturas, Login, Registro, Notas



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
            
        return render_template("administraccion_usuario.html", frm=frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

@app.route("/usuario/administrar/save", methods=["GET", "POST"])
def registro_usuario():
    frm = Registro()
    if "id_usuario" in session and session["perfil"]=="Admin":     
    
        # Se capturan los elementos del formulario
        #usuario = frm.usuario.data
        #id = frm.id.data
        doctype = frm.tipoDocumento.data
        documento = frm.documento.data

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
        password = str(frm.documento.data)

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
                flash ("Guardado con exito ✔")
        return render_template("administraccion_usuario.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")    
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Ruta para editar usuarios    
@app.route("/usuario/update", methods=["GET", "POST"])
def editar_usuario():

    frm = Registro()
    if "id_usuario" in session and session["perfil"]=="Admin":

        # if frm.validate_on_submit():
        # Se capturan los elementos del formulario
        #barra_busqueda = frm.buscador.data
        doctype = frm.tipoDocumento.data
        documento = frm.documento.data

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

        # if frm.editar:
        # print("actualizar")
        with sqlite3.connect("unitolima.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("UPDATE usuario SET nombre = ?, apellidos = ?, tipo_documento = ?, numero_documento = ?, direccion = ?, departamento = ?, ciudad = ?, telefono_fijo = ?, celular = ?, email = ?, observaciones = ?, perfil_id = ? WHERE numero_documento = ? ", [nombres, apellidos, doctype, documento, direccion, departamento, ciudad, telefono, celular, correo, observaciones, perfil, documento])
            con.commit()
            if con.total_changes > 0:
                flash("Usuario editado")  
            else:
                flash("No se pudo editar el usuario")

        return render_template("administraccion_usuario.html", frm=frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    
    else:
        return render_template("logout.html")

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
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




# # Ruta para eliminar usuarios


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
                flash("No se pudo eliminar el usuario")
        
        return render_template("administraccion_usuario.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"] )
    
    else:
        return render_template("logout.html")


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

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Ruta para ver usuarios en el caso del profesor
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


# #------------------------------------------- APIs DASHBOARD ---------------------------------------------#
# #@app.route("/dashboard", methods=["GET", "POST"])
# #def user_info():
# #    return render_template("dashboard.html") 
# #--------------------------------------------------------------------------------------------------------#


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
            #fecha_actividad = frm.fecha_actividad.data
            # print(id_actividad + nombre_actividad + id_asignatura_fk + tipo_actividad + instrucciones_actividad)
            # estudiantes = frm.estudiantes.data
            # docente = frm.docente.data
            # tipo_nota = frm.tipo_nota.data
            # nota_final_actividad = frm.nota_final_actividad.data
            # nota_final_asignatura = frm.nota_final_asignatura.data
            if frm.registrar_actividad:
                with sqlite3.connect("unitolima.db") as con:
                    # Crea un cursor para manipular la base de datos
                    cursor = con.cursor()
                        # Si existe un usuario
                    if cursor.fetchone():
                        flash ("La actividad se encuentra registrada")
                    # Si no que guarde uno
                    else:
                        # Prepara la sentencia SQL
                        cursor.execute("INSERT INTO actividad (id_actividad, nombre_actividad, id_asignatura_fk, tipo_actividad, instrucciones_actividad) VALUES (?,?,?,?,?)", [id_actividad, nombre_actividad, id_asignatura_fk, tipo_actividad, instrucciones_actividad])
                        # Ejecuta la sentencia SQL
                        con.commit()
                        flash ("Guardado con exito")

        return render_template("crear_actividad.html", frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
        

# # Ruta 2 detalle actividad
@app.route("/actividad/detalle", methods=["GET", "POST"])
def ver_actividad():
    frm = Actividades()
    if "id_usuario" in session:
        #if frm.validate_on_submit(): 
        id_actividad = frm.id_actividad.data
        if frm.consultar_actividad:
            with sqlite3.connect("unitolima.db") as con:
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute("SELECT * FROM actividad WHERE id_actividad = ?", [id_actividad])
                row = cursor.fetchone()
                if row:
                    frm.id_asignatura_fk.data = row["id_asignatura_fk"]
                    frm.instrucciones_actividad.data = row["instrucciones_actividad"]
                    frm.tipo_actividad.data = row["tipo_actividad"]
                    frm.nombre_actividad.data = row["nombre_actividad"]
                    # frm.fecha_actividad.data = row["fecha_actividad"]
                    print(id_actividad)
                else:
                    frm.id_asignatura_fk.data = ""
                    frm.instrucciones_actividad.data = ""
                    frm.tipo_actividad.data = ""
                    frm.nombre_actividad.data = ""
                    # frm.fecha_actividad.data = ""
        
        return render_template("detalle_actividad.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------------------------------------------------------------#



# #------------------------------------------- APIs BUSCADOR ----------------------------------------------#
# # Ruta 1
@app.route("/buscador", methods=["GET", "POST"])
def buscar():
    if "id_usuario" in session:
        
        return render_template("buscador.html",UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
    

# #--------------------------------------------------------------------------------------------------------#


# #---------------------------------------------- APIs NOTAS -----------------------------------------------#
# Ruta VER NOTAS
@app.route("/notas/visualizar", methods=["GET", "POST"])
def ver_notas():
    frm = Notas() 
    if "id_usuario" in session:
        if frm.validate_on_submit():
            asignatura = frm.materias.data
            with sqlite3.connect("unitolima.db") as con:
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute("SELECT * FROM nota WHERE asignatura_id = ?", [int(asignatura)])
                row = cursor.fetchone()
                if row["actividad_id"] == 1:
                    frm.a1.data = str(row["actividad_id"])
                    frm.n1.data = str(row["valor_nota"])
                if row["actividad_id"] == 2:
                    frm.a2.data = row["actividad_id"]
                    frm.n2.data = str(row["valor_nota"])
                if row["actividad_id"] == 3:
                    frm.a3.data = row["actividad_id"]
                    frm.n3.data = str(row["valor_nota"])
                elif row["actividad_id"] != 1 and row["actividad_id"] != 2 and row["actividad_id"] != 3:
                    flash("No se encontraron calificaciones registradas")

        return render_template("ver_notas.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
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
                    cursor.execute("SELECT * FROM nota WHERE usuario_id = ? AND actividad_id = ?", [int(usuario), int(actividad)])
                    # Si existe un usuario
                    if cursor.fetchone():
                        flash ("El estudiante ya cuenta con una calificación para esta actividad")
                    # Si no que guarde la calificación
                    else:
                        # Prepara la sentencia SQL
                        cursor.execute("INSERT INTO nota (usuario_id, actividad_id, valor_nota, asignatura_id, tipo) VALUES (?,?,?,?,?)", [int(usuario), int(actividad), float(nota), int(asignatura), tipo])
                        # Ejecuta la sentencia SQL
                        con.commit()
                        flash ("Calificación guardada con éxito")
        return render_template("ingresar_notas.html",frm = frm, UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------#


# #---------------------------------------------- APIs ASIGNATURAS -----------------------------------------------#

# # Ruta 1 - Registrar asignaturas
@app.route("/asignaturas/administracion", methods=["GET", "POST"])
def administrar_asignatura():
    if "id_usuario" in session:
        
        frm = Asignaturas()    
        return render_template ("registrar_asignaturas_superadmin.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")

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
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            cursor.execute("INSERT INTO asignatura (nombre_asignatura, tipo, descripcion ) VALUES (?,?,?)", [asignatura, tipo, descripcion])  
            # row = cursor.fetchone()
            if con.total_changes>0:
                flash("Asignatura registrada")
            else:
                flash("No se ha registrado la asignatura")

        
            
        return render_template ("registrar_asignaturas_superadmin.html", frm = frm,UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# # Ruta 2 - Editar Asignaturas
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

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Ruta 3 - Eliminar Asignaturas
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

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------

# # Ruta 4 - Ver Asignaturas
@app.route("/asignaturas/vertodos", methods=["GET", "POST"])
def ver_asignatura():
    if "id_usuario" in session:
        return render_template("ver_asignaturas.html",UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
    



# #--------------------------------------------------------------------------------------------------------#


# #------------------------------------------ APIs FEEDBACK ---------------------------------------------#
# # Ruta para retroalimentacion para docentes
@app.route("/feedback/docente", methods=["GET"])
def feedback_teacher():

    if "id_usuario" in session:
        return render_template("retroalimentacion_docente.html",UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------#
# # Ruta para retroalimentacion estudiante
@app.route("/feedback/estudiante", methods=["GET"])
def feedback_student():

    if "id_usuario" in session:
        return render_template("retroalimentacion_estudiante.html",UserName=session["nombres"],TypeUser=session["perfil"], ActiveSesion=session["activeSesion"])
    else:
        return render_template("logout.html")
# #--------------------------------------------------------------------------------------------------------#


if __name__=="__main__":
    app.run(debug=True)


