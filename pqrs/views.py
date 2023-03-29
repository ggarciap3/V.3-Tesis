from django.shortcuts import render,redirect
from django.core import serializers
from pqrs.models import Categoriapq,Tipospq, Ingresopq, opciones_Presentaciones, opciones_Productos
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
import ModulPQRS.settings as setting
import json
# librerias para el correo electrónico
import yagmail
from django.core.files.storage import FileSystemStorage

import matplotlib.pyplot as plt
from django.db.models import Count,Sum
import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required

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
        context['title']="Iniciar Sesión"
        return context

class chatbotView(LoginView):
    template_name ='chatbot.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['title']="Iniciar Sesión"
        return context

class tipospqsView(LoginView):
    template_name ='tipospqs.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        listaTipospqs = Tipospq.objects.all()
        context=super().get_context_data(**kwargs)
        context['title']="Iniciar Sesión"
        context['tipospqs']=listaTipospqs
        return context
    
def chatbot(request):
    return render(request, 'chatbot.html')

def tipospqs(request):
    listaTipospqs = Tipospq.objects.all()
    return render(request, 'tipospqs.html',{'tipospqs': listaTipospqs})


def detalleTipospq(request,id):
    vertipospq = Tipospq.objects.get(id=id)
    listaCategoriapqs = Categoriapq.objects.all()
    listaIngresopqs=Ingresopq.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos,'verTipospq':vertipospq, 'categoripqs': listaCategoriapqs,'ingresopqs':listaIngresopqs}
    return render(request, 'vista_ingresopq.html',data)

@login_required
def adminCategoriapqs(request):
    busqueda= request.GET.get("buscarcategoriapq")
    listaCategoriapqs = Categoriapq.objects.all()

    if busqueda:
        listaCategoriapqs=Categoriapq.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()
    return render(request, 'adminCategoriapqs.html',{'categoriapqs': listaCategoriapqs})

@login_required
def registroCategoriapq(request):
    nombre = request.POST['disnombre']

    Categoriapq.objects.create(
        nombre=nombre,
    )
    return redirect('/adminCategoriapqs')

@login_required
def editaCategoriapq(request,id):
    edicioncategoriapq = Categoriapq.objects.get(id=id)
    return render(request, 'edicionCategoriapqs.html', {'edicionCategoriapq': edicioncategoriapq})

@login_required
def edicionCategoriapqs(request):
    id=request.POST['categoriapqid']
    categoriapq = Categoriapq.objects.get(id=id)

    if request.POST:
        categoriapq=Categoriapq()
        categoriapq.id = request.POST.get('categoriapqid')
        categoriapq.nombre = request.POST.get('categoriapqnombre')
        categoriapq.save()
    return redirect('/adminCategoriapqs')

@login_required
def eliminacionCategoriapq(request,id):
    categoriapq=Categoriapq.objects.get(id=id)
    categoriapq.delete()
    
    return redirect('/adminCategoriapqs')    

@login_required
def adminTipospqs(request):
    listaCategoriapqs = Categoriapq.objects.all()
    listaTipospqs = Tipospq.objects.all()
    busqueda= request.GET.get("buscartipospq")

    if busqueda:
        listaTipospqs=Tipospq.objects.filter(
            nombre__icontains=busqueda 
        ).distinct()

    return render(request, 'adminTipospqs.html',{'categoriapqs': listaCategoriapqs,'tipospqs': listaTipospqs})

@login_required
def registroTipospq(request):
    nombre = request.POST['nombre']

    categoriapq=Categoriapq()
    categoriapq.id = int(request.POST['categoriapq'])
    categoriapq_tipospq=categoriapq
    foto = request.FILES['imagen']
    descripcion = request.POST['descripcion']
    #restricciones = request.POST['restricciones']

    Tipospq.objects.create(
        nombre=nombre,
        id_categoriap=categoriapq_tipospq,
        descripcion=descripcion,
        #restriciones=restricciones,
        imagen=foto,

    )
    return redirect('/adminTipospqs')


