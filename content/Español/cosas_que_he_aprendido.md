Title: Cosas que he aprendido, SOA
Date: 2014-12-06
Author: Israel Fermín Montilla
Tags: programacion, buenas prácticas

Luego de algún tiempo desarrollando software, sea para web o escritorio,
uno realmente termina de entender aquello que nos decían en *Algoritmos
y Programación I* de **Divide y vencerás**, quizás en la Universidad uno
no lo aplica mucho, tienes 8 proyectos y 14 parciales en una semana y
tienes que salir de todo lo más rápido posible, entonces terminas
escribiendo muchísimo terrible, quien sea inocente, que lance la primera
piedra. Incluso a veces en el trabajo por la presión de los *deadlines*
uno termina tomando atajos para hacer la cosa funcionar y dejar un
comentario de estos que empiezan con **TODO** o **FIXME** para
arreglarlo luego o advertir al resto del equipo que ese bloque de código
debe ser arreglado o podría causar problemas más adelante.

Lo primero que uno tiende a hacer es separar todo en funciones, tratar
de que cada función que se escribe haga una y sólo una cosa, sin efectos
colaterales, por ejemplo:

```python
def write_to_file(f, text):
    f.write(text)
    f.close()
```

Esta función, claramente, no hace una cosa, hace dos, escribe un texto
al archivo y luego lo cierra, esto es poco intuitivo, cualquiera
llamaría la función dos veces y, la segunda, seguramente ocurre una
excepción, lo ideal sería:

1.  Renombrar la función a *write\_to\_file\_and\_close()* o...
2.  Mucho mejor, simplemente cerrar el archivo en otra parte.

¿Ven?, **divide y vencerás**, nada difícil ¿no?

Luego, conocemos las clases, los objetos y los paquetes (no, no esa
clase de paquetes, no sean mal pensados), entonces, empezamos encapsular
entidades en clases, cuyos objetos actuarán sobre los datos que maneja
el programa y cada clase tendrá una y sólo una tarea específica, esta
tarea la cumplirá porque todos y cada uno de los métodos que escribimos
para ella están relacionados entre sí y están diseñados para trabajar en
conjunto para lograr ese objetivo, es decir, tienen *alta cohesión*.

Al mismo tiempo, estas clases, la agrupamos en *paquetes* o *módulos*,
cada uno de estos, cumple también una tarea específica que no afecta el
trabajo de los demás, es decir, tienen *bajo acoplamiento*, tenemos,
normalmente, un módulo para acceso a datos, un módulo para la lógica
compleja del programa y otro para interactuar con la *Capa 8 de la red*,
es decir, el usuario.

Hasta ahora, vamos bien, todo dividido en módulos y así arquitectamos
nuestros sistemas por un largo tiempo, todo lo nuevo que hacemos, lo
encapsulamos en un módulo aparte que se puede importar, *y vio Dios que
era bueno*, entonces nos permitió seguirlo haciendo así.

## Construyendo un elefante

Si trabajamos mucho tiempo iterando sobre el mismo sistema, la tendencia
natural es que este crezca, entonces, la cantidad de módulos irá
creciendo cada vez más, así como también los recursos que consume y, si
todo sale bien, también crecerá el tráfico que tenemos que manejar,
entonces, poco a poco sólo un gran servidor se irá quedando corto, ¿cuál
es la solución natural?, escalar de manera horizontal y agregar más
servidores corriendo detrás de un balanceador de carga, pero recordemos
que estamos corriendo un sistema enorme con muchos módulos cargados en
memoria, se necesita un servidor grande (y probablemente caro) para
levantar algo tan pesado.

Más allá de eso, empezamos a preguntarnos, ¿qué tanto se usa cada
módulo?, por ejemplo, tenemos un módulo de registro de usuarios pero, no
todos los usuarios que van a nuestra página, por ejemplo, necesitan
registrarse, sin embargo, ese módulo está cargado N veces, donde N es la
cantidad de servidores que tengamos sosteniendo nuestro monolito que,
además, seguramente seguirá creciendo cada vez más.

Eso por un lado, por otro lado, por otro lado, cada vez que vamos a
liberar un feature nuevo, resolver un bug o simplemente cambiar un texto
en una plantilla, tenemos que hacer deploy de un sistema pesado en N
servidores, algo que puede tardar bastante tiempo y quizás causar
*downtime* de algunos minutos, quizás perdiendo potenciales usuarios.

Además, poco a poco hacer cambios en un *codebase* tan grande, se vuelve
doloroso, es difícil de modificar, difícil de probar, difícil de escalar
y, por lo tanto, difícil de mantener.

## ¿Trabajo de hormigas?, ventajas

