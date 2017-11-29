Title: Cosas que he aprendido: Descriptores
Date: 2014-12-01
Author: Israel Fermín Montilla
Tags: python, programación, descriptores

Bueno, llevo ya unos años dedicado casi 100% a desarrollo web con
*Python*, unos años en los que he aprendido muchas cosas sobre el
lenguaje y, por un momento, pensé que sabía suficiente, pero cuando uno
empieza a pensar eso es peligroso, al final, nunca se sabe suficiente y
siempre hay mucho por aprender.

El año pasado, durante mi entrevista para entrar en
[dubizzle](http://dubizzle.com){.reference .external} aprendí un
concepto nuevo que incluye python y que es súper interesante, podría
resultar útil para alguien y, sino, escribiendo sobre ello me ayudo a mi
mismo a recordarlo y a entenderlo mejor.

Python, incluye una cantidad enorme de características en su biblioteca
estándar que nos ayudan a resolver problemas comunes del día a día y
ofrecer interfaces más intuitivas y pythónicas, tal el es caso de las
propiedades o *properties*. Hablaré un poco de ellas porque son claves
para entender el concepto de descriptores o *descriptors*.

## Properties

Básicamente, es una función que convierte en un *getter* un atributo que
queremos que sea de sólo lectura, pero su uso más común es retornar
manejar el acceso o controlar el valor de atributos que dependen del
valor de otros atributos del mismo objeto y proveer una interfaz de
acceso más pythónica a dicho atributo, por ejemplo:

```python
import datetime


class Subscription(object):
    # declaración de atributos
    def __init__(self, *args, **kwargs):
        # inicialización de lo que sea que haga falta

    @property
    def can_be_used(self):
        return not self.is_expired and not self.is_consumed

    @property
    def is_expired(self):
        return self.expiration_date <= datetime.date.today()

    @property
    def is_consumed(self):
        return self.used_credits >= self.total_credits
```

Como vemos, se simplifica un poco el acceso a estos atributos, se
encapsula la llamada a la función correspondiente y se da una interfaz
como si se tratara de un atributo, escondiendo la complejidad "tras
bastidores", de otra manera, las llamadas a las funciones serían
explícitas y el código se vería más complejo de lo que en realidad es.

Veamos un ejemplo un poco más complejo y en el que los descriptores
pudieran ayudar a simplificar la implementación manteniendo una interfaz
simple.

Digamos que necesitamos escribir una clase que representa una instancia
de libro en una casa editorial, todo bajo las siguientes reglas:

1.  Cada libro tiene un título, cuya longitud máxima y mínima son 500 y
    10 respectivamente
2.  Cada libro tiene un precio, que debe ser mayor que cero
3.  Cada libro tiene un número de existencias en inventario, que debe
    ser mayor que cero
4.  Cada libro tiene un año de publicación, que sebe ser un número mayor
    que 1300 (sí, ya se que hay mejores manera de hacer esto)
5.  Cada libro tiene un nombre de autor, cuya longitud máxima y mínima
    debe ser 50 y 10, respectivamente

Esto puede implementarse fácilmente usando *properties* y *setters*,
veamos como

```python
class Book(object):
    TITLE_MAX = 500
    TITLE_MIN = 10
    AUTHOR_MAX = 50
    AUTHOR_MIN = 10
    PUB_YEAR_MIN = 1300

    def __init__(self, title, author, price, inventory, year):
        self._title = None
        self._author = None
        self._price = None
        self._inventory = None
        self._year = None

        self.title = title
        self.author = author
        self.price = price
        self.inventory = inventory
        self.year = year


    # cool
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) < self.TITLE_MIN or len(value) > self.TITLE_MAX:
            raise ValueError('Longitud inválida')
        self._title = value

    # otra vez...
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if len(value) < self.AUTHOR_MIN or len(value) > self.AUTHOR_MAX:
            raise ValueError('Longitud inválida')
        self._author = value

    # Bueno, ya se hacen una idea
```

Habría que hacer lo mismo para cada atributo/propiedad, la interfaz es
simple, pero la implementación no es elegante, se ve un poco sucia y
repetitiva, sin embargo, es válida.

## Descriptores

Los descriptores vienen a resolver este problema, básicamente un
descriptor es una *property* encapsulada en una clase que nos permite
realizar las validaciones necesarias de manera simple. Algo así como un
"*property* con esteroides", veamos de qué se trata

```python
class MinMaxLengthString(object):
    def __init__(self, min_default, max_default):
        self.max_default = max_default
        self.min_default = min_default

        self.data = {}

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if len(value) > self.max_default or len(value) < self.min_default:
            raise ValueError('Longitud Inválida')

        self.data[instance] = value


class MinIntegerValue(self, min_value):
    def __init__(self, min_value):
        self.min_value = min_value

        self.data = {}

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if value < self.min_value:
            raise ValueError('Valor menor de lo permitido')

        self.data[instance] = value
```

Con esto, nuestra clase *Book* cambiaría de la siguiente manera:

```python
class Book(object):
    # Los descriptores siempre se colocan al nivel de la clase
    title = MinMaxLengthString(10, 500)
    author = MinMaxLengthString(10, 50)
    year = MinIntegerValue(1300)
    price = MinIntegerValue(0)
    inventory = MinIntegerValue(0)

    def __init__(self, title, author, price, inventory, year):
        self.title = title
        self.author = author
        self.price = price
        self.inventory = inventory
        self.year = year
```

Una implementación mucho más limpia y legible, veamos cómo funciona

Supongamos que ya hemos hecho algo como

```python
>>> b = Book('La Muerte de Honorio', 'Miguel Otero Silva', 50, 100, 1963)
```

1.  Al ejecutar, por ejemplo *b.year = 1200*, se va a invocar realmente
    *b.year.\_\_set\_\_(b, 1200)* realizando las validaciones necesarias
2.  Al ejecutar, por ejemplo, *t = b.title*, se va a invocar realmente
    *b.title.\_\_get\_\_(m, Book)* retornando el valor solicitado

Se puede hacer lo que sea en los métodos *\_\_get\_\_()* y
*\_\_set\_\_()* y, además, se puede definir otro método
*\_\_delete\_\_()* que es invocado cuando se borra el descriptor, por
ejemplo *del(b.author)*.


### Posible puesta de torta

Hay dos cosas que llaman la atención en los ejemplos de los
descriptores:

1.  La primera de ellas es que **se colocan a nivel de la clase**, esto
    es porque si se hace de otra manera, los métodos que implementan los
    descriptores pueden generar **comportamientos extraños**. Por
    ejemplo, si se coloca dentro del *\_\_init\_\_()*, el descriptor,
    pasa a ser un **atributo de la instancia** y retornará el valor que
    tiene como atributo de instancia, es decir, una instancia de la
    clase del descriptor, y no el valor que retorna el *\_\_get\_\_()*
    del descriptor.
2.  La segunda es que se utiliza un diccionario para almacenar asignar y
    retornar valores al descriptor, esto es porque al ser utilizados
    como **atributos de clase**, estos se instancian **sólo** una vez,
    es decir, se tiene sólo **una referencia** a esos objetos, por lo
    que todas las instancias de *Book*, comparten las mismas instancias
    de los respectivos descriptores, entonces, si se almacena el valor
    directamente en el descriptor, siempre obtendremos el **último valor
    asignado** para ese campo en alguna instancia de *Book*

Espero haber ayudado a mejorar un poco sus prácticas de programación (o
al menos las mías), si te parece que lo que escribo es útil, te invito
suscribirte a mi lista de correos en la caja que está a la derecha,
tengo varios proyectos en mente que estaré anunciando por esa vía y que
quizás te podrían interesar.

> Aprender a usar descriptores no sólo hace nuestro set de herramientas
> más grande, genera un entendimiento más profundo de cómo funciona
> Python y ayuda a apreciar la elegancia de su diseño. - Raymond
> Hettinger

Muchas gracias por leerme, no olviden suscribirse y seguirme, estaré
publicando más cosas sobre desarrollo y programación por esas vías.