def verTipospq(request,id):
    vertipospq = Tipospq.objects.get(id=id)
    listaCategoriapqs = Categoriapq.objects.all()
    listaIngresopqs=Ingresopq.objects.all()
   
    data = {'horarioI':opciones_Presentaciones, 'horarioF':opciones_Productos, 'verTipospq':vertipospq,'categoriapqs': listaCategoriapqs,'ingresopqs':listaIngresopqs}
    
    return render(request, 'verTipospqs.html',  data)

@login_required
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
            #tipospq.restriciones=request.POST.get('restricciones')
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
            #tipospq.restriciones=request.POST.get('restricciones')
            tipospq.save()

    return redirect('/verTipospq/'+str(tipospq.id))

@login_required
def eliminacionTipospq(request,id):
    tipospq=Tipospq.objects.get(id=id)
    tipospq.delete()
    
    return redirect('/adminTipospqs') 

@login_required
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

    # filtrar por nombre si hay una búsqueda
    busqueda = request.GET.get("buscarres")
    if busqueda:
        listaNueva = [d for d in listaNueva if busqueda.lower() in d["nombres"].lower()]
        if not listaNueva:
            # si no se encontraron resultados, volver a cargar todos los elementos
            listaNueva = [{'pk': i.pk, **i.__dict__} for i in listaIngresopq]

    listaForm = []
    for d in listaNueva:
        for pre in opciones_Presentaciones:
            if d["Presentaciones"] == pre[0]:
                d["Presentaciones"] = pre[1]
                
        for pro in opciones_Productos:
            if d["Productos"] == pro[0]:
                d["Productos"] = pro[1]
            
        listaForm.append(d)

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
    lote = request.POST['lote']
    descrip = request.POST['descrip']
    cantidad = request.POST['cantidad']

    fecha_compra = request.POST['fecha_compra']
    Presentaciones = request.POST['Presentaciones']
    Productos = request.POST['Productos']
    foto = request.FILES['evidencia']
    

    Ingresopq.objects.create(
        nombres=nombre,
        apellidos=apellido,
        cedula=ci,
        telefono=telefono,
        email=correo,
        id_tipospq=tipospq_ingresopq,
        fecha_compra=fecha_compra,
        lote=lote,
        descrip=descrip,
        cantidad=cantidad,
        Presentaciones=Presentaciones,
        Productos=Productos,
        evidencia=foto,

    )
    mensaje = f"""Estimado equipo de Servicio al cliente,

    Se ha registrado una nueva queja/reclamo a nombre del cliente {nombre} {apellido} con CI número {ci} con la descripción {descrip}. 
    Para dar atención a la información registrada por el cliente ingrese con sus credenciales a la página corporativa.

    Wall-eat."""
    enviar_correo(mensaje)
    return redirect('/tipospqs')
# metodo para enviar correo
def enviar_correo(mensaje:str):
    lista_correos = User.objects.values_list('email', flat=True)
    para = list(lista_correos);
    yag = yagmail.SMTP("wall.eat.co@gmail.com", "rcundbofzdotxfbv")
    body = mensaje
    # para = ["axha0188@gmail.com", "arongarcia558@gmail.com"]
    yag.send(to=para, subject="Ingreso de quejas y reclamos", contents=body)

@login_required
#lista de ingresos
def editaIngresopq(request,id):
    edicioningresopqs = Ingresopq.objects.get(id=id)
    return render(request, 'edicionIngresopqs.html', {'edicionIngresopqs': edicioningresopqs})
@login_required
def edicionIngresopqs(request, id):
    ingresopq = Ingresopq.objects.get(id=id)
    return render(request, 'edicionIngresopqs.html', {'ingresopq': ingresopq})
