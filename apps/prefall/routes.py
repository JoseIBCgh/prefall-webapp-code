from sqlalchemy import null, desc, create_engine, exc

from apps.authentication.models import Test, User
from apps.prefall import blueprint
from flask import jsonify, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound

from flask_security import (
    auth_required,
    roles_accepted,
    hash_password
)
from random import randint

from flask import flash, current_app
from werkzeug.utils import secure_filename
import os
from pathlib import Path

from apps.prefall.decorators import clinical_data_access, personal_data_access
from apps.prefall.forms import (
    CreatePatientForm, 
    EditClinicalDataForm, 
    EditPersonalDataForm,
    UploadTestForm
)

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
    form = UploadTestForm()

    if form.validate_on_submit():
        file = form.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        try:
            add_df_to_sql(df)
        except exc.IntegrityError:
            form.test.errors.append("Duplicated data")
        os.remove(file_path)
        return redirect(request.url)
    return render_template('prefall/detalles_personales.html', paciente=paciente, form=form)

@blueprint.route('detalles_clinicos/<id>', methods=['GET', 'POST'])
@clinical_data_access()
def detalles_clinicos(id):
    paciente = User.query.filter_by(id=id).first()
    form = UploadTestForm()

    if form.validate_on_submit():
        file = form.test.data
        filename = secure_filename(file.filename)
        Path(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = read_csv(file_path)
        df = add_columns(df, id)
        df = df.drop_duplicates(subset=["time"])
        try:
            add_df_to_sql(df)
        except exc.IntegrityError:
            form.test.errors.append("Duplicated data")
        os.remove(file_path)
        return redirect(request.url)
    return render_template('prefall/detalles_clinicos.html', paciente=paciente, form=form)

ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_csv(filename):
    import pandas as pd
    colnames = ["date", "time", "acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y", "mag_z"]
    df = pd.read_csv(
        filename, delim_whitespace=True, skiprows=6, usecols=range(1,12), 
        names=colnames)
    return df

def add_columns(df, id_paciente):
    df["id_paciente"] = id_paciente
    
    from apps import db
    
    test = db.session.query(Test).filter(
        Test.id_paciente == id_paciente).order_by(
        db.desc(Test.num_test)).limit(1).first()
    if test is None:
        next_num = 0
    else:
        next_num = test.num_test + 1
    df["num_test"] = next_num
    
    return df

def add_df_to_sql(df):
    try:
        sql_engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        df.to_sql('test', sql_engine, if_exists='append', index=False)
        sql_engine.dispose()
    except exc.IntegrityError as e:
        sql_engine.dispose()
        raise e


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