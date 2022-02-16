# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import redirect, render_template, request, url_for
from jinja2 import TemplateNotFound

from flask_security import (
    auth_required,
    roles_accepted,
    current_user,
)

from apps.home.forms import FilterBarForm

@blueprint.route('/index', methods=['GET', 'POST'])
@auth_required()
def index():
    from apps import db
    from apps.authentication.models import User, Centro, Role
    if(current_user.has_role("medico")):
        form = FilterBarForm()
        pacientes = current_user.pacientes_asociados
        if "filter" in request.form and form.validate():
            pacientes = apply_filters(pacientes, request.form)

        return render_template('accounts/loged.html', pacientes=pacientes, form=form)
    if(current_user.has_role("auxiliar")):
        form = FilterBarForm()
        userRole = Role.query.filter_by(name="paciente").first()
        center = current_user.centro
        pacientes = User.query.\
            filter(User.roles.contains(userRole)).\
                filter_by(centro = center).all()
        if "filter" in request.form and form.validate():
            pacientes = apply_filters(pacientes, request.form)

        return render_template('accounts/loged.html', pacientes=pacientes, form=form)
    return render_template('home/index.html', segment='index')

def apply_filters(pacientes, form):
    id = form['id']
    nombre = form['nombre']
    if id != '':
        pacientes = filter(lambda p: p.id == int(id), pacientes)
    if nombre != '':
        pacientes = filter(lambda p: nombre in p.nombre, pacientes)
    return pacientes
'''
@blueprint.route('/<template>')
@auth_required()
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
'''