@login_required
def actualizar_estado(request, id):
    ingresopq = Ingresopq.objects.get(id=id)
    if request.method == 'POST':
        estado = request.POST.get('estado', False)
        if estado == 'on':
            ingresopq.estado = True
            ingresopq.save()
            if ingresopq.email and ingresopq.estado:
                nombres = ingresopq.nombres
                apellidos = ingresopq.apellidos
                mensaje = f"Estimado/a {nombres} {apellidos},\n\nReciba un cordial saludo de parte del departamento de Servicio al cliente de Wall-eat. Queremos confirmarle que hemos recibido de manera exitosa su queja/reclamo y agradecemos el tiempo que se ha tomado para contarnos su experiencia y hacernos saber su preocupación. \n\nNos tomamos muy en serio su experiencia y queremos asegurarnos de que sea abordada de manera adecuada y eficiente. Para ello, hemos iniciado una investigación sobre su caso para poder identificar cualquier problema o error que haya surgido en el proceso y tomar las medidas necesarias para solucionarlo.\n\nSu satisfacción es nuestra prioridad y haremos todo lo posible para resolver este problema. Esperamos tener una solución para su caso en el menor tiempo posible y lo mantendremos actualizado/a sobre cualquier avance.\n\nAtentamente,\nServicio al cliente Wall-eat"
                yag = yagmail.SMTP("wall.eat.co@gmail.com", "rcundbofzdotxfbv")
                yag.send(to=ingresopq.email, subject="Respuesta a ingreso de queja/reclamo", contents=mensaje)
        else:
            ingresopq.estado = False
            ingresopq.save()
        return redirect('edicionIngresopqs', id=id)
    else:
        print("Error")
    return render(request, 'edicionIngresopqs.html', { 'ingresopq': ingresopq})

@login_required
def subir_doc(request):
    ingresopqs = Ingresopq.objects.all()
    return render(request, 'subir_doc.html', {'ingresopqs': ingresopqs})
@login_required
def edicionPdf(request, id):
    ingresopq = Ingresopq.objects.get(id=id)

    if request.method == 'POST':
        ingresopq.doc = request.FILES.get('doc', ingresopq.doc)  # actualizar documento
        archivopfd = request.FILES['doc']
        ingresopq.estadodoc = request.POST.get('estadodoc') == 'on'  # actualizar estado del documento
        ingresopq.save()
        ruta_archivo = default_storage.save('pdfqueja.pdf', archivopfd)
        # print(ingresopq.doc)
        if ingresopq.email and ingresopq.estadodoc:
            # obtiene la ruta completa del archivo almacenado
            ruta_completa_archivo = default_storage.path(ruta_archivo)
            mensaje = f"Estimado/a {ingresopq.nombres} {ingresopq.apellidos},\n\nNos complace informarle que hemos resuelto su queja de manera satisfactoria y queremos agradecerle por su paciencia durante todo este proceso.\n\nNuestro equipo ha trabajado diligentemente para resolver el problema que experimentó, por lo que hemos tomado las medidas para asegurarnos de que no vuelva a suceder en el futuro. Esperamos que pueda sentirse satisfecho/a con nuestros productos/servicios una vez más.\n\nSi tiene alguna otra inquietud o pregunta, no dude en ponerse en contacto con nosotros a través de este mismo correo electrónico o mediante nuestra línea de atención al cliente.\n\nAtentamente,\n\nServicio al cliente Wall-eat"
            adjunto = ruta_completa_archivo
            yag = yagmail.SMTP("wall.eat.co@gmail.com", "rcundbofzdotxfbv")
            yag.send(to=ingresopq.email, subject="Solución a queja/reclamo", contents=mensaje,attachments=adjunto)
            
        return redirect('subir_doc')

    return render(request, 'edicionPdf.html', {'ingresopq': ingresopq})

@login_required
def verIngresopqs(request, id):
    ingresopq = Ingresopq.objects.get(id=id)
    return render(request, 'verIngresopqs.html', {'ingresopq': ingresopq})

