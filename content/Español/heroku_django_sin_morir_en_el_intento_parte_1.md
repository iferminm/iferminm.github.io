Title: Heroku + Django sin morir en el intento (Parte 1)
Date: 2013-09-23
Author: Israel Fermín Montilla
Tags: heroku, django, python, PAAS

Antes, para tener tu sistema web en línea, debías contratar un servicio
de Servidor Dedicado o mínimo un VPS y administrarlo, si tenías más
presupuesto, comprabas un servidor y lo acondicionabas o alquilabas un
rack en algún centro de datos para tenerlo colocado allí.

Ahora, con el boom de *Infraestructura como Servicio* (IaaS) y
*Plataforma como Servicio* (PaaS), ya no es necesario tener servidores
propios y, dependiendo del servicio, es decir, si es *IaaS* o *PaaS*,
tampoco debes tener conocimientos de administración de servidores.

## IAAS vs PAAS

En general, un proveedor de *IaaS* te da el hardware para que tú lo
configures y ensambles el ambiente en el que va a correr tu aplicación,
esto es instalar todos los paquetes de software necesarios par que el
proyecto corra: servidor de base de datos, servidor web, intérpretes,
bibliotecas, storages adicionales y un largo *end of thinking capacity*
(etc). La ventaja de un proveedor de este tipo es que hacen que escalar
tu infraestructura de manera horizontal es realmente fácil y no tienes
que construir un centro de datos para albergar tu granja de servidores
ni mucho menos configurar todo lo que eso implica, un ejemplo de
servicios de este tipo es el *Elastic Compute Cloud* de *Amazon Web
Services* (AWS EC-2).

