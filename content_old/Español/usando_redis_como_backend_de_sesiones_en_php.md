Title: Usando Redis como backend de sesiones en php
Date: 2014-10-19
Author: Israel Fermín Montilla
Tags: programación, redis, web, php

Bueno, sí, leyeron bien el título, luego de años me tocó trabajar de
nuevo con php en la oficina, dejen el escándalo.

Siendo sincero, las cosas parecieran haber mejorado mucho desde la
última vez que hice (o traté de hacer) algo con php, era php 4.algo en
aquel momento, jugaba con *Symfony* y fue una desgracia que no se la
deseo ni a mi peor enemigo.

Luego, más recientemente jugué con *Yii*, un framework para desarrollo
web con php que me pareció bastante bueno y es una alternativa que le
recomiendo a todo aquel que no tenga más remedio que desarrollar usando
este lenguaje, algunos me dicen que pruebe *Lavarel* y seguramente me
cambie a php, pero dudo mucho que algo me atrape tanto como *Python*,
sin importar el framework, incluso *Web2Py* tiene muchas cosas
rescatables.

Bueno, manos a la obra:

## La historia:

En la oficina están en una onda de *intercambiar código* con nuestros
aliados comerciales o "páginas hermanas", el problema es que nosotros
desarrollamos en *Python* + *django* y a veces *bottle* y todos los
demás en php.

Este proyecto en particular, fue desarrollado con un framework hecho en
casa en php y es usado como una librería para autenticación utilizando
servicios de 3eros, es decir, *OAuth*. Esto en un mundo ideal, donde
todo lo programas con php y puedes simplemente hacer:

```php
use project\module\submodule\file;
```

y todo bien.

## El problema:

Obviamente, no podemos importar código php en nuestro proyecto en
*Python*, entonces, la solución fue simplemente, adaptar la librería
provista por la otra gente para usarla como un servicio, la cosa salió
bastante bien, pero al momento de poner todo en producción, nos dimos
cuenta de algo.

Se desplegaron dos instancias de este servicio detrás de un balanceador
de carga, para autenticar usando *OAuth*, es necesario golpear más de
una vez el servicio, entonces, estando dos (o más) instancias detrás de
un balanceador de carga, no tienes manera de garantizar que quien
atiende el primer *request*, es el mismo que atiende el segundo.

A esto súmale que se guarda cierta información en la sesión para
mantenerla durante todo el proceso de autenticación y php almacena las
variables de sesión en un archivo local del servidor.

## La solución:

Sin pensarlo mucho, la solución es tener *algo* que todas las instancias
compartan para escribir la información relacionada a las sesiones, puede
ser una base de datos *MySQL*, un sistema de archivos compartido con
*NFS*, lo que sea, nosotros optamos por *Redis* porque es lo más rápido
y fácil de configurar, responde rápido porque mantiene ciertas cosas en
memoria y es difícil que pierda datos, puede pasar, pero igual es
información transitoria que no nos interesa conservar.

### Implementación:

Luego de investigar unos minutos, nos dimos cuenta de que no era nada
del otro mundo, simplemente cambiar unos parámetros de configuración en
los respectivos archivos *php.ini*, instalar un par de paquetes y listo.

#### Instalación de paquetes:

Descargamos
[php-redis](https://github.com/nicolasff/phpredis)

```bash
sudo aptitude install php5-dev
cd php_redis/
sudo phpize
sudo ./configure
sudo make
sudo make install
```

#### php.ini:

Simplemente debemos modificar las siguientes líneas:

```
extension=redis.so
[Session]
session.save_handler=redis
session.save_path="tcp://localhost:6379"
```

El *save_path* debe tener la IP y el Puerto donde nuestra instancia de
redis estará escuchando.

## Conclusión:

Ciertamente las cosas han mejorado sólo un poco en php desde la última
vez que lo usé para algo más que un proyecto de juguete. Sin embargo no
me veo programando en php a menos que sea estrictamente necesario por
las características o restricciones de un proyecto en particular.

Respecto al servicio de autenticación, ya está en producción, pareciera
estar funcionando bastante bien, sin embargo hay muchas cosas con las
que no estamos contentos, seguramente terminemos cambiándolo por una
versión 2.0, seguramente en *Python* y desarrollado por nosotros pero,
al menos por ahora, funciona y hace el trabajo.
