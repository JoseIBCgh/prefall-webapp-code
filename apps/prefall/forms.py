from tokenize import String
from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, DecimalField, DateField, 
    TextAreaField, SubmitField, PasswordField, EmailField, SelectField
)
from wtforms.validators import DataRequired, AnyOf, Optional, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask_ckeditor import CKEditorField

class CreatePatientClinicalForm(FlaskForm):
    identificador = StringField('Identificador',id='id_create_patient', validators=[
        DataRequired(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
        ])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    apellidos = StringField('Apellidos', id='apellidos_create_user', validators=[DataRequired()])
    email = StringField('Email', id='email_create_patient', validators=[DataRequired()])
    username = StringField('Username', id='username_create_patient', validators=[DataRequired()])
    password = StringField('Password', id='password_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = SelectField('Sexo', id='sex_create_patient', choices=[('V', 'V'), ('M', 'M')], validators=[DataRequired()])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])
    antecedentes = TextAreaField('Antecedentes clínicos', id='antecedentes_create_patient', validators=[Optional()])

class CreatePatientPersonalForm(FlaskForm):
    identificador = StringField('Identificador',id='id_create_patient', validators=[
        DataRequired(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
        ])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    apellidos = StringField('Apellidos', id='apellidos_create_user', validators=[DataRequired()])
    email = StringField('Email', id='email_create_patient', validators=[DataRequired()])
    username = StringField('Username', id='username_create_patient', validators=[DataRequired()])
    password = StringField('Password', id='password_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = SelectField('Sexo', id='sex_create_patient', choices=[('V', 'V'), ('M', 'M')], validators=[DataRequired()])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])

class CreateUserForm(FlaskForm):
    identificador = StringField('Identificador',id='id_create_user', validators=[
        DataRequired(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
        ])
    nombre = StringField('Nombre', id='name_create_user', validators=[DataRequired()])
    apellidos = StringField('Apellidos', id='apellidos_create_user', validators=[DataRequired()])
    email = StringField('Email', id='email_create_patient', validators=[DataRequired()])
    username = StringField('Username', id='username_create_patient', validators=[DataRequired()])
    password = StringField('Password', id='password_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_user', validators=[DataRequired()])
    sexo = SelectField('Sexo', id='sex_create_patient', choices=[('V', 'V'), ('M', 'M')], validators=[DataRequired()])
    altura = DecimalField('Altura', id='height_create_user', validators=[Optional()])
    peso = DecimalField('Peso', id='weight_create_user', validators=[Optional()])
    tipo = SelectField('Tipo', id='type_create_user', choices=[
        ('paciente', 'Paciente'),
        ('medico', 'Medico'),
        ('auxiliar', 'Auxiliar')
    ])

class CreateCenterAdminForm(FlaskForm):
    identificador = StringField('Identificador',id='id_create_user', validators=[
        DataRequired(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
        ])
    username = StringField('Usuario', id='username_admin', validators=[DataRequired()])
    nombre = StringField('Nombre', id='name_admin', validators=[DataRequired()])
    apellidos = StringField('Apellidos', id='apellidos_admin', validators=[DataRequired()])
    password = PasswordField('Contraseña', id='password_admin', validators=[DataRequired()])
    email = EmailField("Email", id="email_admin", validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_admin', validators=[DataRequired()])
    sexo = SelectField('Sexo', id='sex_admin', choices=[('V', 'V'), ('M', 'M')], validators=[DataRequired()])

class EditPersonalDataForm(FlaskForm):
    identificador = StringField('Identificador',id='id_edit_personal_data', validators=[
        Optional(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
        ])
    nombre = StringField('Nombre', id='name_edit_personal_data', validators=[Optional()])
    apellidos = StringField('Apellidos', id='apellidos_edit_personal_data', validators=[Optional()])
    password = PasswordField('Contraseña', id='password_edit_personal_data', validators=[Optional()])
    fecha = DateField('Fecha de nacimiento', id='date_edit_personal_data', validators=[Optional()])
    sexo = SelectField('Sexo', id='sex_edit_personal_data', choices=[('V', 'V'), ('M', 'M')], validators=[Optional()])
    altura = DecimalField('Altura', id='height_edit_personal_data', validators=[Optional()])
    peso = DecimalField('Peso', id='weight_edit_personal_data', validators=[Optional()])

class EditClinicalDataForm(FlaskForm):
    identificador = StringField('Identificador',id='id_edit_clinical_data', validators=[
        Optional(),
        Length(max=10, message='Solo se permiten 10 caracteres como máximo')
    ])
    nombre = StringField('Nombre', id='name_edit_personal_data', validators=[Optional()])
    apellidos = StringField('Apellidos', id='apellidos_edit_personal_data', validators=[Optional()])
    fecha = DateField('Fecha de nacimiento', id='date_edit_personal_data', validators=[Optional()])
    sexo = SelectField('Sexo', id='sex_edit_personal_data', choices=[('V', 'V'), ('M', 'M')], validators=[Optional()])
    altura = DecimalField('Altura', id='height_edit_personal_data', validators=[Optional()])
    peso = DecimalField('Peso', id='weight_edit_personal_data', validators=[Optional()])
    antecedentes = TextAreaField('Antecedentes clínicos', id='antecedentes_edit_personal_data', validators=[Optional()])

class EditCenterDataForm(FlaskForm):
    cif = StringField('CIF', id='cif_edit_center_data', validators=[Optional()])
    nombreFiscal = StringField('Nombre fiscal', id='name_edit_center_data', validators=[Optional()])
    direccion = StringField('Dirección', id='direccion_edit_center_data', validators=[Optional()])
    CP = IntegerField('CP', id='CP_edit_center_data', validators=[Optional()])
    ciudad = StringField('Ciudad', id='ciudad_edit_center_data', validators=[Optional()])
    provincia = StringField('Provincia', id='provincia_edit_center_data', validators=[Optional()])
    pais = StringField('País', id='pais_edit_center_data', validators=[Optional()])

class UploadTestForm(FlaskForm):
    test = FileField('Introducir test de la marcha', validators=[
        FileRequired(),
        FileAllowed(['txt', 'csv'], 'csv only')
    ])
    submitUploadTest = SubmitField('Upload', id="submit_upload_test")

class UploadFileForm(FlaskForm):
    file = FileField('Introducir fichero', validators=[
        FileRequired()
    ])
    submitUploadFile = SubmitField('Upload', id="submit_upload_file")

class CreateCenterForm(FlaskForm):
    cif = StringField('CIF', id='cif_create_health_center', validators=[DataRequired()])
    nombre = StringField('Nombre fiscal', id='nombre_create_health_center', validators=[DataRequired()])
    direccion = StringField('Dirección', id='direccion_create_health_center', validators=[DataRequired()])
    CP = IntegerField('CP', id='cp_create_health_center', validators=[DataRequired()])
    ciudad = StringField('Ciudad', id='ciudad_create_health_center', validators=[DataRequired()])
    provincia = StringField('Provincia', id='provincia_create_health_center', validators=[DataRequired()])
    pais = StringField('País', id='pais_create_health_center', validators=[DataRequired()])

class FilterUserForm(FlaskForm):
    identificador = StringField('Identificador',id='id_filter_user', validators=[Optional()])
    nombre = StringField('Nombre', id='name_filter_user', validators=[Optional()])
    centro = StringField('Centro', id='center_filter_user', validators=[Optional()])
    submitFilterUser = SubmitField('Filtrar', id="submit_filter_user")

class FilterTestForm(FlaskForm):
    nombrePaciente = StringField('Nombre', id='name_filter_test', validators=[Optional()])
    numero = IntegerField('Número',id='id_filter_test', validators=[Optional()])
    submitFilterTest = SubmitField('Filtrar', id="submit_filter_test")

class FilterFileForm(FlaskForm):
    nombreFichero = StringField('Nombre', id='name_filter_test', validators=[Optional()])
    submitFilterFile = SubmitField('Filtrar', id="submit_filter_test")

class DiagnosticarTestForm(FlaskForm):
    diagnostico = CKEditorField('Diagnostico', validators=[DataRequired()])
    submitDiagnosticoTest = SubmitField('Enviar', id="diagnosticar_test_submit")

class ElementForm(FlaskForm):
    selected_element = SelectField('Select an Element', coerce=int)
    submit = SubmitField('Submit')

class ElementStringForm(FlaskForm):
    selected_element = SelectField('Select an Element', coerce=str)
    submit = SubmitField('Submit')

class DoubleElementForm(FlaskForm):
    selected_element = SelectField('Select an Element', coerce=int)
    second_selected_element = SelectField('Select Another Element', coerce=str)
    submit = SubmitField('Submit')

class CompareTestsForm(FlaskForm):
    paciente1 = SelectField('Selecciona un paciente', coerce=int)
    test1 = SelectField('Selecciona un test', coerce=int, validate_choice=False)
    paciente2 = SelectField('Selecciona un paciente', coerce=int)
    test2 = SelectField('Selecciona otro test', coerce=int, validate_choice=False)
    metric = SelectField('Selecciona la metrica', coerce=str)
    submit = SubmitField('Submit')

class CompareFasesForm(FlaskForm):
    paciente1 = SelectField('Selecciona un paciente', coerce=int)
    test1 = SelectField('Selecciona un test', coerce=int, validate_choice=False)
    paciente2 = SelectField('Selecciona otro paciente', coerce=int)
    test2 = SelectField('Selecciona otro test', coerce=int, validate_choice=False)
    submit = SubmitField('Submit')

class CompareTestsFormPaciente(FlaskForm):
    test1 = SelectField('Selecciona un test', coerce=int)
    test2 = SelectField('Selecciona otro test', coerce=int)
    metric = SelectField('Selecciona la metrica', coerce=str)
    submit = SubmitField('Submit')

class CompareFasesFormPaciente(FlaskForm):
    test1 = SelectField('Selecciona un test', coerce=int)
    test2 = SelectField('Selecciona otro test', coerce=int)
    submit = SubmitField('Submit')

class MetricForm(FlaskForm):
    selected_element = SelectField('Select a metric', coerce=str)
    submit = SubmitField('Submit')