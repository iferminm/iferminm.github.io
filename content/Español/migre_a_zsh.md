Title: Migré a ZSH
Date: 2015-05-26
Author: Israel Fermín Montilla
Tags: zsh, shell, herramientas

Es bien sabido por todos que en Linux y en el Open Source en general,
uno es libre de elegir todas y cada una de las partes del sistema que va
a configurar para su computadora personal o de trabajo, la línea de
comandos no es excepción.

Por defecto, viene configurado
[BASH](http://es.wikipedia.org/wiki/Bash) en todos
los sistemas linux, sin embargo, es posible cambiarlo sin ningún tipo de
problemas, en mi caso, luego de investigar un poquito, elegí una
combinación que me ha resultado bastante bien durante las últimas dos
semanas: [ZSH](http://es.wikipedia.org/wiki/Zsh) +
un plugin llamado [oh my
zsh](https://github.com/robbyrussell/oh-my-zsh).

Acá las razones por las cuales decidí migrar y por qué me ha parecido
tan genial:

## YOLO

Siempre digo que quiero probar herramientas nuevas, pero nunca pongo
manos a la obra, en los últimos meses me he propuesto a organizarme y
crear hábitos, utilizando distintos hacks, que me permitan llevar a cabo
todo lo que me pasa por la mente sin descuidar cosas importantes como la
familia y el trabajo. Así que, quise probar *ZSH* a ver qué tal, ¿qué
mejor momento que ahora?

## No es un cambio muy traumático

*BASH* nace en 1989, *ZSH* nace en 1990, mantiene compatibilidad con
todos los comandos de *BASH* y agrega nuevas funcionalidades que vamos a
ver en las razones siguientes :-).

## El autocompletado de ZSH

*ZSH* tiene una capacidad increíble de autocompletar, no sólo te muestra
las posibles opciones, cosa que también hace *BASH*, sino que te permite
seleccionarla de manera interactiva, cosa que *BASH* no hace de manera
natural.

![Autocompletado
interactivo](https://dl.dropboxusercontent.com/u/3437671/blog/zsh/foto1.png)
Además, no sólo completa rutas y comandos básicos del sistema operativo,
con *Oh My ZSH* también tiene autocompletado para git, cosa que me
resulta muy útil porque es una herramienta que uso todos los días en la
oficina y para proyectos personales, este autocompletado incluye una
pequeña descripción de lo que hace cada comando de git.

![git &lt;TAB&gt; y esto
aparece](https://dl.dropboxusercontent.com/u/3437671/blog/zsh/foto2.png)

### Completación de rutas

No, no es lo mismo que la anterior, este es algo mucho más potente que
no vi nunca en *BASH* supongamos que soy perezoso para escribir, y
quiero ir a */home/israelord/Work*, que es la ruta donde tengo todos mis
proyectos, tanto de la oficina como freelance. Se que ese es el único
patrón que coincide, simplemente escribo */h/i/W* y al presionar tab, me
autocompleta la ruta.

En caso que haya ambigüedad, como por ejemplo, si quiero ir a
*/usr/local/bin*, al escribir */u/l/b*, hay dos opciones para la *l*,
bajo el directorio */user*: *lib* o *local*. En este caso, me permitirá
seleccionar la opción correcta de manera interactiva, tal como en el
ejemplo anterior, antes de terminar el autocompletado. Puedo resolver
esto simplemente escribiendo */u/lo/b* y me generará la ruta correcta de
una vez, simplemente debo completar más la parte de la ruta que genera
el conflicto para que sea única, aunque la selección interactiva no me
disgusta para nada.

### Cambios de directorio

Sí, ya se, para eso está *cd*, pero este es un caso de uso de cd que no
vi en *BASH*, supongamos que estoy en la ruta del ejemplo anterior
*/usr/local/bin*, pero en realidad quería ir a */usr/local/sbin*. En vez
de hacer como en *BASH* *cd ../sbin*, puedo hacer *cd bin sbin* y me
lleva allí. Funciona igual con sub rutas, puedo hacer *cd local/sbin
games* y me lleva a */usr/games*, por ejemplo.

Esto es especialmente útil cuando tengo proyectos con la misma
estructura, por ejemplo, estoy en
*/home/israelord/proyecto1/auth/views/*, simplemente con hacer *cd
proyecto1 proyecto2*, me lleva a
*/home/israelord/proyecto1/auth/views/*. No más cd ../../../../

### Autocorrector

No mucho que decir, si me equivoco y escribo gut, me corrige y escribe
git, por ejemplo, si hay más de un posible patrón, me muestra la
selección interactiva que vimos antes.

### Renombrado de archivos en batch

Supongamos que tengo 700 fotos que y los nombres son cosas como
IMG\_2193192873198723.jpg, quiero renombrarlas a algo más manejable,
como "foto\_1.jpg", "foto\_2.jpg" y así.

Bueno, simplemente escribo

```bash
zmv '(*).jpg' 'foto_$1.jpg'
```

Y listo!.

## Oh My ZSH

Es un plugin que extiende *ZSH* y, además, tiene varios addons, por
ahora sólo estoy usando el de *git* porque tiene muchísimos alias útiles
para las tareas de día a día con *git* que les dejaré de tarea revisar,
pero la diferencia es abismal respeto a lo que escribirías normalmente,
por ejemplo:

En vez de git push origin master con Oh my zsh simplemente escribo
ggpush ;-)

### Instalando

*ZSH* normalmente está instalado, simplemente hay que modificar nuestro
usuario para que sea el terminal por defecto

```bash
chsh -s /bin/zsh
```

Para instalar el plugin *Oh my ZSH*, basta con ejecutar

```bash
curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
```

O, si preferimos usar *wget*

```bash
wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh
```
