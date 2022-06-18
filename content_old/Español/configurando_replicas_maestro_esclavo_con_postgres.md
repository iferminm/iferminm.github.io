Title: Configurando réplicas Maestro-Esclavo con Postgres
Date: 2011-11-10
Author: Israel Fermín Montilla
Tags: bases de dato, replicación, postgres

Muchas veces, por alguna razón, hacemos desde la capa de aplicación
cientos de validaciones y procesos que, si sabemos cómo, podríamos
delegar en el manejador de base de datos.

Las validaciones de reglas de negocio son un ejemplo muy frecuente de
ello, tendemos, por ejemplo, a implementar validaciones redundantes (en
el caso de entornos web) del lado del cliente, utilizando AJAX, y del
lado del servidor, utilizando el lenguaje de programación que más nos
agrade. Esto, añade un nivel de complejidad a nuestro sistema, cuando,
muy tranquilamente, podríamos delegar esa validación en nuestro
manejador de base de datos a través de un Trigger, con la ventaja de que
si algún día, otro sistema necesita conectarse a la base de datos, las
reglas de negocio están implementadas directamente en el manejador y,
como ya estamos acostumbrados, todo corre más rápido en el nivel más
bajo.

Ahora bien, ¿por qué empiezo diciendo todo eso?, simplemente por hacer
referencia a un ejemplo bastante común, en el que nosotros,
programadores, desarrolladores, ingenieros, o como quieran llamarnos,
hacemos uso (o quizás sub-uso) de un software muy sofisticado, como lo
es un Manejador de Base de Datos y, tendemos a pensar, que es sólo un
pote para guardar datos que, además, habla un lenguaje extraño llamado
SQL. Otra de las cosas que, algunas veces, hacemos y nos hacen parecer
novatos es actualizar dos servidores de base de datos distintos
disparando sentencias hacia los dos, o tres, o cuantos sean. Esto añade
un nivel de complejidad innecesario a nuestra aplicación, además de
estar fuertemente acoplado con la arquitectura física (hardware) del
sistema implementado, si el número de servidores a sincronizar cambia,
será necesario también realizar modificaciones a nivel de código o de
configuración del programa y, además, desaprovechamos la potencia que
nos ofrece un manejador de base de datos.

PostgresSQL nos ofrece la posibilidad de sincronizar dos servidores de
base de datos mediante Replicación de manera nativa. Existen distintos
tipos de replicación de servidores, en este caso, configuraremos un
esquema Maestro-Esclavo, en el que mi servidor Maestro, recibe y ejecuta
todas las transacciones y, además, actualiza a mi servidor Esclavo, que,
únicamente, utilizo para realizar consultas. Empezamos por instalar la
última versión disponible de Postgres, utilizando el gestor de paquetes
de nuestra distribución de Linux favorita, para este ejemplo, utilicé
Debian Wheezy (Testing) y Postgres 9.1.


## Configurando el Maestro

El maestro, es el nodo que ejecuta todas las transacciones de base de
datos, digamos que puede realizar todas las operaciones CRUD. Empecemos
por establecer ciertos valores de configuración para el manejador en el
archivo /etc/postgresql/9.1/main/postgresql.conf. Debemos configurar los
siguientes valores:

```
listen_addresses = '*'
wal_level = hot_standby
wal_sync_method = fsync
max_wal_senders = 2
wal_keep_segments = 8
```

Ahora bien, analicemos este segmento de configuración:

-   *listen\_addresses:* establece las direcciones IP de donde mi
    servidor va a aceptar peticiones, este parámetro acepta valores
    separados por coma o el caracter asterisco, como en este caso, para
    especificar que va a aceptar peticiones de cualquier host, de no ser
    así, sólo las IP listadas podrían sincronizar la base de datos.
