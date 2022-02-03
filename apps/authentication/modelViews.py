from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from apps.authentication.models import Permission
from apps.authentication.routes import access_forbidden

class AdminModelView(ModelView):

    def is_accessible(self):
        return current_user.can(Permission.ADMIN)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return access_forbidden("requires admin permision")