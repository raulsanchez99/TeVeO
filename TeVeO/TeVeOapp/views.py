from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404

from .models import Camera, Comment, Token
from .forms import ConfigForm
from .camaras import *  # Importar todas las funciones de media_operations
from .configuration import *

from django.utils import timezone
import time

from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.cache import never_cache
from django.urls import reverse

from urllib.parse import urlparse, parse_qs

# Create your views here.

def config(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            font_size = form.cleaned_data['font_size']
            font_family = form.cleaned_data['font_family']
            request.session['username'] = username
            request.session['font_size'] = font_size
            request.session['font_family'] = font_family
            user, created = User.objects.get_or_create(username=username)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    token.token = default_token_generator.make_token(user)
                token.font_size = font_size
                token.font_family = font_family
                token.save()
                request.session['auth_token'] = token.token
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        form = ConfigForm()

    username, font_size, font_family = userConfiguration(request)

    context = {
        'form': form,
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'config.html', context)


def index(request):
    # Manejo de la sesion del usuario
    username, font_size, font_family = userConfiguration(request)

    # Odenar los comentario por tiempo
    order = 'desc'
    if request.method == 'POST':
        order = request.POST.get('order', 'desc')

    comments = ordenarCamarasFecha(order)

    # Crear el contexto
    context = {
        'comments': comments,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }

    # Importante hacer con render y no con HttpResponse porque render es mas
    # seguro y maneja mejor los errores
    return render(request, 'index.html', context)


@never_cache
def camaras(request):
    # Obtener las fuentes de datos disponibles en static/xml
    random_img = None
    order = 'desc'
    if request.method == 'POST':
        xml_selected = request.POST.get(f'{"selected_xml"}')
        order = request.POST.get('order', 'desc')
        if xml_selected == "clean":
            limpiar_camaras()
        elif xml_selected is not None:
            print(f"XML seleccionado: {xml_selected}")
            cargar_camaras(xml_selected)
            get_img(xml_selected)

    cameras = ordenarCamarasComentarios(order)

    username, font_size, font_family = userConfiguration(request)
    # print(f"Username en mainCameras: {username},
    # Font size: {font_size}, Font family: {font_family}")

    random_img = get_imagen_aleatoria()
    xml_files = get_xml()

    context = {
        'request': request,
        'xml_files': xml_files,
        'random_img': random_img,
        'cameras': cameras,
        'cameras_count': cameras.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'paginaCamaras.html', context)


def pag_camaras(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.

    # Obtener la cámara con el id indicado
    camera = Camera.objects.filter(id=id).first()

    if camera is None:
        return HttpResponse("Cámara no encontrada")

    # Ordenar los comentarios por tiempo
    order = 'desc'
    if request.method == 'POST':
        order = request.POST.get('order', 'desc')

    # Obtener todos los comentarios de la camera ordenados por fecha
    comments = ordenarComentariosFecha(
        Comment.objects.filter(camera=camera), order)

    # Obtener el nombre de usuario, tamaño de fuente y familia de fuentes
    username, font_size, font_family = userConfiguration(request)

    context = {
        'request': request,
        'camera': camera,
        'comments': comments,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }

    return render(request, 'camaras.html', context)

# Funcion para guardar un comentario si se ha hecho un post request


def guardar_comentario(request, camera, name):
    comment_text = request.POST.get('body')  # Cambiar 'cuerpo' a 'body'
    if comment_text:  # Verificar si comment_text no es vacío
        # Guardar el comentario en la base de datos con la camara, comentario,
        # fecha y la imagen de la cámara en ese momento
        img_comment = guardar_comentarios(camera.img_path)
        comment = Comment(name=name, camera=camera, comment=comment_text,
                          date=timezone.now(), img_path_comment=img_comment)
        comment.save()


def ver_comentarios(request):
    camera_id = request.GET.get('camera_id')
    camera = Camera.objects.filter(id=camera_id).first()
    username, font_size, font_family = userConfiguration(request)

    if camera is None:
        return HttpResponse("Cámara no encontrada")

    if request.method == 'POST':
        guardar_comentario(request, camera, username)

    # Obtener todos los comentarios de la camera de más reciente a más
    # antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'comentarios.html', context)


def camara_id(request, id):
    # Seleccionar la cámara con el identificador indicado. Si no existe, se
    # mostrará un mensaje de error. En caso contrario, se mostrará la imagen
    # de la cámara, y un enlace para volver al listado de cámaras.
    camera = Camera.objects.filter(id=id).first()
    username, font_size, font_family = userConfiguration(request)

    if camera is None:
        return HttpResponse("Cámara no encontrada")

    camera.img_path = get_imagen_actual(id)
    print(f"Imagen actual: {camera.img_path}")

    if request.method == 'POST':
        guardar_comentarios(request, camera, username)

    # Obtener todos los comentarios de la camera de más reciente a más
    # antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')
    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'now': timezone.now(),
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
    }
    return render(request, 'camara_id.html', context)


def get_url(img_path):
    """
    Obtiene la URL de la última imagen, añadiendo un
    parámetro de tiempo para evitar el caché del navegador.
    """
    if img_path is None:
        print("No se encontró ninguna imagen")
        return None

    return img_path + '?t=' + str(time.time())


def get_imagen(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")

    img_path = get_imagen_actual(id)
    context = {
        'request': request,
        'camera': camera,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
        'latest_image_url': get_url(img_path),
    }
    return render(request, 'imagen.html', context)


def cargar_comentarios(request, id):
    camera = Camera.objects.filter(id=id).first()
    if camera is None:
        return HttpResponse("Cámara no encontrada")

    # Obtener todos los comentarios de la camera de más reciente a más
    # antiguo
    comments = Comment.objects.filter(camera=camera).order_by('-date')

    context = {
        'request': request,
        'comments': comments,
        'camera': camera,
        'now': timezone.now(),
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'cargar_comentarios.html', context)


def camara_json(request, id):
    try:
        cam = Camera.objects.get(id=id)
    except Camera.DoesNotExist:
        raise Http404("Cámara no disponible")

    # Obtener los comentarios de la cámara
    comments = Comment.objects.filter(camera=cam)

    # Serializar los comentarios a JSON
    comments_json = serializers.serialize('json', comments)

    data = {
        'id': cam.id,
        'source_id': cam.source_id,
        'src': cam.src,
        'img_path': cam.img_path,
        'num_comments': comments.count(),
        'comments': comments_json,
    }
    return JsonResponse(data)


def camaras_json(request):
    cameras = Camera.objects.all()
    data = []
    for cam in cameras:
        # Obtener los comentarios de la cámara
        comments = Comment.objects.filter(camera=cam)

        # Serializar los comentarios a JSON
        comments_json = serializers.serialize('json', comments)

        data.append({
            'id': cam.id,
            'source_id': cam.source_id,
            'src': cam.src,
            'img_path': cam.img_path,
            'num_comments': comments.count(),
            'comments': comments_json,
        })
    return JsonResponse(data, safe=False)


def help(request):
    username, font_size, font_family = userConfiguration(request)
    context = {
        'username': username,
        'font_size': font_size,
        'font_family': font_family,
        'cameras_count': Camera.objects.count(),
        'comments_count': Comment.objects.count(),
    }
    return render(request, 'help.html', context)


def token_sesion(request):
    auth_token = request.session.get('auth_token')
    if auth_token is None:
        # Si no hay un token de autenticación, crea uno
        user = User.objects.get(username=request.session['username'])
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.token = default_token_generator.make_token(user)
            token.font_size = request.session['font_size']
            token.font_family = request.session['font_family']
            token.save()
        auth_token = token.token
        request.session['auth_token'] = auth_token
    auth_link = request.build_absolute_uri(
        reverse('set_session')) + f'?auth_token={auth_token}'
    return JsonResponse({'auth_link': auth_link})


def config_sesion(request):
    if request.method == 'POST':
        auth_link = request.POST.get('auth_link')
        if auth_link is not None:
            url = urlparse(auth_link)
            auth_token = parse_qs(url.query).get('auth_token', [None])[0]
            if auth_token is not None:
                try:
                    token = Token.objects.get(token=auth_token)
                    request.session['username'] = token.user.username
                    request.session['font_size'] = token.font_size
                    request.session['font_family'] = token.font_family
                    print(f"Nombre de usuario: {token.user.username}")
                    print(f"Tamaño de fuente: {token.font_size}")
                    print(f"Familia de fuentes: {token.font_family}")

                except Token.DoesNotExist:
                    messages.error(
                        request, 'El enlace de autorización no es válido.')
    return redirect('index')