¿Qué pasaría si cada módulo lo convertimos en un proyecto aparte?, sí,
con su propio servidor y todo, tendríamos varios servicios que hacen una
sola cosa y, simplemente, tendríamos que escribir clientes para esos
servicios y utilizarlos cuando sea necesario y en el orden que sea
necesario, ¿qué ventajas tiene esto?

Por un lado, usamos servidores más pequeños y si, por ejemplo, los
usuarios están subiendo muchas fotos, simplemente escalamos el "servicio
de gestión de fotos" y listo, es decir, agregamos un nuevo servidor y
eso debería soportar más tráfico. No creamos una instancia nueva de un
servidor enorme con, además, partes del sistema que no está siendo
usadas o que no están recibiendo tanto tráfico.

Por otro lado, es más fácil conseguir errores, si falla el servicio de
pagos, sabemos que algo está mal con ese servicio pues, la única manera
de que algo llegue allí es a través de la interfaz HTTP que este
servicio expone. También agregar features nuevos se convierte en una
tarea fácil, no hay que modificar un proyecto enorme sino quizás agregar
un servicio nuevo e integrarlo. Resolver bugs se convierte también en
una tarea más fácil pues ya sabemos dónde está fallando y, a la hora de
hacer un release, si hay *downtime* es sólo un servicio y los usuarios
prefieren un *En este momento no es posible completar tu solicitud,
intenta en unos minutos* que un *En este momento estamos en
mantenimiento, regresa luego*, al menos pueden seguir usando las otras
partes del sistema, ¿no?.

Finalmente, permite que la plataforma sea políglota, es decir, si tienes
todo hecho en Ruby on Rails, por ejemplo, pero quieres tener el motor de
búsqueda con tecnologías de Web Semántica y, la mejor herramienta que
conseguiste fue integrar [Jena](https://jena.apache.org/) con 
[Pellet](http://clarkparsia.com/pellet/) como motor de inferencia y 
todo eso está en *Java*, simplemente es un servicio más que expondrá 
unas interfaces para que el resto pueda usarlo, así que realmente 
no importa en qué esté escrito.

## No todo es perfecto

Como todo en software, no hay balas de plata para matar problemas, cada
solución tiene también sus contra, algunos de los que he podido ver son
los siguientes:

-   Un request del usuario puede derivar en 50 o 60 requests internos a
    servicios, por lo que la velocidad de respuesta se aprecia, hay que
    tener en caché lo que se pueda e invalidar ese caché oportunamente
    para actualizarlo cuando sea necesario.
-   Cuando el equipo es muy grande, no todos los desarrolladores conocen
    todos los servicios, siempre hay unos que saben más que otros y
    otros que saben mucho de algunos y nada de otros, es difícil
    mantener homogeneidad en el conocimiento acerca de todo el stack.
-   Si un servicio no responde por alguna razón y las interfaces de los
    servicios son HTTP, ese request se pierde, por lo tanto no tendremos
    esos datos en el servicio que corresponda, así que si nuestro
    enfoque es optimista, el servicio que envió el request está contando
    con que todo salió bien, hay que pensar entonces en algún método que
    permita reintentar o, si falla la solicitud, tener un método de
    *fallback* para estos casos, quizás una cola para que el otro
    servicio empiece a procesar cuando se despierte o, quizás, cambiar
    las llamadas HTTP por colas compartidas.
-   Las complicaciones de tener múltiples servidores tras un balanceador
    de carga se multiplican por el número de servicios que tengamos.

## Buenas prácticas

Aplica todo lo que ya sabemos, pero hay que ser un poco más rigurosos.

-   **Documentación:** además del código, hay que documentar la API que
    expone el servicio que escribimos.
-   **Tolerancia a fallos:** además de servidores redundantes, es
    necesario tener un método de recuperación de datos en caso que falle
    algún servicio y algo no llegue a la base de datos.
-   **Pruebas:** probar cada servicio es fácil, un set de pruebas
    unitarias hace el trabajo bastante bien, la cosa se pone un poco más
    difícil con la pruebas de integración, es necesario contar con los
    servicios con los que se va a interactuar a la hora de ejecutar
    estas pruebas.
-   **Deploy:** se hace vital contar con un sistema de integración
    continua, de otra manera todo se nos puede salir de las manos y se
    vuelve poco mantenible.
-   **Monitoreo:** es necesario monitorear todos los servicios para
    conocer dónde están los cuellos de botella y optimizar lo que sea
    necesario o tomar acciones para solventarlo. Además de saber cuándo
    un servicio está caído antes de que los usuarios empiecen
    a quejarse.

Como todo, el nirvana no es solamente orientado a servicios, hay muchas
otras maneras de arquitectar sistemas y todas son correctas dependiendo
de las condiciones y el contexto que las rodean.

Acá dejo [una entrevista](http://queue.acm.org/detail.cfm?id=1142065) a uno de mis héroes
personales sobre este tema, Werner Vogels, CEO de Amazon.
