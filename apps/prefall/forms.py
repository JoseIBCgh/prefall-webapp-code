from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, AnyOf, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreatePatientClinicalForm(FlaskForm):
    id = IntegerField('Identificador',id='id_create_patient', validators=[DataRequired()])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = StringField('Sexo', id='sex_create_patient', validators=[DataRequired(), AnyOf(values=["V", "M"], message="Introduce V o M")])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])
    antecedentes = TextAreaField('Antecedentes clínicos', id='antecedentes_create_patient', validators=[Optional()])

class CreatePatientPersonalForm(FlaskForm):
    id = IntegerField('Identificador',id='id_create_patient', validators=[DataRequired()])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = StringField('Sexo', id='sex_create_patient', validators=[DataRequired(), AnyOf(values=["V", "M"], message="Introduce V o M")])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])

class EditPersonalDataForm(FlaskForm):
    nombre = StringField('Nombre', id='name_edit_personal_data', validators=[Optional()])
    fecha = DateField('Fecha de nacimiento', id='date_edit_personal_data', validators=[Optional()])
    sexo = StringField('Sexo', id='sex_edit_personal_data', validators=[Optional(), AnyOf(values=["V", "M"], message="Introduce V o M")])
    altura = DecimalField('Altura', id='height_edit_personal_data', validators=[Optional()])
    peso = DecimalField('Peso', id='weight_edit_personal_data', validators=[Optional()])

class EditClinicalDataForm(FlaskForm):
    nombre = StringField('Nombre', id='name_edit_personal_data', validators=[Optional()])
    fecha = DateField('Fecha de nacimiento', id='date_edit_personal_data', validators=[Optional()])
    sexo = StringField('Sexo', id='sex_edit_personal_data', validators=[Optional(), AnyOf(values=["V", "M"], message="Introduce V o M")])
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
    submitUpload = SubmitField('Upload', id="submit_upload_test")

class CreateCenterForm(FlaskForm):
    cif = StringField('CIF', id='cif_create_health_center', validators=[DataRequired()])
    nombre = StringField('Nombre fiscal', id='nombre_create_health_center', validators=[DataRequired()])
    direccion = StringField('Dirección', id='direccion_create_health_center', validators=[DataRequired()])
    CP = IntegerField('CP', id='cp_create_health_center', validators=[DataRequired()])
    ciudad = StringField('Ciudad', id='ciudad_create_health_center', validators=[DataRequired()])
    provincia = StringField('Provincia', id='provincia_create_health_center', validators=[DataRequired()])
    pais = StringField('País', id='pais_create_health_center', validators=[DataRequired()])

class FilterUserForm(FlaskForm):
    id = IntegerField('Identificador',id='id_filter_user', validators=[Optional()])
    nombre = StringField('Nombre', id='name_filter_user', validators=[Optional()])
    centro = StringField('Centro', id='center_filter_user', validators=[Optional()])
    submitFilterUser = SubmitField('Filtrar', id="submit_filter_user")

class FilterTestForm(FlaskForm):
    nombrePaciente = StringField('Nombre', id='name_filter_test', validators=[Optional()])
    numero = IntegerField('Número',id='id_filter_test', validators=[Optional()])
    submitFilterTest = SubmitField('Filtrar', id="submit_filter_test")

class DiagnosticarTestForm(FlaskForm):
    diagnostico = TextAreaField('Diagnostico', id='diagnosticar_test_input', validators=[DataRequired()])
    submitDiagnosticoTest = SubmitField('Enviar', id="diagnosticar_test_submit")