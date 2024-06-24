from .models import Camera

import os
import re
import requests
import random
import xml.dom.minidom

# id de los 4 arcchivos
id_listado1 = 'LIS1-'
id_listado2 = 'LIS2-'
id_cctv = 'CCTV-'
id_dgt = 'DGT-'

# URLs de los 4 archivos
url_listado1 = ('https://gitlab.eif.urjc.es/cursosweb/2023-2024/'
                'final-teveo/-/raw/main/listado1.xml')
url_listado2 = ('https://gitlab.eif.urjc.es/cursosweb/2023-2024/'
                'final-teveo/-/raw/main/listado2.xml')
url_cctv = ('http://datos.madrid.es/egob/catalogo/202088-0-trafico-'
            'camaras.kml')
url_dgt = ('https://infocar.dgt.es/datex2/dgt/CCTVSiteTablePublication/'
           'all/content.xml')


def get_xml():
    # Obtiene el directorio base del archivo actual
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Une el directorio base con la ruta específica 'TeVeOapp/static/xml'
    directory = os.path.join(base_dir, 'TeVeOapp/static/xml')
    # Crea una lista de todos los archivos en el directorio que terminan en
    # '.xml' o '.kml'
    result = [f for f in os.listdir(directory) if f.endswith(
        '.xml') or f.endswith('.kml')]
    # Invierte el orden de la lista
    result.reverse()
    return result


def get_listado1(camera):
    try:
        id = camera.getElementsByTagName('id')[0].firstChild.data
        src = camera.getElementsByTagName('src')[0].firstChild.data
        name = camera.getElementsByTagName('lugar')[0].firstChild.data
        coordinates = camera.getElementsByTagName('coordenadas')[
            0].firstChild.data
        # Invertir las coordenadas
        coordinates = ','.join(coordinates.split(',')[::-1])
        source_id = id_listado1
        return source_id, id, src, name, coordinates
    except IndexError:
        print("Error: No se pudo obtener el archivo.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_listado2(camera):
    try:
        id = camera.getAttribute('id')
        src = camera.getElementsByTagName('url')[0].firstChild.data
        name = camera.getElementsByTagName('info')[0].firstChild.data
        latitude = camera.getElementsByTagName('latitude')[0].firstChild.data
        longitude = camera.getElementsByTagName('longitude')[0].firstChild.data
        coordinates = f'{latitude},{longitude}'
        source_id = id_listado2

    # Devuelve los datos extraídos
    except IndexError:
        print("Error: No se pudo obtener el archivo.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    return source_id, id, src, name, coordinates


def get_CCTV(cameras):
    for placemark in cameras:
        try:
            # Obtener el número, nombre y descripción
            number = placemark.getElementsByTagName(
                'Data')[0].getElementsByTagName('Value')[0].firstChild.data
            name = placemark.getElementsByTagName(
                'Data')[1].getElementsByTagName('Value')[
                0].firstChild.data
            description = placemark.getElementsByTagName(
                'description')[
                0].firstChild.data

            # Obtener la url
            img_url_match = re.search('src=(https://[^ ]+)', description)
            if img_url_match is None:
                print(f"La URL de la imagen de la cámara {number} no esta disponible")
                continue
            img_url = img_url_match.group(1)

            # Obtener las coordenadas
            coordinates = placemark.getElementsByTagName(
                'Point')[0].getElementsByTagName(
                'coordinates')[0].firstChild.data

            coordinates = ','.join(coordinates.split(',')[::-1])
            coordinates = coordinates.split(',')[1]

            # Añadir la cámara a la base de datos si no existe
            if not Camera.objects.filter(id=number).exists():
                cam = Camera(source_id=id_cctv, id=number,
                             src=img_url, name=name, coordinates=coordinates)
                cam.save()
            else:
                print(
                    f'La cámara {number} ya existe')
        except Exception as e:
            print(f"Error de la camara {number}: {e}")


def get_dgt(camera):
    try:

        camera_id = camera.getAttribute('id')
        camera_name = camera.getElementsByTagName('_0:cctvCameraIdentification')[0].firstChild.data
        image_url = camera.getElementsByTagName('_0:urlLinkAddress')[0].firstChild.data
        latitude = camera.getElementsByTagName('_0:latitude')[0].firstChild.data
        longitude = camera.getElementsByTagName('_0:longitude')[0].firstChild.data
        source_id = id_dgt

        # Devolver los datos extraídos
        return (source_id, camera_id, image_url, camera_name,
                f'{latitude},{longitude}')

    except IndexError:
        print("Error: No se pudo obtener los elementos de este archivo.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_files(xml_file, file_path):
    # URL del archivo XML
    if xml_file == 'listado1.xml':
        url = url_listado1
    elif xml_file == 'listado2.xml':
        url = url_listado2
    elif xml_file == 'CCTV.kml':
        url = url_cctv
    elif xml_file == 'dgt.xml':
        url = url_dgt

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/96.0.4664.110 Safari/537.36"
            ),
        }

        response = requests.get(url, headers=headers)

        # Escribir el contenido de la respuesta en un archivo
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Imprimir un mensaje de éxito
        print(f"El archivo {xml_file} de {url} se descargo")
    except Exception as e:
        print(f"Error al descargar {xml_file} de {url}. Error: {str(e)}")


def guardar_camara(sourc_id, id, src, name, coordinates):
    if not Camera.objects.filter(id=id).exists():
        cam = Camera(source_id=sourc_id, id=id, src=src,
                     name=name, coordinates=coordinates)
        cam.save()
    else:
        print(f'La camara {id} ya existe.')


def cargar_camaras(xml_file):
    # Obtener el directorio del archivo XML
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'TeVeOapp/static/xml')
    file_path = os.path.join(directory, xml_file)

    # Descargar el archivo XML
    download_files(xml_file, file_path)

    # Parsear el archivo XML
    dom = xml.dom.minidom.parse(file_path)
    root = dom.documentElement

    # Cargar las cámaras
    if xml_file == 'listado1.xml':
        cameras = root.getElementsByTagName('camara')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = get_listado1(
                camera)
            guardar_camara(sourc_id, id, src, name, coordinates)
    elif xml_file == 'listado2.xml':
        cameras = root.getElementsByTagName('cam')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = get_listado2(
                camera)
            guardar_camara(sourc_id, id, src, name, coordinates)
    elif xml_file == 'CCTV.kml':
        cameras = root.getElementsByTagName('Placemark')
        get_CCTV(cameras)
    elif xml_file == 'dgt.xml':
        cameras = root.getElementsByTagName('_0:cctvCameraMetadataRecord')
        for camera in cameras:
            sourc_id, id, src, name, coordinates = get_dgt(
                camera)
            guardar_camara(sourc_id, id, src, name, coordinates)


