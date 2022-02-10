from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, AnyOf

class CreatePatientForm(FlaskForm):
    id = IntegerField('Identificador',id='id_create_patient', validators=[DataRequired()])
    nombre = StringField('Nombre', id='name_create_patient', validators=[DataRequired()])
    fecha = DateField('Fecha de nacimiento', id='date_create_patient', validators=[DataRequired()])
    sexo = StringField('Sexo', id='sex_create_patient', validators=[DataRequired(), AnyOf(values=["V", "M"], message="Introduce V o M")])
    altura = DecimalField('Altura', id='height_create_patient', validators=[DataRequired()])
    peso = DecimalField('Peso', id='weight_create_patient', validators=[DataRequired()])
    antecedentes = TextAreaField('Antecedentes clínicos', id='antecedentes_create_patient')