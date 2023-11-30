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
# static/assets/css
### Descripción general y propósito
Contiene todos los estilos.
### Dependencias
- url("https://fonts.googleapis.com/css?family=Open+Sans:300,400,600");
- url("../plugins/bootstrap/css/bootstrap.min.css");
- url("../fonts/feather/css/feather.css");
- url("../plugins/jquery-scrollbar/css/jquery.scrollbar.min.css");
- url("../fonts/datta/datta-icon.css");
### Implementacion
- style.css
# static/assets/js
### Descripción general y propósito
Contiene algunas funciones de js. vendor-all.min y pcoded.min.js es el js de la plantilla Flask datta-able. predict.js es la funcion que se encarga de llamar a analizar un fichero con el modelo de ML.
### Dependencias
No tiene
### Implementacion
- pcoded.min.js
- vendor-all.min.js
- predict.js
# static/assets/plugins
### Descripción general y propósito
Codigo de la plantilla Flask datta-able
# templates
### Descripción general y propósito
Contiene todas las templates de la aplicación
## templates/accounts
### Descripción general y propósito
Templates de login y registro
### Dependencias
No tiene
### Implementacion
- loged.html
- login.html
- register.html
## templates/home
### Descripción general y propósito
Esto viene con la plantilla Flask datta-able
## templates/includes
### Descripción general y propósito
Componentes que se añaden a las templates.
### Dependencias
- /static/assets/js/vendor-all.min.js
- /static/assets/plugins/bootstrap/js/bootstrap.min.js
- /static/assets/js/pcoded.min.js
### Implementacion
- _form_helpers.html
- base-sidebar.html
- navigation.html
- scripts.html
- sidebar-admin-centro.html
- sidebar-admin.html
- sidebar-authenticated.html
- sidebar-auxiliar.html
- sidebar-medico.html
- sidebar-paciente.html
- sidebar.html
## templates/layouts
### Descripción general y propósito
Templates base a partir de los que se heredan los otros
### Dependencias
- /static/assets/fonts/fontawesome/css/fontawesome-all.min.css
- /static/assets/plugins/animation/css/animate.min.css
- /static/assets/css/style.css
### Implementacion
- base-fullscreen.html
- base.html
## templares/prefall
### Descripción general y propósito
Todas las vistas de las rutas de la aplicacion.
### Dependencias
- /static/assets/js/plot.js
- /static/assets/js/predict.js
- https://cdnjs.cloudflare.com/ajax/libs/tabulator/5.5.2/css/tabulator.min.css
- https://cdnjs.cloudflare.com/ajax/libs/tabulator/5.5.2/js/tabulator.min.js
- https://cdn.plot.ly/plotly-latest.min.js
- https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js
- https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js
- https://cdnjs.cloudflare.com/ajax/libs/canvg/1.5/canvg.js
- https://cdn.webdatarocks.com/latest/webdatarocks.min.css
- https://cdn.webdatarocks.com/latest/webdatarocks.toolbar.min.js
- https://cdn.webdatarocks.com/latest/webdatarocks.js
- https://code.jquery.com/jquery-3.2.1.slim.min.js
- https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js
- https://cdnjs.cloudflare.com/ajax/libs/jquery-expander/1.7.0/jquery.expander.min.js
### Implementacion
- center_list.html
- create_admin_center.html
- create_center.html
- create_patient_clinical.html
- create_patient_personal.html
- create_user.html
- detalles_centro.html
- detalles_centro_admin.html
- detalles_clinicos.html
- detalles_personales.html
- detalles_test.html
- editar_detalles_centro.html
- editar_detalles_clinicos.html
- editar_detalles_personales.html
- pantalla_principal_auxiliar.html
- pantalla_principal_medico.html
- pantalla_principal_paciente.html
- plots.html
- plots_paciente.html
- ver_detalles_test.html
## templates/security
### Descripción general y propósito
Vistas de manejo de contraseñas. (cambio, reset, olvidada)
### Dependencias
No tiene
### Implementacion
- change_password.html
- forgot_password.html
- reset_password.html