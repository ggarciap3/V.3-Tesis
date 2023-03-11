from django.shortcuts import render,redirect
from django.core import serializers
from pqrs.models import Categoriapq,Tipospq, Ingresopq, opciones_Presentaciones, opciones_Productos # opciones_horaFin

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
import ModulPQRS.settings as setting
import json
# librerias para el correo electrónico
import yagmail

# Create your views here.
def home(request):
    return render(request, 'home.html')

class LoginFormView(LoginView):
    template_name ='home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['title']="Iniciar Secion"
        return context

def tipospqs(request):
    listaTipospqs = Tipospq.objects.all()
    return render(request, 'tipospqs.html',{'tipospqs': listaTipospqs})

def chatbot(request):
    return render(request, 'chatbot.html')


def detalleTipospq(request,id):
    vertipospq = Tipospq.objects.get(id=id)
    listaCategoriapqs = Categoriapq.objects.all()
    listaIngresopqs=Ingresopq.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos,'verTipospq':vertipospq, 'categoripqs': listaCategoriapqs,'ingresopqs':listaIngresopqs}
    return render(request, 'vista_ingresopq.html',data)

def adminCategoriapqs(request):
    busqueda= request.GET.get("buscarcategoriapq")
    listaCategoriapqs = Categoriapq.objects.all()

    if busqueda:
        listaCategoriapqs=Categoriapq.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()
    return render(request, 'adminCategoriapqs.html',{'categoriapqs': listaCategoriapqs})

def registroCategoriapq(request):
    nombre = request.POST['disnombre']

    Categoriapq.objects.create(
        nombre=nombre,
    )
    return redirect('/adminCategoriapqs')

def editaCategoriapq(request,id):
    edicioncategoriapq = Categoriapq.objects.get(id=id)
    return render(request, 'edicionCategoriapqs.html', {'edicionCategoriapq': edicioncategoriapq})

def edicionCategoriapqs(request):
    id=request.POST['categoriapqid']
    categoriapq = Categoriapq.objects.get(id=id)

    if request.POST:
        categoriapq=Categoriapq()
        categoriapq.id = request.POST.get('categoriapqid')
        categoriapq.nombre = request.POST.get('categoriapqnombre')
        categoriapq.save()
    return redirect('/adminCategoriapqs')

def eliminacionCategoriapq(request,id):
    categoriapq=Categoriapq.objects.get(id=id)
    categoriapq.delete()
    
    return redirect('/adminCategoriapqs')    

def adminTipospqs(request):
    listaCategoriapqs = Categoriapq.objects.all()
    listaTipospqs = Tipospq.objects.all()
    busqueda= request.GET.get("buscartipospq")

    if busqueda:
        listaTipospqs=Tipospq.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()

    return render(request, 'adminTipospqs.html',{'categoriapqs': listaCategoriapqs,'tipospqs': listaTipospqs})

def registroTipospq(request):
    nombre = request.POST['nombre']

    categoriapq=Categoriapq()
    categoriapq.id = int(request.POST['categoriapq'])
    categoriapq_tipospq=categoriapq
    foto = request.FILES['imagen']
    descripcion = request.POST['descripcion']
    restricciones = request.POST['restricciones']

    Tipospq.objects.create(
        nombre=nombre,
        id_categoriap=categoriapq_tipospq,
        descripcion=descripcion,
        restriciones=restricciones,
        imagen=foto,

    )
    return redirect('/adminTipospqs')


def verTipospq(request,id):
    vertipospq = Tipospq.objects.get(id=id)
    listaCategoriapqs = Categoriapq.objects.all()
    listaIngresopqs=Ingresopq.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos, 'verTipospq':vertipospq,'categoriapqs': listaCategoriapqs,'ingresopqs':listaIngresopqs}
    
    return render(request, 'verTipospqs.html',  data)

