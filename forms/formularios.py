from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField, SelectField, DateTimeField, DecimalField 
from wtforms.validators import DataRequired 


class Login(FlaskForm):
    username = IntegerField("Identificación 👥", validators = [DataRequired("Por favor llene este campo con numeros")])
    password = PasswordField("  Password  🔑", validators = [DataRequired("Por favor llene este campo")])
    entrar = SubmitField("Entrar 📡")



class Registro(FlaskForm):
    nombres = StringField("Nombres")
    apellidos = StringField("Apellidos")
    tipoDocumento = SelectField("Tipo de Documento*", choices=["","CC", "CE", "NIT"])
    documento = IntegerField("Documento")
    perfil = SelectField("Perfil", choices=["","ESTUDIANTE", "DOCENTE", "SUPERADMIN"])
    direccion = StringField("Direccion")
    departamento = SelectField("Departamento*", choices=["","AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLANTICO", "BOGOTA D.C.", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO", "CORDOBA", "CUNDINAMARCA", "GUAINIA", "GUAVIARE", "HUILA", "LA GUAJIRA", "MAGDALENA", "META", "N. DE SANTANDER", "NARINO", "PUTUMAYO", "QUINDIO", "RISARALDA", "SAN ANDRES Y P.", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "VAUPES", "VICHADA"])
    ciudad = SelectField("Ciudad", choices=["","IBAGUE", "BARRANQUILLA", "CARTAGENA", "CALI"])
    telefono = StringField("Telefono")
    celular = StringField("Celular")
    email = StringField("Email")
    observaciones = TextAreaField("Observaciones")
    buscador = IntegerField("Buscador")
    guardar = SubmitField("Registrar 💾", render_kw=({"onfocus":"cambiaRuta('/usuario/administrar/save')"}))
    eliminar = SubmitField("Eliminar 🗑",render_kw=({"onfocus":"cambiaRuta('/usuario/administrar/delete')"}))
    editar = SubmitField("Editar ✏",render_kw=({"onfocus":"cambiaRuta('/usuario/administrar/update')"}))
    buscar = SubmitField("Buscar 🔎",render_kw=({"onfocus":"cambiaRuta('/usuario/administrar/get')"}))
    consulta=SubmitField("Consultar 🔎")

class VerUsuario(FlaskForm):
    nombres = StringField("Nombres")
    apellidos = StringField("Apellidos")
    tipoDocumento = SelectField("Tipo de Documento*")
    documento = IntegerField("Documento")
    perfil = StringField("Perfil")
    direccion = StringField("Direccion")
    departamento = StringField("Departamento")
    ciudad = StringField("Ciudad")
    telefono = StringField("Telefono")
    celular = StringField("Celular")
    email = StringField("Email")
    observaciones = TextAreaField("Observaciones")
    buscador = IntegerField("Buscador")
    eliminar = SubmitField("Eliminar")

    
    

class Notas(FlaskForm):
    codigo = StringField("Codigo", validators = [DataRequired()])
    estudiante = StringField("Estudiante", validators = [DataRequired()])
    actividad = StringField("Actividad", validators = [DataRequired()])
    tipo = SelectField("Tipo Nota", choices=["Ejercicio Practico", "Trabajo Escrito", "Examen"])
    nota = StringField("Nota")
    notaAsignatura = DecimalField("Nota Asignatura")
    ingresar = SubmitField("Ingresar")#, render_kw=({"onfocus":"cambiaRuta('/notas/ingresar')"}))
    

class VerNotas(FlaskForm):
    materias = StringField("Asignatura")
    estudiantes = StringField("Estudiante")
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiaRuta('/notas/visualizar')"}))
    consultarEstudiante = SubmitField("Consultar", render_kw=({"onfocus":"cambiaRuta('/notas/visualizar/docente')"}))
    a1 = StringField("Actividad 1")
    a2 = StringField("Actividad 2")
    a3 = StringField("Actividad 3")
    n1 = StringField("Nota 1")
    n2 = StringField("Nota 2")
    n3 = StringField("Nota 3")
    notaFinal = StringField("Nota Final")


class Asignaturas(FlaskForm):
    codigo = IntegerField("Codigo")
    asignatura = StringField("Nombre de asignatura" )
    tipo = SelectField("Tipo de Asignatura", choices=["Por definir","ELECTIVA", "FORMACION BASICA", "OBLIGATORIA", "PRACTICAS", "OTRO"], validators = [DataRequired("Por favor llene este campo")])
    descripcion = TextAreaField("Descripción de la asignatura") #Usar un place holder para indicar descripción
    registrar = SubmitField('Registrar 💾',render_kw=({"onfocus":"cambiaRuta('/asignaturas/registrar')"}))
    buscar = SubmitField('Buscar 🔎',render_kw=({"onfocus":"cambiaRuta('/asignaturas/get')"}))
    eliminar = SubmitField('Eliminar 🗑',render_kw=({"onfocus":"cambiaRuta('/asignaturas/eliminar')"}))
    editar = SubmitField("Actualizar ✏",render_kw=({"onfocus":"cambiaRuta('/asignaturas/editar')"}))


class Actividades(FlaskForm):
    id_actividad = StringField("ID actividad*", validators = [DataRequired("Por favor llene este campo")])
    tipo_actividad = SelectField("Tipo de Actividad", choices=["Ejercicio Practico", "Trabajo Escrito", "Examen"], validators = [DataRequired("Por favor llene este campo")])
    nombre_actividad = StringField("Nombre Actividad*", validators = [DataRequired("Por favor llene este campo")])
    id_asignatura_fk = StringField("ID Asignatura*", validators = [DataRequired("Por favor llene este campo")])#,choices=["1","2","3"])
    fecha_actividad = DateTimeField("Fecha de Entrega")
    instrucciones_actividad = TextAreaField("Instrucciones")
    registrar_actividad = SubmitField("Registrar")  # OJO - falta adicionar botón registrar en menu Registrar actividades
    consultar_actividad = SubmitField("Consultar Actividad")        # OJO - falta adicionar botón


class BuscarEstudiante(FlaskForm):
    codigo = IntegerField("Codigo", validators = [DataRequired("Por favor llene este campo")])
    nombre = StringField("Nombre del estudiante")
    retroalimentacion = StringField("Retroalimentación")
    nota = StringField("Nota")
    asignatura = StringField("Asignatura")
    buscar = SubmitField("Buscar",render_kw=({"onfocus":"cambiaRuta('/buscador')"}))
    editar = SubmitField("Editar calificación",render_kw=({"onfocus":"cambiaRuta('/notas/ingresar')"}))
    
