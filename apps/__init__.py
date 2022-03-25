# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

from flask_admin import Admin

from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    current_user,
    hash_password,
    permissions_accepted,
    permissions_required,
    roles_accepted,
    logout_user,
)

from flask_mail import Mail

from flask_ckeditor import CKEditor

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
ckeditor = CKEditor()

from apps.authentication.models import AccionesTestMedico, DocumentoPaciente, File, Role, Test, TestUnit, User, Centro, Model, Boundary, TrainingPoint
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'prefall'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    app.security = Security(app, user_datastore)

    from apps.authentication.modelViews import AdminModelView
    admin = Admin(app, name='webapp', template_mode='bootstrap3')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Role, db.session))
    admin.add_view(AdminModelView(Test, db.session))
    admin.add_view(AdminModelView(TestUnit, db.session))
    admin.add_view(AdminModelView(Centro, db.session))
    admin.add_view(AdminModelView(File, db.session))
    admin.add_view(AdminModelView(DocumentoPaciente, db.session))
    admin.add_view(AdminModelView(AccionesTestMedico, db.session))
    
    return app