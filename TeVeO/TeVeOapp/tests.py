from django.test import TestCase, RequestFactory
from . import views
from .models import *

# Create your tests here.
class Tests(TestCase):

    def test_config(self):

        request = RequestFactory().get('/config/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.config(request)
        print("Test config")
        self.assertEqual(response.status_code, 200)

    def test_index(self):

        request = RequestFactory().get('/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.index(request)
        print("Test index")
        self.assertEqual(response.status_code, 200)


    def test_camaras(self):

        # Creamos una camara con el id TEST
        cam = Camera.objects.create(
            source_id='TEST',
            id='TEST',
            src='https://infocar.dgt.es/etraffic/data/camaras/3.jpg',
            name='TEST',
            coordinates='TEST',
            img_path='TEST'
        )

        # Guardamos la camara
        cam.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camaras(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camaras")

        # Borramos la camara
        cam.delete()

    def test_pag_camaras(self):

        request = RequestFactory().get('/camaras/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.pag_camaras(request)
        print("Test pag_camaras")
        self.assertEqual(response.status_code, 200)



    def test_ver_comentarios(self):

        request = RequestFactory().get('/comentario/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.ver_comentarios(request)
        self.assertEqual(response.status_code, 200)
        print("Test ver_comentarios")


    def test_camara_id(self):

        # Creamos una camara con el id TEST
        cam = Camera.objects.create(
            source_id='TEST',
            id='TEST',
            src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg',
            name='TEST',
            coordinates='TEST',
            img_path='TEST'
        )

        # Guardamos la camara
        cam.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/dyn')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camara_id(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camara_id")

        # Borramos la camara
        cam.delete()

    def test_get_imagen(self):

        # Creamos una camara con el id TEST
        cam = Camera.objects.create(
            source_id='TEST',
            id='TEST',
            src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg',
            name='TEST',
            coordinates='TEST',
            img_path='TEST'
        )

        # Guardamos la camara
        cam.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/img')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.get_imagen(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test get_imagen")

        # Borramos la camara
        cam.delete()

    def test_cargar_comentarios(self):

        # Creamos una camara con el id TEST
        cam = Camera.objects.create(
            source_id='TEST',
            id='TEST',
            src='https://infocar.dgt.es/etraffic/data/camaras/4.jpg',
            name='TEST',
            coordinates='TEST',
            img_path='TEST'
        )

        # Guardamos la camara
        cam.save()

        # Creamos un comentario para la camara
        comment = Comment.objects.create(
            name='TEST',
            camera=cam,
            comment='TEST-TEST',
            date='06-04-24',
            img_path_comment='TEST')

        # Guardamos el comentario
        comment.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/comment')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.cargar_comentarios(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test cargar_comentarios")

        # Borramos la camara
        cam.delete()

    def test_camara_json(self):

        # Creamos una camara con el id TEST
        cam = Camera.objects.create(
            source_id='TEST',
            id='TEST',
            src='https://infocar.dgt.es/etraffic/data/camaras/3.jpg',
            name='TEST',
            coordinates='TEST',
            img_path='TEST'
        )
        # Guardamos la camara
        cam.save()

        # Creamos un request con el id TEST
        request = RequestFactory().get('/camaras/TEST/json')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}

        response = views.camara_json(request, 'TEST')
        self.assertEqual(response.status_code, 200)
        print("Test camara_json")

        # Borramos la camara
        cam.delete()

    def test_camaras_json(self):

        request = RequestFactory().get('/camaras/json')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.camaras_json(request)
        print("Test camaras_json")
        self.assertEqual(response.status_code, 200)

    def test_help(self):

        request = RequestFactory().get('/ayuda/')
        request.session = {
            'username': '',
            'font_size': 'TEST',
            'font_family': 'TEST'}
        response = views.help(request)
        print("Test help")
        self.assertEqual(response.status_code, 200)