Por otra parte, un proveedor de *PaaS*, hace exactamente lo mismo, pero
con un nivel más de abstracción, te proveen toda la infraestructura y el
ambiente para que simplemente deposites tu código allí y pongas tu
aplicación a correr con configuraciones mínimas y sin ser un experto en
administración y configuración de servidores, de hecho, es transparente
para ti toda la nube que hay por detrás.
[Heroku](http://www.heroku.com/){.reference .external} es un proveedor
de este tipo de servicio que además cumple con el [12 factor
app](http://12factor.net/){.reference .external} por lo que además hace
que sea súper fácil ajustar tu código para correr allí y que tome los
parámetros de configuración que define la plataforma sin mucho problema.

## Ahora, Heroku

El modelo de trabajo en *Heroku* se basa en add-ons, que básicamente
integran tu sistema con un DBMS, un sistema de alertas en caso de fallos
o de monitoreo para ver el rendimiento, detectar cuellos de botella y
tomar correctivos al respecto, todo esto con unos cuantos clicks (y una
tarjeta de crédito), sin configurar absolutamente nada a nivel de
servidores sino todo a nivel de aplicación.

Todo esto suena como un sueño hecho realidad y, en muchos casos, lo es,
pero nada es perfecto y *Heroku*, aunque facilita muchísimas cosas a
nivel de despliegue, te complica muchas otras a nivel de desarrollo,
esto puede ser bueno, te obliga a optimizar y a aprender, pero a veces,
el esquema de plugins y addons puede volverse insostenible, sobre todo
cuando debes pagar por varios y el presupuesto es limitado, además,
desde el punto de vista de aplicación, *Heroku* impone varias
limitaciones acerca de cómo debe comportarse, el tiempo en que debe
responder, el tiempo que debe durar el deploy y cuánto debe pesar.

### Algunas limitaciones

-   *El app debe iniciar en 60 segundos o menos:* si este tiempo se
    excede, el deploy falla.
-   *Heroku duerme dynos cada cierto tiempo:* cada cierto tiempo Heroku
    reinicia los dynos, esto es un proceso totalmente aleatorio, por eso
    se recomienda tener al menos 2, si uno es reiniciado el otro sigue
    aceptando requests. Cuando esto ocurre, el proceso recibe un
    *SIGTERM*, al recibir la señal, se tienen 10 segundos de gracia para
    terminar lo que se estaba haciendo antes de recibir un *SIGKILL*
    y reiniciar.
-   *El app no puede pesar más de 300MB:* de lo contrario, el deploy
    falla, es recomendable usar el .slugignore para excluir archivos que
    sólo se usan para desarrollo y que no hacen falta en producción, lo
    mismo con las librerías para testing, no deberían incluirse en el
    requirements.txt que va a producción.
-   *El app debe responder a los requests en 30 segundos:* de lo
    contrario se levanta un error H12 (Worker Timeout) y la respectiva
    pantalla de *Application Error*.
-   *Heroku es stateless:* esto quiere decir que no guarda estado, para
    conservar estado del app es necesario valerse de otras herramientas,
    como una base de datos, memcached, y servicios de
    almacenamiento externos.

### Algunos de los golpes

Con esas limitaciones se puede vivir, pero hay que darle la vuelta para
no desesperarse, hay algunas cosas que capaz son obvias, pero que uno no
las ve sino hasta que empieza a trabajar y se consigue con un problema,
basta con volver sobre las limitaciones antes expuestas y encontraremos
una respuesta o al menos una posible razón.

Ahora voy a empezar a listar los problemas que he tenido en *RingTu* y
cómo los solucioné. Recuerden que estoy trabajando con **Django**, por
lo que todo lo he resuelto utilizando herramientas para este framework.

#### No es bueno para servir assets

Cuando digo assets, me refiero a los archivos estáticos que dan forma a
la interface web: css, js, imágenes, gradientes, ¿gifs animados?,
tipografías y demás cosas bonitas que hacen los diseñadores por
nosotros.

Por defecto, nuestro dyno sirve todos estos archivos, además de servir
nuestra aplicación, aceptando peticiones de nuestros clientes,
procesándolas y decidiendo qué es lo que va a enviarse de vuelta.

Servir los archivos estáticos o *static assets* resulta en requests
adicionales que van a mantener ocupado nuestro dyno y esto nos cuesta
tiempo y, si ya estamos pagando, dinero. Esos requests adicionales se
podrían invertir en responder y procesar solicitudes nuevas y no en
entregar archivos estáticos, además, la **buena práctica** con *django*
es delegar la entrega de contenido estático a un **servidor web** como
*Apache* o *NGinx* y así evitar procesamiento adicional a nivel de
*views* (los *controladores* de *django*).

La solución acá es, simplemente, almacenar los archivos estáticos *en
otro lado*, puede ser incluso un *VPS* con *Apache* o *NGinx* instalado,
pero hay varios servicios que pueden hacerlo mejor y optimizar la
entrega de contenidos como *Cloudfile* de **Rackspace** y, el que opté
por usar, *Simple Storage Service* de **Amazon**. Si ya tus assets no
cambian mucho, lo mejor es servirlos a través de una *CDN* (Content
Delivery Nerwork o Red de Entrega de Contenidos), como *Cloudfront*,
también de **Amazon**.

Ahora, **¿Cómo se resuelve esto en django?**, bueno, hay varias
librerías que te permiten sincronizar los archivos estáticos con un
servicio de almacenamiento remoto, la que decidí usar fue
[django-s3-folder-storage](https://github.com/jamstooks/django-s3-folder-storage){.reference
.external}, una pequeña librería que se vale de otra más compleja (y
completa, soporta múltiples servicios) llamada
[django-storages](https://github.com/iserko/django-storages){.reference
.external} para organizar tu contenido en directorios dentro de un
*bucket* de *S3*, es necesario agregar parámetros de configuración en
nuestro *settings.py*, sería algo como esto:

```
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

    # Expires 20 years in the future at 8PM GMT
    tenyrs = date.today() + timedelta(days=365*10)
    AWS_HEADERS = {
        'Expires': tenyrs.strftime('%a, %d %b %Y 20:00:00 GMT')
    }

    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
    STATIC_S3_PATH = 'static/'
```

El parámetro de configuración AWS\_QUERYSTRING\_AUTH colocado en *False*
es para que *S3* no nos genere urls firmadas para los assets sino que
nos permita acceso público permanente. Si lo dejamos en *True*, su valor
por defecto, nos va a generar un url válido por 5min y, como son
archivos estáticos, esta url no se va a refrescar nunca, así que nuestra
página se verá **bien**, con todos sus estilos y efectos sólo mientras
duren las urls vigentes.

Los demás son simplemente parámetros de configuración de S3, deben
recordar añadir las variables de configuración en *Heroku*.

```
    heroku config:add AWS_ACCESS_KEY_ID=EL_KEY_ID_DE_AWS_S3
    heroku config:add AWS_SECRET_ACCESS_KEY=EL_SECRET_KEY_ID_DE_AWS_S3
    heroku config:add AWS_STORAGE_BUCKET_NAME=EL_NOMBRE_DEL_BUCKET
```

Recuerden también colocar *s3\_folder\_storage* entre los
*INSTALLED\_APPS* del proyecto y activar la opción de *Heroku* para que
reconozca las variables de configuración en tiempo de compilación, de
otra manera, el deploy fallará.

```
    heroku labs:enable user-env-compile
```

Con esto, ya deberíamos poder sincronizar los *assets* a *S3*

```
    heroku run python manage.py collectstatic
```

Dependiendo de qué tantos archivos estáticos tengamos, va a tardar más o
menos, va a enviar todo lo que esté en nuestro *STATIC\_ROOT* al *bucket
S3* que configuramos anteriormente.

#### No puedes utilizar el sistema de archivos

Había dicho al principio que *Heroku* es *stateless*, es decir, no
conserva el estado de tu aplicación. Entonces ellos implementaron algo
llamado *Ephemeral Filesystem*, es decir, un sistema de archivos
*efímero*, que se reinicia cada vez que los dynos son reiniciados por
cualquier razón, sea un deploy o sea porque heroku los reinició.

**¿Qué significa esto?**, pues que **no puedes escribir a disco** como
lo harías en cualquier servidor *normal*, si lo haces, debes saber que
cuando tu app sea reiniciada, perderás todos los archivos, tiene un poco
de sentido, cuando usas más de un dyno y escribes a disco, cuando el
usuario quiera recuperar lo que subió, no tenemos manera de saber cuál
dyno atendió aquella solicitud y no sabremos dónde buscar, así que, de
una manera u otra, lo mejor es almacenar los archivos de nuestros
usuarios en un lugar seguro y de donde podamos recuperarlos luego sin
problemas.

Nuevamente podemos utilizar *AWS-S3* para ello, con algunas
configuraciones adicionales, podemos hacer que por defecto nuestros
*media files*, para usar la terminología de *django*, sean almacenados
en nuestro *bucket*.

Es necesario agregar las siguientes líneas a nuestro *settings.py*:

```
    MEDIA_ROOT = ''
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media/'
    MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
```

Con esto, todo lo que suban nuestros usuarios irá a la carpeta *media/*
de nuestro bucket.

Hay que tener en cuenta que todo se está subiendo al mismo *bucket* y la
política que se definió en principio para poder almacenar los archivos
estáticos da acceso público a todo el contenido por defecto, por lo que
hay que tomar previsiones *de alguna manera* para que no todo el mundo
pueda ver los archivos de nuestros usuarios de manera directa.

Acá expondré la estrategia que uso:

1.  **Sobre-escritura del método save():** en los modelos que tengan un
    *ImageField* o un *FileField*, la idea de esto es sobreescribir la
    política de control de acceso particular para el archivo una ves que
    fue subido. Para esto utilizaremos una librería llamada
    [boto](https://github.com/boto/boto){.reference .external} que es un
    wrapper en Python para el API de *AWS*

```python
    from django.db import models
    from django.conf import settings
    from django.contrib.auth.models import User

    class Video(models.Model)
        user = models.ForeignKey(User)
        video = models.FileField(upload_to='user_videos/')

        def save(self, *args, **kwargs):
            from boto.s3 import connection, key
            super(VoiceMessage, self).save(*args, **kwargs)

            conn = connection.S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            k = key.Key(bucket)
            k.key = '%s%s' % (settings.DEFAULTS3_PATH, self.video)
            k.set_acl('private')

```

Con esto tenemos el archivo privado en *S3*, ahora, necesitamos una
manera de darle acceso al usuario que es propietario del archivo.

2.  **Escribiendo una vista para acceder al archivo privado:** la mejor
    manera que conseguí para darle acceso al usuario a su archivo fue
    escribiendo una vista de *django* que revisara que el usuario que
    origina el request es realmente el propietario del objeto y
    redirigirlo a la ubicación de su archivo en *S3*. Escribiremos un
    pequeño helper, además, para encapsular la generación del URL, como
    es un archivo privado, el url debe ir firmado y sólo será válido por
    el tiempo que nosotros indiquemos, en este caso, lo haremos por
    una hora.

En el helper colocamos lo siguiente:

```python
    from django.conf import settings


    def get_s3_redirect_url(filepath, ttl=60):
        from boto.s3.connection import S3Connection

        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, is_secure=True)
        return conn.generate_url(ttl, 'GET', bucket=config.AWS_STORAGE_BUCKET_NAME, key=filepath, force_http=True)
```

y en la vista:

```python
    from django.http import HttpResponse, HttpResponseRedirect
    from django.contrib.auth.decorators import login_required
    from .models import Video

    @login_required
    def get_user_video(request, video_id):
        if request.method == 'GET':
            from .helpers import get_s3_redirect_url
            user = request.user
            video = Video.objects.get(id=video_id)
            if user == video.user:
                filepath = '%s%s' % (settinga.DEFAULT_S3_PATH, video.video)
                url = get_s3_redirect_url(filepath, ttl=3600)
                return HttpResponseRedirect(url)

        return HttpResponse(status=403)
```

Con esto generamos una url firmada y válida por 3600 segundos (una hora)
si el usuario que origina la solicitud es el propietario del objeto que
contiene el archivo (video) que se desea obtener, caso contrario
retornamos 403 ya que la persona no tiene permisos para ver ese
contenido.
