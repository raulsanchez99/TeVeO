from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('camaras/', views.camaras, name='mainCameras'),
    path('camaras/json', views.camaras_json, name='cameras_json'),
    path('camaras/<str:id>/', views.pag_camaras, name='camera'),
    path('camaras/<str:id>/comment', views.cargar_comentarios, name='get_comments'),
    path('camaras/<str:id>/dyn', views.camara_id, name='camera_dyn'),
    path('camaras/<str:id>/img', views.get_imagen, name='latest_image'),
    path('camaras/<str:id>/json', views.camara_json, name='camera_json'),
    path('comentario/', views.ver_comentarios, name='comment'),
    path('config/', views.config, name='config'),
    path('config/auth_link', views.token_sesion, name='auth_link'),
    path('config/set_session', views.config_sesion, name='set_session'),
    path('help/', views.help, name='ayuda'),
]
