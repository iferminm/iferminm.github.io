Title: Cosas que he aprendido, Mixins
Date: 2014-12-19
Author: Israel Fermín Montilla
Tags: programación, mixins

A menudo nos ocurre que estamos programando y vemos que hay ciertos
métodos que se repiten en varias clases, esto es una señal de que ese
conjunto de métodos pueden abstraerse de alguna manera para no tener que
duplicar esa lógica, entonces, escribimos una clase base, con esos
métodos y luego simplemente la heredamos y todo cool.

Cuando esto ocurre por segunda vez en un subconjunto de las clases
*hijas*, pueden pasar dos cosas:

1.  Ese conjunto de métodos pertenece al mismo dominio del problema, en
    cuyo caso, los colocamos en la clase padre que corresponda
2.  Ese conjunto de métodos resuelve otro tipo de problemas o es más
    bien algún tipo de utilidad pero debe estar en esa clase por
    alguna razón.

En el segundo caso lo que uno tiende a hacer con lenguajes que soportan
herencia múltiple como Python es crear una nueva clase y agregarla a la
lista de clases padre de la clase en cuestión.

Conforme nuestro programa va creciendo en complejidad, podemos
enfrentarnos al famoso problema del diamante de la herencia múltiple,
los mixins son una solución limpia y sencilla para evitar este tipo de
inconvenientes que son un dolor de cabeza para depurar y agregan
complicaciones innecesarias.

## ¿Qué es un Mixin?

Un Mixin es una clase que hereda de la clase por defecto, *object* en el
caso de Python, y define un conjunto de métodos para agregar
comportamiento a alguna otra entidad. Un mixin por sí solo puede
resultar inútil, pero al combinarlos y agregarlos a una clase resultan
ser una herramienta muy potente que ayuda a la reutilización de código
sin ambigüedades y sin generar efectos colaterales.

## Ejemplos

Bueno, basta de palabrería y manos al teclado.

Supongamos que estamos desarrollando algo en *django* y necesitamos que
el usuario sea capaz de dejar comentarios, esta vista debe ser invocable
vía ajax. Debo hacerlo de manera que pueda reusar el código pues se que
en el futuro habrá más vistas que deben ser "ajax friendly"

```python
import json

from django.views.generic import CreateView
from django.http import HttpResponse

from app.models import Comment
from app.forms import CommentForm


class CommentCreateView(CreateView, JSONResponseMixin):
    model = Comment
    form = CommentForm
```

Como vemos, es la implementación de lo que vendría siendo una vista
basada en clases normal y corriente para procesar un formulario,
validarlo y crear un nuevo registro de *Comment*, sólo una cosa salta a
la vista: el *JSONResponseMixin*. Veamos qué hace:

```python
class JSONResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        return self.get_json_response(context, **kwargs)

    def get_json_response(self, data, **kwargs):
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            **kwargs
        )
```

Y eso es todo, luego, si necesito hacer que alguna otra vista sea "ajax
friendly", simplemente tengo que hacer que herede del
*JSONResponseMixin*. Algo importante acá es que si necesito serializar
objetos complejos, *json.dumps()* no será suficiente, debería escribir
mi propio método para convertirlo en *JSON* y enviarlo.

Si te parece útil o interesante lo que escribo, suscríbete a mi lista de
correos en la caja que está a la derecha, tengo algunas cosas en mente
que estaré anunciando por esa vía. Gracias, de nuevo, por leerme.
