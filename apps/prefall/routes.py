from apps.authentication.models import User
from apps.prefall import blueprint
from flask import jsonify, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from apps.prefall.decorators import clinical_data_access, personal_data_access
from apps.prefall.forms import CreatePatientForm, EditClinicalDataForm, EditPersonalDataForm

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

@blueprint.route('detalles_personales/<id>', methods=['GET', 'POST'])
@personal_data_access()
def detalles_personales(id):
    paciente = User.query.filter_by(id=id).first()
    return render_template('prefall/detalles_personales.html', paciente=paciente)

@blueprint.route('detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_clinicos(id):
    paciente = User.query.filter_by(id=id).first()
    return render_template('prefall/detalles_clinicos.html', paciente=paciente)

@blueprint.route('editar_detalles_personales/<id>', methods=['GET', 'POST'])
@personal_data_access()
def editar_detalles_personales(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditPersonalDataForm(request.form)
    if 'editar_detalles_personales' in request.form and form.validate():
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        if nombre != "":
            paciente.nombre = nombre
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
        from apps import db
        db.session.commit()
        return redirect(url_for('prefall_blueprint.detalles_personales', id=id))
        
    return render_template(
        'prefall/editar_detalles_personales.html', 
        form=form, paciente=paciente)

@blueprint.route('editar_detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def editar_detalles_clinicos(id):
    paciente = User.query.filter_by(id=id).first()
    form = EditClinicalDataForm(request.form)
    if 'editar_detalles_clinicos' in request.form and form.validate():
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        sexo = request.form['sexo']
        altura = request.form['altura']
        peso = request.form['peso']
        antecedentes = request.form['antecedentes']
        if nombre != "":
            paciente.nombre = nombre
        if fecha != "":
            paciente.fecha_nacimiento = fecha
        if sexo != "":
            paciente.sexo = sexo
        if altura != "":
            paciente.altura = altura
        if peso != "":
            paciente.peso = peso
        if antecedentes != "":
            paciente.antecedentes_clinicos = antecedentes
        from apps import db
        db.session.commit()
        return redirect(url_for('prefall_blueprint.detalles_clinicos', id=id))
        
    return render_template(
        'prefall/editar_detalles_clinicos.html', 
        form=form, paciente=paciente)

@blueprint.route('debug/<info>')
def debug(info):
    return info