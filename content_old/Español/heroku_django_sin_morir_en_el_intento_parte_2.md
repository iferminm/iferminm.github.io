Title: Heroku + Django sin morir en el intento (Parte 2)
Date: 2014-09-20
Author: Israel Fermín Montilla
Tags: heroku, PAAS, python, django

En el artículo anterior, hablamos de IaaS y de PaaS y de cómo se
diferencian concluimos que *Heroku* es PaaS, además, expusimos algunas
de las limitaciones que nos impone la plataforma para desplegar nuestras
aplicaciones y cómo trabajar alrededor de ellas para hacer funcionar
todo.

Muchas veces, quizás por inocentes o inexpertos, tendemos a hacer todo
en la vista (y hablo de vistas de *django*), por ejemplo, necesitamos
enviar algo al servidor donde hosteamos las imágenes, simplemente
hacemos ejecutamos ese request en la vista, necesitamos enviar un correo
electrónico de confirmación, nada, lo enviamos en la vista, necesitamos
procesar una imagen para reducir la calidad y que ocupe menos espacio en
el servidor donde la vamos a hostear, dale... en la vista.

Bueno, exagero un poco, quizás no en la vista, si somos estrictos con
nuestro código, escribiremos una función que suba la foto al servidor,
otra que envíe el correo y otra que procese la imagen para reducir el
tamaño y llamaremos todo desde la vista. Este enfoque sigue estando
errado y, a continuación, voy a explicar por qué.

Todos venimos de hacer proyectos en la universidad, algunos más
difíciles que otros, en algún proyecto, seguramente nos tocó realizar
llamadas a alguna *API REST*, o enviar algún archivo a un servidor
remoto, en todos los casos, estoy seguro de que todos hicimos lo mismo,
una función que se ejecuta cuando enviamos el formulario y hace todo en
línea: llamadas remotas, envío de archivos, envío de correos, etc.

No es incorrecto, funciona, pero ¿cuánto tardó la página siguiente en
cargar?, la pregunta más adecuada sería ¿cuánto tiempo tardó la función
en redirigirme a la siguiente página?, calculemos unos 3 a 5 segundos
por llamada remota y unos 2 a 3 segundos, total, alrededor de 15
segundos en redirigir, a eso hay que sumarle el tiempo de carga de la
página siguiente.

Particularmente, mi primer trabajo fue en el mundo de los ERP, es una
historia totalmente distinta, si una persona manda a generar un reporte
que tarda 4 horas en ejecutarse y para ello el programa se bloquea y no
le permite hacer más nada, simplemente no tiene otra opción más que
esperar las 4 horas sentado en su escritorio, ir a tomarse un café,
bajar a fumar un cigarrillo hasta que esté listo.

Cuando programas para web, debes tomar en cuenta que debes ser gentil
con el usuario y no hacerlo esperar, tu página debe responder rápido,
sino, hay muchas otras páginas que hacen lo mismo y el usuario
simplemente tiene que regresar a la pestaña del navegador donde está su
búsqueda en google y seleccionar otro resultado. Una buena *rule of
thumb* a la hora de ejecutar operaciones pesadas, como todas las que
incluyan llamadas remotas o procesamiento de imágenes, es realizarlas de
manera asíncrona, para ello debemos valernos de *algo* que nos permita
retrasar la ejecución de una tarea.

Por un lado, necesitaremos algo que nos sirga para mantener una cola de
tareas pendientes por ejecutar, por otro lado necesitamos algo que vaya
leyendo esas tareas y ejecutándolas, la manera más simple de hacerlo en
*Python* es con una librería llamada *python-rq* y usando *Redis* como
backend de tareas, es muy fácil de configurar y súper sencilla de usar
para la mayoría de proyectos pequeños a medianos funcionará bastante
bien. Para proyectos a mayor escala, quizás lo mejor sea utilizar
*celery* con *RabbitMQ* como broker de mensajes. Hay muchas herramientas
que podemos usar como backend de mensajes: Redis, RabbitMQ, ZeroMQ,
Kafka, HornetQ... es cuestión de evaluarlas y ver cuál se ajusta más al
proyecto en cuestión en el cual estamos trabajando.