def guardar_imagen(cam):
    try:
        print(f"Processing camera with id {cam.id}")
        print(f"URL for camera with id {cam.id}: {cam.src}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/96.0.4664.110 Safari/537.36"
            ),
        }
        response = requests.get(cam.src, headers=headers)

        if response.status_code == 200:
            img = response.content
            img_path = os.path.join(
                'img/data', f'{cam.source_id}{cam.id}.jpg')
            full_img_path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), 'TeVeOapp/static', img_path)
            with open(full_img_path, 'wb') as f:
                f.write(img)
            cam.img_path = img_path
            cam.save()
            print(
                f"""Successfully saved image for
                camera with id {cam.id} and path {img_path}""")

        else:
            # Si falla la petición, imprimir un mensaje de error
            cam.img_path = 'img/resources/error.jpg'
            cam.save()
            print(
                f"""Failed to process camera with id {cam.id}.
                Error: {response.status_code}""")
    except Exception as e:
        print(f"Failed to process camera with id {cam.id}. Error: {str(e)}")


def get_img(xml_file):
    if xml_file == 'listado1.xml':
        cameras = Camera.objects.filter(source_id=id_listado1)
    elif xml_file == 'listado2.xml':
        cameras = Camera.objects.filter(source_id=id_listado2)
    elif xml_file == 'CCTV.kml':
        cameras = Camera.objects.filter(source_id=id_cctv)
    elif xml_file == 'dgt.xml':
        cameras = Camera.objects.filter(source_id=id_dgt)

    # Descargar y guardar la imagen de cada cámara
    for cam in cameras:
        guardar_imagen(cam)


def get_imagen_actual(id):
    # Obtener la cámara de la base de datos
    cam = Camera.objects.filter(id=id).first()
    if cam is None:
        print(f"La cámara {id} no esta disponible")
        return None

    # Descargar y guardar la imagen de la cámara
    guardar_imagen(cam)

    return cam.img_path


def get_imagen_aleatoria():
    # Obtener el directorio de las imágenes
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(base_dir, 'TeVeOapp/static/img/data')

    # Obtener la lista de archivos .jpg en el directorio
    result = [f for f in os.listdir(directory) if f.endswith('.jpg')]

    # Si hay al menos una imagen, seleccionar una aleatoriamente y devolverla
    if result:
        return random.choice(result)

    # Si no hay imágenes, devolver None
    return None


def eliminar_archivos(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))


def limpiar_camaras():
    # Eliminar todas las cámaras
    Camera.objects.all().delete()
    print("All cameras deleted")

    # Obtener el directorio base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Eliminar todas las imágenes en el directorio de datos
    data_directory = os.path.join(base_dir, 'TeVeOapp/static/img/data')
    eliminar_archivos(data_directory)

    # Eliminar todas las imágenes en el directorio de comentarios
    comments_directory = os.path.join(
        base_dir, 'TeVeOapp/static/img/comments')
    eliminar_archivos(comments_directory)

    print("No queda ningua imagen")


def guardar_comentarios(path):
    try:
        # Obtener el directorio base y el directorio de comentarios
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))
        directory = os.path.join(base_dir, 'TeVeOapp/static/img/comments')

        # Obtener la lista de archivos .jpg en el directorio de comentarios
        result = [f for f in os.listdir(directory) if f.endswith('.jpg')]

        # Crear el nuevo path para la imagen
        new_path = os.path.join(
            'img/comments', f'{len(result)}_{os.path.basename(path)}')
        full_path = os.path.join(base_dir, 'TeVeOapp/static', new_path)

        # Copiar la imagen al nuevo path
        with open(full_path, 'wb') as f:
            image_path = os.path.join(base_dir, 'TeVeOapp/static', path)
            with open(image_path, 'rb') as f2:
                f.write(f2.read())

        return new_path
    except Exception as e:
        print(f"No se pudo guardar la imagen. Error: {str(e)}")
        return None
