from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, AnyOf, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreatePatientForm(FlaskForm):
    id = IntegerField('Identificador',id='id_create_patient', validators=[DataRequired()])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = StringField('Sexo', id='sex_create_patient', validators=[DataRequired(), AnyOf(values=["V", "M"], message="Introduce V o M")])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])
    antecedentes = TextAreaField('Antecedentes clínicos', id='antecedentes_create_patient', validators=[Optional()])

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

class UploadTestForm(FlaskForm):
    test = FileField('Introducir test de la marcha', validators=[
        FileRequired(),
        FileAllowed(['txt', 'csv'], 'csv only')
    ])
    submit = SubmitField('Upload', id="submit_upload_test")

class CreateCenterForm(FlaskForm):
    cif = StringField('CIF', id='cif_create_health_center', validators=[DataRequired()])
    nombre = StringField('Nombre fiscal', id='nombre_create_health_center', validators=[DataRequired()])
    direccion = StringField('Dirección', id='direccion_create_health_center', validators=[DataRequired()])
    CP = IntegerField('CP', id='cp_create_health_center', validators=[DataRequired()])
    ciudad = StringField('Ciudad', id='ciudad_create_health_center', validators=[DataRequired()])
    provincia = StringField('Provincia', id='provincia_create_health_center', validators=[DataRequired()])
    pais = StringField('País', id='pais_create_health_center', validators=[DataRequired()])

class FilterBarForm(FlaskForm):
    id = IntegerField('Identificador',id='id_filter_bar', validators=[Optional()])
    nombre = StringField('Nombre', id='name_filter_bar', validators=[Optional()])
    submit = SubmitField('Filtrar', id="submit_filter_bar")