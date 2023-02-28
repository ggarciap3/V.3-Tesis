from django.shortcuts import render,redirect
from django.core import serializers
from reservas.models import Disiplina,Instalacion, Reserva, opciones_Presentaciones, opciones_Productos # opciones_horaFin

from django.http import JsonResponse

from django.contrib.auth.views import LoginView,LogoutView
import complejo.settings as setting
import json

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

def instalaciones(request):
    listaInstalaciones = Instalacion.objects.all()
    return render(request, 'instalaciones.html',{'instalaciones': listaInstalaciones})

def chatbot(request):
    return render(request, 'chatbot.html')


def detalleInstalacion(request,id):
    verinstalacion = Instalacion.objects.get(id=id)
    listaDisiplinas = Disiplina.objects.all()
    listaReservas=Reserva.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos,'verInstalacion':verinstalacion, 'disiplinas': listaDisiplinas,'reservas':listaReservas}
    return render(request, 'vista_reserva.html',data)

def adminDisiplinas(request):
    busqueda= request.GET.get("buscardisiplina")
    listaDisiplinas = Disiplina.objects.all()

    if busqueda:
        listaDisiplinas=Disiplina.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()
    return render(request, 'adminDisiplinas.html',{'disiplinas': listaDisiplinas})

def registroDisiplina(request):
    nombre = request.POST['disnombre']

    Disiplina.objects.create(
        nombre=nombre,
    )
    return redirect('/adminDisiplinas')

def editaDisiplina(request,id):
    ediciondisiplina = Disiplina.objects.get(id=id)
    return render(request, 'edicionDisiplinas.html', {'edicionDisiplina': ediciondisiplina})

def edicionDisiplinas(request):
    id=request.POST['disiplinaid']
    disiplina = Disiplina.objects.get(id=id)

    if request.POST:
        disiplina=Disiplina()
        disiplina.id = request.POST.get('disiplinaid')
        disiplina.nombre = request.POST.get('disiplinanombre')
        disiplina.save()
    return redirect('/adminDisiplinas')

def eliminacionDisiplina(request,id):
    disiplina=Disiplina.objects.get(id=id)
    disiplina.delete()
    
    return redirect('/adminDisiplinas')    

def adminInstalaciones(request):
    listaDisiplinas = Disiplina.objects.all()
    listaInstalaciones = Instalacion.objects.all()
    busqueda= request.GET.get("buscarinstalacion")

    if busqueda:
        listaInstalaciones=Instalacion.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()

    return render(request, 'adminInstalaciones.html',{'disiplinas': listaDisiplinas,'instalaciones': listaInstalaciones})

def registroInstalacion(request):
    nombre = request.POST['nombre']

    disiplina=Disiplina()
    disiplina.id = int(request.POST['disiplina'])
    disiplina_instalacion=disiplina

    #precio = request.POST['precio']
    #capacidad = request.POST['capacidad']
    foto = request.FILES['imagen']
    descripcion = request.POST['descripcion']
    #indumentaria = request.POST['indumentaria']
    #recomendaciones = request.POST['recomendaciones']
    restricciones = request.POST['restricciones']
    #equipo_incluido = request.POST['equipo_incluido']
    

    Instalacion.objects.create(
        nombre=nombre,
        id_diciplina=disiplina_instalacion,
        descripcion=descripcion,
        restriciones=restricciones,
        #precio=precio,
        #capacidad=capacidad,
        imagen=foto,
        #indumentaria=indumentaria,
        #recomendaciones=recomendaciones,
        #equipo_incluido=equipo_incluido,
    )
    return redirect('/adminInstalaciones')


def verInstalacion(request,id):
    verinstalacion = Instalacion.objects.get(id=id)
    listaDisiplinas = Disiplina.objects.all()
    listaReservas=Reserva.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos, 'verInstalacion':verinstalacion,'disiplinas': listaDisiplinas,'reservas':listaReservas}
    
    return render(request, 'verInstalaciones.html',  data)

def editaInstalacion(request,id):
    edicioninstalacion = Instalacion.objects.get(id=id)
    imagen=edicioninstalacion.imagen
    if request.POST:
        if request.POST.get('imagen')=='':
            instalacion=Instalacion()
            instalacion.id = edicioninstalacion.id
            instalacion.nombre=request.POST.get('nombre')
            
            disiplina=Disiplina()
            disiplina.id=request.POST.get('disiplina')
            instalacion.id_diciplina=disiplina

            #instalacion.precio=request.POST.get('precio')
            #instalacion.capacidad=request.POST.get('capacidad')
            instalacion.imagen=imagen
            instalacion.descripcion=request.POST.get('descripcion')
            #instalacion.indumentaria=request.POST.get('indumentaria')
            #instalacion.recomendaciones=request.POST.get('recomendaciones')
            instalacion.restriciones=request.POST.get('restricciones')
            #instalacion.equipo_incluido=request.POST.get('equipo_incluido')

            instalacion.save()
        else:
            instalacion=Instalacion()
            instalacion.id = edicioninstalacion.id
            instalacion.nombre=request.POST.get('nombre')
            
            disiplina=Disiplina()
            disiplina.id=request.POST.get('disiplina')
            instalacion.id_diciplina=disiplina

           # instalacion.precio=request.POST.get('precio')
            #instalacion.capacidad=request.POST.get('capacidad')
            instalacion.imagen=request.FILES.get('imagen')
            #instalacion.descripcion=request.POST.get('descripcion')
            #instalacion.indumentaria=request.POST.get('indumentaria')
            instalacion.recomendaciones=request.POST.get('recomendaciones')
            instalacion.restriciones=request.POST.get('restricciones')
            #instalacion.equipo_incluido=request.POST.get('equipo_incluido')

            instalacion.save()

    return redirect('/verInstalacion/'+str(instalacion.id))

def eliminacionInstalacion(request,id):
    instalacion=Instalacion.objects.get(id=id)
    instalacion.delete()
    
    return redirect('/adminInstalaciones') 

def adminReservas(request):
    listaReserva = Reserva.objects.all()
    # lo transforma en json
    serialized_data = serializers.serialize('json', listaReserva)
    deserialized_data = json.loads(serialized_data)
    # fields son los datos que limpiamos de la base de datos
    listaNueva = [_["fields"] for _ in deserialized_data]
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
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos, 'reservas':listaForm}
    return render(request, 'adminReservas.html', data)

def registroReservas(request,id):
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    ci = request.POST['ci']
    telefono = request.POST['telefono']
    correo = request.POST['correo']

    instalacion=Instalacion()
    instalacion.id = int(id)
    instalacion_reserva=instalacion

    codigo=str(request.POST['apellido'])+str(request.POST['ci'])+str(request.POST['telefono']) 
    cantidad = request.POST['cantidad']

    fecha_reserva = request.POST['fecha_reserva']
    Presentaciones = request.POST['Presentaciones']
    Productos = request.POST['Productos']
    

    Reserva.objects.create(
        nombres=nombre,
        apellidos=apellido,
        cedula=ci,
        telefono=telefono,
        email=correo,
        id_instalacion=instalacion_reserva,
        fecha_compra=fecha_reserva,
        codigo_qr=codigo,
        cantidad=cantidad,
        Presentaciones=Presentaciones,
        Productos=Productos,

        
    )
    
    return redirect('/instalaciones')



def validarFecha(request):
    fecha = request.GET.get('fecha_reserva', None)
    data = {
        'is_taken': Reserva.objects.filter(fecha_compra=fecha).exists()
    }
    
    return JsonResponse(data)
