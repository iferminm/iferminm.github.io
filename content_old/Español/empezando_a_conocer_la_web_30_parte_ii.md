Title: Empezando a conocer la Web 3.0 (Parte II)
Date: 2011-06-14
Author: Israel Fermín Montilla
Tags: web semántica, internet, web 3.0

by [Israel Fermín Montilla](author/israel-fermin-montilla.html) on Tue
14 Jun, 2011

Hace un tiempo, publiqué el primero de una serie de artículos acerca de
La Web Semántica, en el que daba una introducción y exponía la visión de
la W3C sobre el rumbo que debería tomar la Web en su "versión 3.0", si
aún no lo has leido,
[aún estás a tiempo](http://codersvenezuela.com/post/empezando-a-conocer-la-web-3-0-parte-i/50).
En esta segunda entrega, expondré algunos conceptos que es
necesario tener claros si deseas adentrarte en este nuevo mundo, así
como también, daré una visión, un poco futurista (casi sacada de una
película de Ciencia Ficción), de las cosas que serán posibles una vez se
alcance a estandarizar todos los conceptos y tecnologías de la Web
Semántica a lo ancho, largo y profundo de la World Wide Web.

El primero de los conceptos que debemos tener claro es el de URI
(Universal Resource Identifier) y URL (Universal Resource Locator), y
las diferencias y similitudes que existen entre ellos pues, es de
intuirse, que nos servirán más adelante. Luego de entender eso, podemos
avanzar y adentrarnos en el mundo de las Ontologías, un concepto del
campo de la Inteligencia Artificial adaptado a la Web Semántica. Una vez
asimilado todo lo referente a las Ontologías, podemos irnos a estudiar
algo de lógica y consultas sobre dichas ontologías para, después, ver
algo acerca de Motores de Inferencia, que serán nuestro más grande
aliado al desarrollar aplicaciones que implementen tecnologías de la Web
Semántica. En este artículo, me concentraré en los dos primeros, es
decir, URL, URI y Ontologías. Algo que parece causar mucha confusión en
estudiantes, son los URI y los URL. Espero despejar cualquier duda en el
siguiente párrafo: Un Identificador Universal de Recurso o URI, por sus
siglas en inglés, es un elemento que nos permite simplemente saber
"quién" es ese recurso. Si me permite identificar el recurso de manera
inequívoca, quiere decir que debe ser único para cada uno. Por su parte,
el Localizador Universal de Recurso, o URL por sus siglas en inglés, me
permite saber la ubicación de ese recurso, debe resultar obvio que
también debe ser único para cada uno pues dos recursos no pueden tener
la misma ubicación. Si exportamos estos conceptos al mundo real y los
aplicamos a personas, un URI podría ser su Cédula de Identidad, que no
me da acceso al recurso, pero me permite saber quién es, un URL, podría
ser su dirección postal + habitación en la que se encuentra (asumiendo
que en Venezuela la gente vive tan cómoda que no necesita compartir
cuarto con nadie) o, incluso, su número telefónico, ambos me dan acceso
al recurso y, de alguna u otra manera, también me permiten conocer quién
es. En pocas palabras, un URL es un URI que, además, me permite conocer
la ubicación del sujeto.

Es necesario tener claro todo lo anterior ya que en la Web Semántica no
se habla de Páginas o Sitios Web, se busca generalizar un poco más ya
que, en la Web, no sólo existen documentos HTML que dan forma a los
Portales Web, sino también Videos, Fotos, documentos PDF, Música,
Servicios Web, en fin, sería mucho más fácil decir qué es lo que no se
encuentra en la Internet. Es por ello que la Web Semántica habla de
Recursos, más allá de su tipo. Ahora bien, la Web Semántica se basa en
modelos de conocimiento bien estructurado, estos modelos de conocimiento
se conocen en el mundo de la Inteligencia Artificial como Ontologías.

Una Ontología no es más que una representación estructurada del
conocimiento de un área específica, de allí que muchos buscadores que
implementan 100% tecnología de Web Semántica sean específicos para un
tema dado. Estos modelos, en el ámbito que nos compete, se utilizan para
describir recursos, a los cuales nos referimos mediante URI's, y, en
cierta forma, darle al computador la capacidad de "entender" de qué
habla dicho recurso y cuáles son sus recursos relacionados, de esta
manera, comenzamos a construir nuestra infraestructura de meta-datos
para realizar búsquedas contextualizadas y con más sentido para el
usuario. La manera como una Ontología organiza el conocimiento, es a
través de una estructura de meta-conocimiento. Esta estructura se
construye a partir de un concepto con el cual la mayoría de los
programadores estamos famimliarizados desde tempranos años de la
carrera, las Clases, todo meta-conocimiento es modelable a través de
Clases. Es de intuirse que se mantienen los conceptos de Herencia y
Polimorfismo también dentro de las Ontologías. Por ejemplo, imaginemos
una MICRO-Ontología de la Vida Salvaje de África\[1\]. Empezando a
pensar al respecto, nos percatamos de que la sabia madre naturaleza ya
nos facilitó con dos clases bien diferenciadas: "Animales" y "Plantas".
Una Ontología, también me permite crear relaciones entre clases, con
propócitos didácticos, imaginemos las clases "Tallo", "Rama" y "Hoja"
que "son parte" de una "Planta", creo que la relación es bastante obvia,
nuestra estructura de composición para la clase "Planta" sería: "Hoja",
es parte de: "Rama", es parte de: "Tallo", es parte de: "Planta".
Podemos complicarlo aún más, podríamos definir clases de "Forma"
(triángulo, rombo, etc) y relacionarlas a "Hoja" y crear la relación
"tiene forma de" para describir cómo es la hoja de una Planta dada,
pero, por ahora, dejémoslo así. Por otro lado, la clase "Animal", tiene
dos subclases muy fáciles de inferir: "Carnívoro" y "Herbívoro", ambas
sub-clases son también "Animales", esto es una estructura de Herencia
pues, una instancia de "Herbívoro" o de "Carnívoro" es también un
"Animal".

Nuestra estructura de Herencia para "Animal" quedaría así: "Carnívoro",
es un: "Animal". "Herbívoro", es un: "Animal". Pero, ahora, ¿cómo se
relacionan todas nuestras clases entre sí?. Bueno, a través de una
relación obviamente, pero, ¿Cuál?. Bueno, un animal debe comer ¿no?.
Entonces, un "Herbívoro" come "Planta" y un "Carnívoro" come
"Herbívoro", también podría crear la relación inversa "es comido por",
por ejemplo. Hasta ahora sólo tenemos el Meta-Conocimiento, es decir,
las descripciones de los recursos, ahora debo agregar recursos, por
ejemplo, si digo: "León" es un "Carnívoro"; "Arbusto" es una "Planta" y
"Zebra" es un "Herbívoro" Automáticamente, podríamos inferir que el
"Arbusto" está conpuesto por "Tallo", "Rama" y "Hoja", es comido por
"Zebra", que a su vez es comido por "León". Si hacemos una analogía con
la Programación Orientada a Objetos, mis clases, seguirían siendo
clases, pero los recursos a los que hacen referencia, serían los objetos
que son instanciados en una clase determinada.

Obviamente, pueden hacerse ontologías muy complejas, lo que aquí muestro
a manera de ejemplo es sólo la punta del iceberg pues los lenguajes de
ontologías para la Web Semántica son sumamente flexibles y potentes: RDF
y OWL\[2\] (que no es más que una extensión de RDF), posteriormente
dedicaré un artículo para profundizar más sobre ellos. Las clases
RDF/OWL, definen y describen mis recursos, y las relaciones entre estas
clases, definen ciertas reglas básicas de inferencia lógica que pueden
ser aprovechadas en un nivel superior por un Motor de Inferencia\[3\]
para resolver consultas sobre una ontología y, a partir de esas premisas
básicas, deducir nuevo conocimiento no explícito directamente en el
modelo de conocimiento.

Imaginemos ahora una WWW totalmente enlazada, totalmente integrada con
la Web Semántica, cuando esto ocurra, serán agentes\[4\] quienes nos
ayuden a realizar búsquedas a través de la web, examinando ontologías,
extrayendo información que se adapte a nuestra consulta e interpretando,
a través de reglas de inferencia bien definidas, cuáles recursos cumplen
mejor con nuestra solicitud. Supongamos que Alan, es un empresario muy
ocupado y su madre lo llamó anoche porque siente dolor en la zona
abdominal desde hace unos días y siente que debería visitar a un médico.
Alan, consulta la Internet desde su TabletPC, a través de su agente,
solicitando las clínicas que se encuentren en 10km a la redonda de la
casa de su madre, organizadas según su reputación. El agente revisa la
ubicación de la casa de su madre (almacenada en el Tablet gracias a la
tecnología de GPS) y consulta una Ontología con las clínicas de la
ciudad y, además, busca en el Servicio Web de la Sociedad Médica
Venezolana (bajo las circunstancias descritas en el párrafo anterior,
debería existir), la lista de las mejores clínicas para poder cumplir
con el patrón de ordenamiento que Alan solicitó. Luego de revisar los
resultados, Alan le pregunta al agente de dónde obtuvo la información,
este le redirige al portal de la Sociedad Médica Venezolana. Alan revisa
las primeras tres clínicas y, finalmente se decide por el Hospital de
Clínicas Caracas (HCC), pues no queda muy lejos de la casa de su madre y
figura de 3ero en la lista de resultados. El agente del HCC le pregunta
qué síntomas presenta, Alan escribe "Dolor Abdominal", el agente le
recomienda visitar a un Gastroenterólogo y le devuelve una lista de los
médicos de esa especialidad del Hospital. Alan se da cuenta de que el
2do en la lista, es un viejo amigo del Colegio y decide solicitar una
cita con él lo más pronto posible, el agente del Hospital le informa que
la cita más próxima es para dentro de dos días, entre las 14:00 y las
18:00, y su agente le recuerda que tiene un par de reuniones en ese
intervalo de tiempo. Alan revisa su agenda y se da cuenta que son dos
reuniones de prioridad menor, pide a su agente que las reprograme y
solicite la cita médica. El agente de Alan, de manera automática, se
comunica con los agentes de las personas involucradas en las reuniones
para reprogramar las citas y, posteriormente se comunica con el agente
del HCC para colocar la cita para dentro de dos días a la hora
mencionada. Todo esto será posible si la información se encuentra
totalmente enlazada y disponible en línea, los recursos son descritos de
manera bien definida y las reglas de inferencia son bien explícitas, es
por ello que es necesario que más personas se interesen en este tema de
manera técnica pues, el futuro de la Internet, está tocando a nuestras
puertas y, la Web Semántica, no puede quedarse enclaustrada dentro de la
academia y ser dominado únicamente por grupos de investigación
científica. Espero haber motivado a alguien más a estudiar dentro de
este campo. Hasta un próximo artículo.

\[1\] Digo Micro-Ontología porque si hacemos la ontología completa, creo
que acabaríamos con todo el espacio disponible en este servidor.

\[2\] Ambos lenguajes están en proceso de definición por el World Wide
Web Consorcium (W3C), el avance puede ser seguido a través el sitio web
del W3C.

\[3\] JENA y Virtuoso son los que parecieran ser más utilizados.

\[4\] Un agente, en informática, es una pieza de software que realiza
una tarea específica de manera automática, es una espécie de "robot".
