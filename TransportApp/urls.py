from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),

    path('listmasini', views.listmasini, name = 'listmasini'),
    path('addcar', views.addcar, name = 'addcar'),
    path('deletecar/<int:id>', views.deletecar, name = 'deletecar'),
    path('updatecar/<int:id>', views.updatecar, name = 'updatecar'),

    path('listgaraje', views.listgaraje, name = 'listgaraje'),
    path('addgaraj', views.addgaraj, name = 'addgaraj'),
    path('deletegaraj/<int:id>', views.deletegaraj, name = 'deletegaraj'),
    path('updategaraj/<int:id>', views.updategaraj, name = 'updategaraj'),

    path('listorase', views.listorase, name = 'listorase'),
    path('addoras', views.addoras, name = 'addoras'),
    path('deleteoras/<int:id>', views.deleteoras, name = 'deleteoras'),
    path('updateoras/<int:id>', views.updateoras, name = 'updateoras'),

    path('listsoferi', views.listsoferi, name = 'listsoferi'),
    path('addsofer', views.addsofer, name = 'addsofer'),
    path('deletesofer/<int:id>', views.deletesofer, name = 'deletesofer'),
    path('updatesofer/<int:id>', views.updatesofer, name = 'updatesofer'),

    path('listproducatori', views.listproducatori, name = 'listproducatori'),
    path('addproducator', views.addproducator, name = 'addproducator'),
    path('deleteproducator/<int:id>', views.deleteproducator, name = 'deleteproducator'),
    path('updateproducator/<int:id>', views.updateproducator, name = 'updateproducator'),

    path('listmodele', views.listmodele, name = 'listmodele'),
    path('addmodel', views.addmodel, name = 'addmodel'),
    path('deletemodel/<int:id>', views.deletemodel, name = 'deletemodel'),
    path('updatemodel/<int:id>', views.updatemodel, name = 'updatemodel'),

    path('listasiguratori', views.listasiguratori, name = 'listasiguratori'),
    path('addasigurator', views.addasigurator, name = 'addasigurator'),
    path('deleteasigurator/<int:id>', views.deleteasigurator, name = 'deleteasigurator'),
    path('updateasigurator/<int:id>', views.updateasigurator, name = 'updateasigurator'),

    path('listconduce', views.listconduce, name = 'listconduce'),
    path('addconduce', views.addconduce, name = 'addconduce'),
    path('deleteconduce/<int:id_masina>/<int:id_sofer>/', views.deleteconduce, name = 'deleteconduce'),
    path('updateconduce/<int:id_masina>/<int:id_sofer>/', views.updateconduce, name = 'updateconduce'),

    path('listasigura', views.listasigura, name = 'listasigura'),
    path('addasigura', views.addasigura, name = 'addasigura'),
    path('deleteasigura/<int:id_masina>/<int:id_asigurator>/', views.deleteasigura, name = 'deleteasigura'),
    path('updateasigura/<int:id_masina>/<int:id_asigurator>/', views.updateasigura, name = 'updateasigura'),

    path('verifica_asigurare', views.verifica_asigurare, name = 'verifica_asigurare'),

    path('nrsoferi', views.nrsoferi, name = 'nrsoferi'),

    path('orasemasini', views.orase_masini, name = 'orasemasini'),
    path('updateorasemasini/<int:id>', views.update_orase_masini, name = 'updateorasemasini'),
    path('deleteorasemasini/<int:id>', views.delete_orase_masini, name = 'deleteorasemasini'),
    path('addorasemasini', views.add_orase_masini, name = 'addorasemasini'),
    
    path('nrvehicule', views.nrvehicule, name = 'nrvehicule')
]