@login_required
def admin_dash(request):
    # Obtener los registros de Ingresopq
    ingresos = Ingresopq.objects.all()
    # Obtener el número total de registros
    total = ingresos.count()
    cantidad = ingresos.count()
    # Obtener el número de registros con estado "True" y "estadodoc" "True"
    totalR = Ingresopq.objects.filter(estado=True).count()
    totalT = Ingresopq.objects.filter(estadodoc=True).count()
    totalN = Ingresopq.objects.filter(estado=False).count()

    totalQ = Ingresopq.objects.filter(id_tipospq=1).count()
    totalRe = Ingresopq.objects.filter(id_tipospq=2).count()
    
    
    total_cantidad = Ingresopq.objects.aggregate(Sum('cantidad'))['cantidad__sum']

    # Crear el gráfico de barras para "Estados de la queja/reclamo"
     
    fig_estado = go.Figure(go.Bar(
            x=[totalR, totalT, totalN],
            y=['En revisión', 'Revisado', 'No revisado'],
            orientation='h',
            marker_color=['lightskyblue', '#CD5C5C', 'lightcoral']
        ),
        layout_title='Registros por estado y estado de documento'
)

    # Obtener el número de registros para cada valor de "id_tipospq"
    counts_tipospq = Ingresopq.objects.values('id_tipospq').annotate(count=Count('id_tipospq'))

    # Convertir el QuerySet en una lista
    ls_tipospq = []
    for item in counts_tipospq:
        ls_tipospq.append(item['id_tipospq'])
    # Obtener los nombres de Tipospq correspondientes a cada valor de "id_tipospq"
    tipospq_objs = Tipospq.objects.filter(id__in=ls_tipospq)
    tipospq_dict = {tp.id: tp.nombre for tp in tipospq_objs}
    ls_tipospq_names = [tipospq_dict.get(id_tipospq, id_tipospq) for id_tipospq in ls_tipospq]
    # Crear el gráfico de barras para "id_tipospq"
    fig_tipospq = go.Figure(
        go.Bar(
            x=ls_tipospq_names,
            y=[item['count'] for item in counts_tipospq],
            marker_color=['#1b004b','#7f00b2']
        ),
        layout_title='Registros por tipos novedad'
    )


    
    # Obtener el número de registros para cada valor de "Productos"
    counts_productos = ingresos.values('Productos').annotate(count=Count('Productos'))
    # Convertir el QuerySet en una lista
    ls_productos = []
    for item in counts_productos:
        if item['Productos'] == 1:
            ls_productos.append('Azucar Blanca')
        elif item['Productos'] == 2:
            ls_productos.append('Azucar Morena')
        elif item['Productos'] == 3:
            ls_productos.append('Azucar Ligero')
        elif item['Productos'] == 4:
            ls_productos.append('Azucar Turbinado')
        elif item['Productos'] == 5:
            ls_productos.append('Azucar Blanco Organico')
        elif item['Productos'] == 6:
            ls_productos.append('Azucar De Coco Organico')
        elif item['Productos'] == 7:
            ls_productos.append('Panela')
        elif item['Productos'] == 8:
            ls_productos.append('Steviazucar Blanca')
        elif item['Productos'] == 9:
            ls_productos.append('Steviazucar Morena')
        elif item['Productos'] == 10:
            ls_productos.append('Stevia Panela')

    # Crear el gráfico de pastel para "Productos"
    fig_productos = go.Figure(
        go.Pie(
            labels=ls_productos,
            values=[item['count'] for item in counts_productos]
        ),
        layout_title='Registros por productos'
    )

    # Generar el HTML de los gráficos
    plotly_html_estado = fig_estado.to_html(full_html=False)
    plotly_html_productos = fig_productos.to_html(full_html=False)
    plotly_html_tipospq = fig_tipospq.to_html(full_html=False)
    
    # Crear el diccionario de contexto y renderizar el template
    context = {
        'total': total,
        'total_cantidad': total_cantidad,
        'cantidad': cantidad,
        'totalR': totalR,
        'totalT': totalT,
        'totalN': totalN,

        'totalQ': totalQ,
        'totalRe' : totalRe,

        'plotly_html_estado': plotly_html_estado,
        'plotly_html_tipospq': plotly_html_tipospq,
        'plotly_html_productos': plotly_html_productos,
    }
    return render(request, 'admin_dash.html', context)