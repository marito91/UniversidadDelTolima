from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField, SelectField, DateTimeField, DecimalField 
from wtforms.validators import DataRequired 


class Login(FlaskForm):
    username = IntegerField("Identificacion", validators = [DataRequired("Por favor llene este campo con numeros")])
    password = PasswordField("Password", validators = [DataRequired("Por favor llene este campo")])
    entrar = SubmitField("Entrar")


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
    codigo = IntegerField("Codigo", validators = [DataRequired("Por favor llene este campo")])
    estudiante = IntegerField("Estudiante", validators = [DataRequired("Por favor llene este campo")])
    asignatura = SelectField("Asignatura", choices=["","-FU- Fundamentos de Programacion", "-PB- Programacion Basica", "-DS- Desarrollo de Software"])
    actividad = IntegerField("Actividad", validators = [DataRequired("Por favor llene este campo")])
    tipo = SelectField("Tipo Nota", choices=["01-Nota","02-Nivelacion", "03-Trabajo Escritro", "04-Supletorio"])
    info = StringField("Tipo Actividad")
    nota = DecimalField("Nota")
    notaAsignatura = DecimalField("Nota Asignatura")
    ingresar = SubmitField("Ingresar")

    


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
    editar = SubmitField("actualizar",render_kw=({"onfocus":"cambiaRuta('/asignaturas/editar')"}))


#class Actividades(FlaskForm):
