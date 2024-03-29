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

@blueprint.route('/old', methods=['GET', 'POST'])
def old():

    return render_template('home/index.html', segment='index')

@blueprint.route('/index', methods=['GET', 'POST'])
@auth_required()
def index():
    if current_user.has_role("paciente"):
        return redirect(url_for('prefall_blueprint.pantalla_principal_paciente'))

    if current_user.has_role("medico"):
        return redirect(url_for('prefall_blueprint.pantalla_principal_medico'))

    if current_user.has_role("auxiliar"):
        return redirect(url_for('prefall_blueprint.pantalla_principal_auxiliar'))

    if current_user.has_role('admin'):
        return redirect(url_for('prefall_blueprint.lista_centros'))

    if current_user.has_role('admin-centro'):
        from apps.authentication.models import Centro
        centro = Centro.query.filter(Centro.id_admin == current_user.id).first()
        return redirect(url_for('prefall_blueprint.detalles_centro', id_centro=centro.id))


    return render_template('home/index.html', segment='index')
    
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