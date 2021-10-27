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
    #usuario = StringField("Usuario")
    #id = StringField("ID")
    guardar = SubmitField("Guardar")
    eliminar = SubmitField("Eliminar",render_kw=({"onfocus":"cambiaRuta('/usuario/eliminar/delete')"}))
    editar = SubmitField("Editar")
    consulta = SubmitField("Buscar")
    buscar = SubmitField("Buscar",render_kw=({"onfocus":"cambiaRuta('/usuario/eliminar/get')"}))

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
    #asignatura = SelectField("Asignatura", choices=["","-FU- Fundamentos de Programacion", "-PB- Programacion Basica", "-DS- Desarrollo de Software"])
    actividad = StringField("Actividad", validators = [DataRequired()])
    tipo = SelectField("Tipo Nota", choices=["Nota","Nivelacion", "Trabajo Escritro", "Supletorio"])
    #info = StringField("Tipo Actividad")
    nota = StringField("Nota")
    notaAsignatura = DecimalField("Nota Asignatura")
    ingresar = SubmitField("Ingresar", render_kw=({"onfocus":"cambiaRuta('/notas/ingresar')"}))

    


class Asignaturas(FlaskForm):
    codigo = IntegerField("Codigo")
    asignatura = StringField("Nombre de asignatura" )
    # materias = SelectField("Asignatura", choices=["","-FU- Fundamentos de Programacion", "-PB- Programacion Basica", "-DS- Desarrollo de Software"],validators = [DataRequired("Por favor llene este campo")])
    # docente = SelectField("Docente", choices=["Por definir","ANDRES GUTIERREZ", "MARCELA VALENCIA", "DAVID MURILLO"],validators = [DataRequired("Por favor llene este campo")])
    tipo = SelectField("Tipo de Asignatura", choices=["Por definir","ELECTIVA", "FORMACION BASICA", "OBLIGATORIA", "PRACTICAS", "OTRO"], validators = [DataRequired("Por favor llene este campo")])
    descripcion = TextAreaField("Descripción de la asignatura") #Usar un place holder para indicar descripción
    # fecha = DateTimeField("Fecha cierre", validators = [DataRequired("Por favor llene este campo")])
    # cierre = DateTimeField("Fecha cierre")
    # inscritos = TextAreaField("Estudiantes inscritos", validators = [DataRequired("Por favor llene este campo")])#Usar un place holder para indicar ids Estudiantes
    # estudiantes = SelectField("Estudiantes inscritos", choices=["","AMAURY ARROYO", "CARLOS AGUIRRE", "DANIEL LONDOÑO", "JULIAN DAVID DEL RIO", "MARIO GOMEZ"])
    registrar = SubmitField('Registrar',render_kw=({"onfocus":"cambiaRuta('/asignaturas/registrar')"}))
    buscar = SubmitField('Buscar',render_kw=({"onfocus":"cambiaRuta('/asignaturas/get')"}))
    eliminar = SubmitField('Eliminar',render_kw=({"onfocus":"cambiaRuta('/asignaturas/eliminar')"}))
    editar = SubmitField("Actualizar",render_kw=({"onfocus":"cambiaRuta('/asignaturas/editar')"}))


class Actividades(FlaskForm):
    id_actividad = StringField("ID actividad", validators = [DataRequired("Por favor llene este campo")])
    tipo_actividad = SelectField("Tipo de Actividad", choices=["Quiz","Evaluación","Trabajo escrito","Tarea"])
    # tasks = SelectField("tasks", choices=["","1-Algoritmos", "2-Condicionales", "3-Ciclos", "4-Bases de datos", "5-Desarrollo de Apps/Web", "6-Proyecto Full Stack"]) #,validators = [DataRequired("Por favor llene este campo")
    nombre_actividad = StringField("Nombre Actividad")
    id_asignatura_fk = SelectField("ID Asignatura",choices=["1","2","3"])
    # tipo_nota = SelectField("Tipo Nota", choices=["01-Nota", "02-Nivelación", "03-Trabajo Escrito", "04-Supletorio"], validators = [DataRequired("Por favor llene este campo")])
    fecha_actividad = DateTimeField("Fecha de Entrega")
    # nota_final_actividad = FloatField("Nota Final Actividad", validators = [DataRequired("Por favor llene este campo")])
    # nota_final_asignatura = FloatField("Nota Final Asignatura", validators = [DataRequired("Por favor llene este campo")])
    #estudiantes = SelectField("Estudiantes inscritos", choices=["","AMAURY ARROYO", "CARLOS AGUIRRE", "DANIEL LONDOÑO", "JULIAN DAVID DEL RIO", "MARIO GOMEZ"]) #,validators = [DataRequired("Por favor llene este campo")
    #docente = SelectField("Docente", choices=["Por definir","ANDRES GUTIERREZ", "MARCELA VALENCIA", "DAVID MURILLO"])   # REVISAR TEMA SESIÓN CON VARIABLE GLOBAL
    instrucciones_actividad = StringField("Instrucciones")
    registrar_actividad = SubmitField("Registrar")  # OJO - falta adicionar botón registrar en menu Registrar actividades
    consultar_actividad = SubmitField("Consultar Actividad")        # OJO - falta adicionar botón
    #eliminar = SubmitField("Eliminar")    # NO HAY MENÚ ELIMINAR, PONER OPCIÓN EN FORM REGISTRAR?
    # editar = SubmitField("Editar")        # NO HAY MENÚ EDITAR
    #guardar = SubmitField("Guardar")      # Esta en MENU RETROALIMENTAR