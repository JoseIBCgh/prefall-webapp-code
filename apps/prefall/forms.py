from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, Optional

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
