from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, Optional

class FilterBarForm(FlaskForm):
    id = IntegerField('Identificador',id='id_filter_bar', validators=[Optional()])
    nombre = StringField('Nombre', id='name_filter_bar', validators=[Optional()])