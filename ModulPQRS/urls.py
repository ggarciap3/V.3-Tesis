"""ModulPQRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from pqrs import views
from pqrs.views import LoginFormView,LogoutView
from django.conf import settings

from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),
    path('', LoginFormView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name="logout"),

    path('tipospqs/', views.tipospqs, name='tipospqs'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('detalleTipospq/<id>', views.detalleTipospq, name='detalleTipospq'),

    path('adminCategoriapqs/', views.adminCategoriapqs, name='adminCategoriapqs'),
    path('registroCategoriapq/', views.registroCategoriapq, name='registroCategoriapq'), 
    path('edicionCategoriapqs/', views.edicionCategoriapqs, name='edicionCategoriapqs'),
    path('editaCategoriapq/<id>', views.editaCategoriapq, name='editaCategoriapq'),
    path('eliminacionCategoriapq/<id>', views.eliminacionCategoriapq, name='eliminacionCategoriapq'),
     

    path('adminTipospqs/', views.adminTipospqs, name='adminTipospqs'),
    path('registroTipospq/', views.registroTipospq, name='registroTipospq'), 
    
    path('verTipospq/<id>', views.verTipospq, name='verTipospq'),
    path('editaTipospq/<id>', views.editaTipospq, name='editaTipospq'),
    path('eliminacionTipospq/<id>', views.eliminacionTipospq, name='eliminacionTipospq'),
   
    path('adminIngresopqs/', views.adminIngresopqs, name='adminIngresopqs'),
    path('registroIngresopqs/<id>', views.registroIngresopqs, name='registroIngresopqs'), 

     #lista de ingreso
    path('editaIngresopq/<id>', views.editaIngresopq, name='editaIngresopq'),   
    path('ingresopq/<id>/', views.edicionIngresopqs, name='edicionIngresopqs'),
    #Actualizar estado
    path('actualizar_estado/<id>', views.actualizar_estado, name='actualizar_estado'),

    #Validaciones 
    re_path(r'^validarFecha/$', views.validarFecha, name='validarFecha'),
    
   ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
