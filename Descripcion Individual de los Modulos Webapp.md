# authentication
### Descripción general y propósito
Se encarga del login y logout y define los modelos en el fichero models.py
### Dependencias
- apps.db
- flask
- flask_security
- ast
- optparse
- flask_wtf
- wtforms
- sqlalchemy
### Implementacion
- __init__.py
- forms.py
- modelViews.py
- models.py
- routes.py
- util.py
# home
### Descripción general y propósito
Pantalla home de todos los usuarios
### Dependencias
- flask
- flask_security
### Implementacion
- __init__.py
- forms.py
- routes.py
# prefall
### Descripción general y propósito
Modulo principal donde estan todas las rutas de la app. Estan separadas por zonas segun el usuario (medico, paciente, auxiliar ...)
### Dependencias
- apps.authentication
- functools
- flask
- flask_security
- tokenize
- flask_wtf
- wtforms
- flask_ckeditor
- pandas
- numpy
- os
- sklearn
- collections
- scipy
- math
- itertools
- glob
- io
- warnings
- base64
- matplotlib
- jinja2
- random
- werkzeug
- datetime
### Implementacion
- __init__.py
- decorators.py
- forms.py
- libraries.py
- routes.py