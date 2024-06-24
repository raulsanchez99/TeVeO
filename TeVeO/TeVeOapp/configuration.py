from .models import Camera, Comment
from django.db.models import Count

#Configuracion del usuario por defecto
DEFAULT_FONT_SIZE = "default_font_size"
DEFAULT_FONT_FAMILY = "default_font_family"
DEFAULT_NAME = "Anonimo"

def fontSize(request):
    size = request.session.get('font_size')
    if size == "small":
        font_size = "font-size-pequena"
    elif size == "large":
        font_size = "font-size-grande"
    else:
        font_size = DEFAULT_FONT_SIZE
    # print(f"Size: {font_size}")
    return font_size


def fontFamily(request):
    family = request.session.get('font_family')
    if family == "Arial":
        font_family = "font-family-arial"
    elif family == "Times New Roman":
        font_family = "font-family-times"
    elif family == "Courier New":
        font_family = "font-family-courier"
    else:
        font_family = DEFAULT_FONT_FAMILY
    return font_family

def userLogin(request):
    username = request.session.get('username')
    if username == "" or username is None:
        username = DEFAULT_NAME
    return username

def userConfiguration(request):
    font_size = fontSize(request)
    font_family = fontFamily(request)
    name = userLogin(request)
    return name, font_size, font_family


def ordenarCamarasComentarios(order):
    order_field = 'num_comments' if order == 'asc' else '-num_comments'
    return Camera.objects.annotate(
        num_comments=Count('comment')).order_by(order_field)


def ordenarCamarasFecha(order):
    order_field = 'date' if order == 'asc' else '-date'
    return Comment.objects.order_by(order_field)


def ordenarComentariosFecha(comments, order):
    order_field = 'date' if order == 'asc' else '-date'
    return comments.order_by(order_field)
