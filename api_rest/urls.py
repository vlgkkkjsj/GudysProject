from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name='home'),
    path('cadastrar/',cadastrar, name='cadastrar'),
    path('salvar/', salvar, name='salvar'),
    path('logar/', logar, name='logar'),
    path('homeLog/', homeLog, name='homeLog'),
    path('logged/', sideSuperUser, name = 'sideSuperUser'),
    path('editar/<int:id>',editar,name='editar'),
    path('update/<int:id>',update , name='update'),
    path('delete/<int:id>',delete ,name='delete'),
    path('listar/', listar, name='listar'),
    path('adminList/', listarAdmin, name='listarAdmin'),
    path('submitRelatorio/', submitRelatorio, name='submitRelatorio'),
    path('redirectRelatorio/', redirectRelatorio, name='redirectRelatorio'),
    path('historicoRelatorios', historicoRelatorios, name='historicoRelatorios'),
    path('relatorio/<int:relatorio_id>/', detalheRelatorio, name='detalheRelatorio'),
    path('redirectList/', redirectList, name='redirectList'),
    path('cadAdmin/', cadAdmin, name='cadAdmin'),
    path('redirectRpp/', redirectRpp, name='redirectRpp'),
    path('rppList/', rppList, name='rppList'),
    path('relatorios/', custom_logout, name='logout'),
]
