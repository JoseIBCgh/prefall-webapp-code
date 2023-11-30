# Prefall Webapp Code

## Plantillas

* Plantilla utilizada datta-able: https://docs.appseed.us/products/flask-dashboards/datta-able


## Instalación


* Versiones:

- Python 3.8.10
- pip 23.0

* Creación del entorno vitual

```
virtualenv venv
```

* Activar entorno

```
env\Scripts>Activate.ps1
```

* Instalar módulos

```
pip install -r requirements.txt
```

* Configurar base de datos:

-     SQLALCHEMY_DATABASE_URI = 'mysql://webapp:webapp@localhost/webapp' en .\apps\config.py   # Como ejemplo

* Configurar variable de entorno para flask:

```
#Hay dos opciones:

set FLASK_APP=run.py

# Pero esta la he probado en Windows 10 y me funciona

$env:FLASK_APP = "run.py" #
```

* Run Flask:

```
flask run 
```

Documentacion en /docs