Como todo en *django*, tenemos un paquete llamado *django-rq* que nos
ayuda a organizar el código de una mejor manera y nos hace la vida más
fácil, empecemos por descargar las librerías y paquetes necesarias:

```
    sudo aptitude install redis-server
    pip install django-rq django
```

Si estamos en *Heroku*, no es necesario instalar *redis*, simplemente
agregar los nuevos paquetes Python al *requirements.txt* para que sean
instalados al hacer *push*

Para poder agregar trabajos a las colas, debemos declararlas para que
*django-rq* las reconozca, simplemente agregamos una nueva variable en
nuestro *settings.py*. A continuación un ejemplo de configuración para
*django\_rq*, la cola *default* es un ejemplo para desarrollo, la cola
*high* es un ejemplo de configuración para Heroku si estamos usando el
*add on* de *Redis To Go*.


```python
    RQ_QUEUES = {
        'default': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
        },
        'high': {
            'HOST': os.getenv('REDISTOGO_URL'),
            'PORT': 6379,
            'DB': 0,
        }
    }
```

Ahora, las funciones sumamente pesadas pueden ser encoladas en
cualquiera de las dos colas que hemos declarado en *settings.py*.

```python
    def funcion_sumamente_pesada(argumento):
        pass
```

Lo que haremos en nuestra vista es, en vez de llamar a la función
directamente, le diremos a *django\_rq* que agregue el trabajo en la
cola que consideremos conveniente.

```python
    import django_rq
    from helpers import funcion_sumamente_pesada

    def view(request):
        #...
        queue = django_rq.get_queue('high') # si no indicamos una cola, retorna la cola 'default'
        queue.enqueue(funcion_sumamente_pesada, argumento)
```

También decorar las funciones que queremos encolar, esto hace que el
código se vea un poco más limpio, pero el efecto es el mismo:

```python
    from django_rq import job

    @job('high')
    def funcion_sumamente_pesada(argumentos):
        pass
```

Y luego, en la vista:

```python
    def view(request):
        #...
        funcion_sumamente_pesada.delay(argumento)
```

Lo que rq hace es tomar el *objeto función*, serializarlo usando
*pickle* y guardar ese objeto serializado en redis. Ahora que tenemos el
trabajo encolado, necesitamos *algo* para leerlo de redis,
des-serializarlo y ejecutarlo.

RQ, viene con un worker que podemos ejecutar en un *dyno* aparte
(recuerden agregar la entrada correspondiente en el *Procfile* de
Heroku), simplemente corremos el siguiente comando en el terminal para
probar localmente:

```
    python manage.py rqworker high default
```

En la consola, podemos ver cómo los trabajos se van ejecutando, incluso,
si apagamos el worker y mandamos a encolar algunos trabajos, al ejecutar
de nuevo el worker de rq podemos ver como los va leyendo de redis y los
ejecuta.


## Consideraciones con objetos persistentes en base de datos

Bueno, ya sabemos que rq hace un *pickle* de la función y sus argumentos
y envía esa información a *Redis* para luego ser leído por el worker,
hacer el *unpickle* y ejecutar el trabajo.

A menudo, necesitamos hacer *delay* de un trabajo que actúa sobre
objetos que persisten en la base de datos, nuestra primera tentación es
simplemente pasar los objetos como argumentos al trabajo.

Ahora, veamos, analicemos qué ocurrirá. Al encolar el trabajo tanto la
función como sus argumentos serán serializados, estos argumentos son
objetos que pueden ser modificados. Luego de encolar, supongamos que
modifico uno de los atributos del objeto y lo guardo en la base de
datos, luego, al ejecutarse mi trabajo la función también modifica otro
atributo y guarda el objeto en la base de datos.

Lo que va a ocurrir es que, como la referencia que fue serializada al
momento de encolar está desactualizada, la modificación que se hizo
luego de encolar no estará reflejada en el objeto luego de ejecutar el
trabajo.

### La solución

Simplemente no pasar objetos persistentes como argumentos, es mucho
mejor simplemente dar los *id* de base de dato al trabajo y que dentro
de la función se ejecute un query para traerlos, de esta manera evitamos
conflictos y dolores de cabeza como el antes descrito.

Espero que esto sea de ayuda, es buena práctica trabajar con colas para
trabajos pesados en cualquier proyecto web, no sólo si estamos corriendo
nuestra app en Heroku.
