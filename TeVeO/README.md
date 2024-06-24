# Final-TeVeO

# ENTREGA CONVOCATORIA JUNIO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Raul Sanchez Merino
* Titulación: Ing. Telematica
* Cuenta en laboratorios: raulsm
* Cuenta URJC: r.sanchezmer.2017
* Video básico (url): https://youtu.be/aZRgjldtjtM
* Despliegue (url): rauls.pythonanywhere.com
* Contraseñas: No hay contraseñas
* Cuenta Admin Site: usuario/contraseña: admin/admin

## Resumen parte obligatoria

### Pagina principal
Al acceder a la web veremos una lista de comentarios realizados por los usuarios.
Tambien disponemos de un menu con las diferentes paginas a las que podremos acceder en la web.

### Pagina Camaras
En la pagina principal de Camaras encontraremos una lista de camaras disponibles, con la informacion de cada camara: Ubicacion, identificador, numero de comentarios y la imagen de la misma.
A la derecha, o abajo dependiendo del dispositivo que usemos, encontramos las fuentes de datos diponibles. Si clickamos en cualquiera de ellos cargaremos sus datos y podremos acceder a ellos despues de unos segundos. He incluido una opcion para eliminar las imagenes y comentarios 

Al selecionar una camara, se nos redireccionara a su pagina personal. En ella podremos ver la imagen actual de la camara, su informacion, asi como los comentarios que otros usuarios han realizado y ordenarlos por orden de antiguedad.
Tambien contamos con un menu que nos permitira añadir un comentario, acceder al pagina dinamica de la camara o ver el JSON de la camara.
### Pagina Administracion
Esta pagina contiene el portal de administracion de Django. Se requiere introducir el usuario y contraseña para acceder.

### Pagina Configuracion
En esta pagina podras registrarte con tu nombre de usuario, lo que te permitira comentar en las camaras que tu desees. Tambien podras elegir el tamaño y la fuente del texto

### Pagina Ayuda
Contiene informacion sobre el funcionamiento de la web.


## Contenido de HTML
Para todas las paginas he incluido:
* Un banner con una imagen.
* Un menu con las diferentes paginas a las que podremos acceder en la web.
* Un footer en el que se muestra el numero de camaras y comentraios disponibles en el momento.

Para cada pagina he incluido la informacion citada anteriormente en el resumen.


## Lista partes opcionales

* Favicon: He añadido una imagen como favicon
* Imagen de error: En caso de que ocurro un fallo he incluido una imagen de error.
* Ordenar comentarios: He añadido la opcion de ordenar los comentarios por la fecha en la que se realizaron
* Ordenar camaras: Tambien se pueden ordenar por el numero de comentarios.
* Imagenes en Carrusel: En la pagina de las camaras he creado un carrusel con las imágenes de las camaras que el usuario haya decidido cargar de las bases de datos.
* Opcion para crear una sesion en la pagina de Configuracion: Se podra crear un enlace de autenticacion o introducir uno ya existente para crear una sesion anterior.


## Otros requisitos
* Tests de extremo a extremo para cada tipo de recurso de la practica.
* He incluido en archivo requirements.txt con las bibliotecas de Python que hacen falta para que la aplicacion funcione correctamente.

## Comentarios sobre la practica
He intentado añadir mi practica e PythonAnywhere pero debido a un problema con los archivos no he podido subirla.
La practica funciona perfectamente en los laboratorios de la universidad como lo demuestro en el video: https://youtu.be/aZRgjldtjtM