def editaTipospq(request,id):
    ediciontipospq = Tipospq.objects.get(id=id)
    imagen=ediciontipospq.imagen
    if request.POST:
        if request.POST.get('imagen')=='':
            tipospq=Tipospq()
            tipospq.id = ediciontipospq.id
            tipospq.nombre=request.POST.get('nombre')
            
            categoriapq=Categoriapq()
            categoriapq.id=request.POST.get('categoriapq')
            tipospq.id_categoriap=categoriapq
            tipospq.imagen=imagen
            tipospq.descripcion=request.POST.get('descripcion')
            tipospq.restriciones=request.POST.get('restricciones')
            tipospq.save()
        else:
            tipospq=Tipospq()
            tipospq.id = ediciontipospq.id
            tipospq.nombre=request.POST.get('nombre')
            categoriapq=Categoriapq()
            categoriapq.id=request.POST.get('categoriapq')
            tipospq.id_categoriap=categoriapq
            tipospq.imagen=request.FILES.get('imagen')
            tipospq.recomendaciones=request.POST.get('recomendaciones')
            tipospq.restriciones=request.POST.get('restricciones')
            tipospq.save()

    return redirect('/verTipospq/'+str(tipospq.id))

def eliminacionTipospq(request,id):
    tipospq=Tipospq.objects.get(id=id)
    tipospq.delete()
    
    return redirect('/adminTipospqs') 

def adminIngresopqs(request):
    listaIngresopq = Ingresopq.objects.all()
    # lo transforma en json
    serialized_data = serializers.serialize('json', listaIngresopq)
    deserialized_data = json.loads(serialized_data)
    # fields son los datos que limpiamos de la base de datos
    listaNueva = []
    for i in deserialized_data:
        listaNueva.append({
            "pk":i["pk"],
            **i["fields"] # aqui saco una copia de los fields por cada pk
        })

    # print(listaCopiaP)
    listaForm = [];
    # creamos una list con los dos arrays
    for d in listaNueva:
        for pre, pro in zip(opciones_Presentaciones, opciones_Productos):
            if d["Presentaciones"] == pre[0]:
                d["Presentaciones"] =  pre[1]

            if d["Productos"] == pro[0]:
                d["Productos"] =  pro[1]
        listaForm.append(d)
    # cambiamos  reservas con el nuevo json  listaFrom    
    # print(serialized_data)
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos, 'ingresopqs':listaForm}
    return render(request, 'adminIngresopqs.html', data)

def registroIngresopqs(request,id):
    
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    ci = request.POST['ci']
    telefono = request.POST['telefono']
    correo = request.POST['correo']

    tipospq=Tipospq()
    tipospq.id = int(id)
    tipospq_ingresopq=tipospq
    num_factura = request.POST['num_factura']
    descrip = request.POST['descrip']
    cantidad = request.POST['cantidad']

    fecha_reserva = request.POST['fecha_reserva']
    Presentaciones = request.POST['Presentaciones']
    Productos = request.POST['Productos']
    evidencia = request.POST['evidencia']
    

    Ingresopq.objects.create(
        nombres=nombre,
        apellidos=apellido,
        cedula=ci,
        telefono=telefono,
        email=correo,
        id_tipospq=tipospq_ingresopq,
        fecha_compra=fecha_reserva,
        num_factura=num_factura,
        descrip=descrip,
        cantidad=cantidad,
        Presentaciones=Presentaciones,
        Productos=Productos,
        evidencia=evidencia,

    )
    mensaje = f"El usuario {nombre} {apellido}"
    enviar_correo(mensaje)
    return redirect('/tipospqs')



def validarFecha(request):
    fecha = request.GET.get('fecha_reserva', None)
    data = {
        'is_taken': Ingresopq.objects.filter(fecha_compra=fecha).exists()
    }
    
    return JsonResponse(data)


#lista de ingresos
def editaIngresopq(request,id):
    edicioningresopqs = Ingresopq.objects.get(id=id)
    return render(request, 'edicionIngresopqs.html', {'edicionIngresopqs': edicioningresopqs})

def edicionIngresopqs(request):
    id=request.POST['ingresopqid']
    ingresopq = Ingresopq.objects.get(id=id)

    if request.POST:
        ingresopq=Categoriapq()
        ingresopq.id = request.POST.get('ingresopqid')
        ingresopq.nombre = request.POST.get('ingresopqnombre')
        ingresopq.save()
    return redirect('/adminIngresopqs')

# metodo para enviar correo
def enviar_correo(mensaje:str):
    lista_correos = User.objects.values_list('email', flat=True)
    para = list(lista_correos);
    yag = yagmail.SMTP("grupo25estudio@gmail.com", "ipaoosgxkwyxaoug")
    body = mensaje
    # para = ["axha0188@gmail.com", "arongarcia558@gmail.com"]
    yag.send(to=para, subject="QUEJAS DE USUARIO", contents=body)