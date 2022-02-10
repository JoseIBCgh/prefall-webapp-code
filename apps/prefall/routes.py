from apps.prefall import blueprint
from flask import render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from apps.prefall.forms import CreatePatientForm

from flask_security import (
    auth_required,
    roles_accepted,
    hash_password
)
from random import randint

@blueprint.route('crear_paciente', methods=['GET', 'POST'])
@roles_accepted("auxiliar")
def crear_paciente():
    create_patient_form = CreatePatientForm(request.form)
    if 'create_patient' in request.form and create_patient_form.validate():

        # read form data
        id = request.form['id']
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']

        default_password = "password"
        n = randint(0,1000000)
        default_email = "default"+ str(n) +"@kruay.com"

        from apps import user_datastore, db
        user_datastore.create_user(
            id=id, nombre=nombre, fecha_nacimiento=fecha, sexo=sexo, altura=altura,
            peso=peso, antecedentes_clinicos=antecedentes, 
            password=hash_password(default_password), email=default_email, roles=["paciente"]
        )
        db.session.commit()

        return redirect(url_for('home_blueprint.index'))


    return render_template('prefall/create_patient.html', form=create_patient_form)