# TESIS_oficial
 Proyecto
#instalas la virtualizacion
py -m vevn env
#activas virtualizacion
pip install requirements.txt

#generas la base de datos 
py manage.py makemigrations
py manage.py migration

#crea usuario
py manage.py createsuperuser

#ejecuta
py manage.py runserver

#ojo revisar
si quieres poner tu direccion ip
ALLOWED_HOSTS = ['192.168.66.170','177.234.200.10']

si quieres ejecuar x default
ALLOWED_HOSTS = []