-   *wal\_level:* donde **wal** quiere decir **Write Ahead Log** y es
    una estrategia que implementan los manejadores para cumplir con las
    propiedades de Atomicidad y Durabilidad de las transacciones
    (¿recuerdan la regla ACID?) y consiste en escribir en un archivo de
    bitácora todas las modificaciones realizadas a la base de datos. En
    Postgres existen tres: **minimal**, que omite algunas operaciones de
    escritura para hacer las operacionas más rápido, pero no guarda
    información suficiente para reconstruir la base de datos a partir de
    un archivo inicial y logs de este tipo, **hot\_standby** y
    **archive**, almacenan toda la información necesaria para hacer la
    reconstrucción completa de los datos, pero únicamente
    **hot\_standby** permite implementar replicación de base de datos
    hacia servidores remotos.
-   *wal\_sync\_method:* es el método que utilizará el manejador para
    forzar las actualizaciones utilizando **WAL**. En este caso,
    utilizamos **fsync** que se asegura de que los cambios sean escritos
    físicamente en la base de datos copia, más información sobre los
    métodos de sincronización disponibles puede conseguirse en \[1\].
-   *max\_wal\_senders:* establece el número de sincronizaciones
    concurrentes que puede ejecutar el servidor.
-   *wal\_keep\_segments*, establece el número de *WAL* logs que el
    servidor guardará en el directorio **pg\_xlog**, estos logs son
    utilizados para realizar las actualizaciones vía streaming. Una vez
    hecho lo anterior, tenemos la configuración básica de Postgres para
    hacer replicación Maestro-Esclavo vía streaming.

Ahora, debemos agregar una regla más de acceso al **pg\_hba.conf**, para
permitir a los esclavos conectarse al servidor maestro:

``` 
host replication all 10.1.1.8/32 trust
```

Con esa línea, estamos configurando el servidor para que permita
conexiones a todos los usuarios con permiso de replicación desde la
sub-red **10.1.1.8/32**.

Ahora, generamos los **WAL**, para ello, ejecutamos lo siguiente en el
terminal SQL de Postgres:

```sql
SELECT pg_start_backup('1')
```

Mientras eso esté ocurriendo, en otro terminal, ejecutamos lo siguiente:

```
cd /var/lib/postgresql/9.1 # tar czvf backup.tgz main
```

Con esto estamos comprimiendo el directorio de datos de Postgres. Una
vez hecho esto, detenemos la generación de WAL:

```sql
SELECT pg_stop_backup()
```

El asunto general se resume con la siguiente ecuación:

backup inconsistente + WAL = restauración a estado consistente.

Estos WAL, se generan en el directorio **pg\_xlog**, y debemos tomar el
último que fue escrito.


## Configurando el Esclavo

Lo primero que debemos hacer es sustituir el directorio de datos de esta
instancia de Postgres por el directorio de datos del Maestro. Luego,
creamos un directorio *recovery*, donde copiaremos el último WAL del
directorio pg\_xlog. Adicionalmente, debemos modificar el
postgresql.conf con las siguientes variables:

```
hot_standby = on wal_level = hot_standby``
```

Ahora, creamos un archivo de configuración en la raíz del directorio de
datos para establecer las siguientes opciones:

```
standby_mode = 'on'
primary_conninfo = 'host=[host_ip] port=5432 user=root password=[some_password]'
restore_command = 'cp /var/lib/postgresql/9.1/main/recovery/%f %p'
```

Con esto le decimos al servidor que va a esperar réplicas de
**primary\_conninfo**, además, el **restore\_command** indica dónde se
encuentra el respaldo inicial inconsistente. Finalmente, nos aseguramos
de que los roles tengan permiso de replicación:

```sql
SELECT * FROM pg_roles
```

y, de no tener permisos de replicación, alteramos los roles necesarios
para ello:

```sql
ALTER ROLE nombre WITH REPLICATION
```

Una vez hecho todo esto, ya hemos configurado un sistema de replicación
Maestro-Esclavo utilizando Postgres como sistema manejador de base de
datos, y no hizo falta una toalla para eso. Fácil ¿no?.

\[1\]
<http://developer.postgresql.org/pgdocs/postgres/runtime-config-wal.html>

\[2\]
<http://developer.postgresql.org/pgdocs/postgres/runtime-config-replication.html#GUC-HOT-STANDBY>
