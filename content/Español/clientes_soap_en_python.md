Title: Clientes SOAP en Python
Date: 2013-08-18
Author: Israel Fermín Montilla
Tags: python, soap, soa, suds

Como todos saben, y algunos me chalequean por eso, en la primera mitad
de 2013 cambié de trabajo dos veces, estaba algo aburrido en Metamax y
decidí aceptar una oportunidad en 4geeks, junto con una serie de
proyectos para una empresa en el extranjero que pintaban bastante bien,
una vez que terminé los proyectos de la otra empresa, terminé
enamorándome del proyecto que desarrollaba desde 4geeks y uniéndome al
startup a tiempo completo.

# La historia
La historia en 4geeks es muy graciosa, un tal Saúl Lustgarten llevaba
tiempo escribiendo en todas las listas de correo donde estoy pidiendo un
desarrollador Python, incluso me contactó personalmente varias veces vía
email y a través de *LinkedIn* para desarrollar su *startup*, una
central telefónica en la nube llamada *RingTu*, el tema era que no me
resultaba atractivo, así que en ese momento acepté la oferta de 4geeks.

El primer día en 4geeks, me informan acerca del proyecto que iba a
desarrollar, "vas a hacer uno de los startups de Wayra, es una central
telefónica en la nube" y yo "¿RingTu?", "sí ese mismo", vaya, al parecer
hasta se las arregló para que desde 4geeks desarrollara su startup,
jajajajajajaja.

Básicamente lo que debía hacer era unos wrappers para unos servicios web
que ellos consumen, ese era sólo el inicio del proyecto, pensé que sería
divertido, ya había hecho wrappers para otros servicios web, y en Python
es muy fácil hacer clientes para servicios web, sin importar si hablan
JSON o XML o algún protocolo propio, la cosa se puso esotérica cuando vi
que todos los URL de los servicios con los que iba a trabajar terminaban
en .wsdl.

# REST... NO! vas a usar SOAP
¿SOAP?, con el boom de REST ¿quién usa SOAP?, en fin, ¿qué tan difícil
puede ser?, en Java es realmente fácil escribir clientes y servicios web
usando SOAP y en Python no debe ser la excepción, hay librerías para
todo, dejé de hacerme preguntas acerca del sentido de la vida, el
universo y todo lo demás y puse manos a la obra a investigar alguna
buena librería que me facilitara el trabajo.

Luego de unos minutos leyendo en *StackOverflow*, vi que al parecer suds
era la mejor opción, no se veía tan abandonada y, comparada a las demás
opciones, tenía una documentación decente.

## Instalando suds

```bash
pip install suds
```

Recuerden que siempre es buena práctica trabajar con virtualenvs y,
además, es muy buena opción el hecho de utilizar virtualenvwrapper para
gestionarlos.

## Empezando a desarrollar tu cliente SOAP
Una vez que tenemos suds ya instalado, es sólo cuestión de empezar a
utilizarla, para hacer clientes, que es de lo que hablaré en este post,
sólo nos interesa la clase definida en *suds.client.Client*.

### SOAP 101
Si repasamos un poco de teoría acerca de los servicios web sobre el
protocolo SOAP, veremos que se convirtió en la capa subyacente para
servicios complejos basados en WSDL, que es una manera de especificar
los objetos y métodos que expone un servicio web y a los que el cliente
puede tener acceso. WSDL es un acrónimo que significa *Web Service
Description Language*.

Toda la definición de servicios web SOAP se hace en un documento WSDL,
que no es mas que un XML donde se define todo lo que este servicio
expone para ser consumido por sus clientes. De igual manera, el pase de
mensajes (soap messages) entre el cliente y el servidor, se hace en
formato XML.

A continuación un ejemplo de documento WSDL:

```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <description xmlns="http://www.w3.org/ns/wsdl"
                 xmlns:tns="http://www.tmsws.com/wsdl20sample"
                 xmlns:whttp="http://schemas.xmlsoap.org/wsdl/http/"
                 xmlns:wsoap="http://schemas.xmlsoap.org/wsdl/soap/"
                 targetNamespace="http://www.tmsws.com/wsdl20sample">

    <!-- Tipos Abstractos -->
       <types>
          <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
                    xmlns="http://www.tmsws.com/wsdl20sample"
                    targetNamespace="http://www.example.com/wsdl20sample">

             <xs:element name="request"> ... </xs:element>
             <xs:element name="response"> ... </xs:element>
          </xs:schema>
       </types>

    <!-- Interfaces abstractas -->
       <interface name="Interface1">
          <fault name="Error1" element="tns:response"/>
          <operation name="Opp1" pattern="http://www.w3.org/ns/wsdl/in-out">
             <input messageLabel="In" element="tns:request"/>
             <output messageLabel="Out" element="tns:response"/>
          </operation>
       </interface>

    <!-- Interface concreta sobre HTTP -->
       <binding name="HttpBinding" interface="tns:Interface1"
                type="http://www.w3.org/ns/wsdl/http">
          <operation ref="tns:Get" whttp:method="GET"/>
       </binding>

    <!-- Interface concreta sobre SOAP -->
       <binding name="SoapBinding" interface="tns:Interface1"
                type="http://www.w3.org/ns/wsdl/soap"
                wsoap:protocol="http://www.w3.org/2003/05/soap/bindings/HTTP/"
                wsoap:mepDefault="http://www.w3.org/2003/05/soap/mep/request-response">
          <operation ref="tns:Ge99t" />
       </binding>


    <!-- Endpoints que ofrecen el servicio -->
       <service name="Service1" interface="tns:Interface1">
          <endpoint name="HttpEndpoint"
                    binding="tns:HttpBinding"
                    address="http://www.example.com/rest/"/>
          <endpoint name="SoapEndpoint"
                    binding="tns:SoapBinding"
                    address="http://www.example.com/soap/"/>
       </service>
    </description>
```

La sección *types* describe los tipos de dato a los que da soporte el
servicio web que se está describiendo. Las *interfaces*, definen un
servicio como tal, es decir, las operaciones que pueden ser realizadas y
los mensajes que son soportados para realizar cada operación. Los
*bindings* especifican la interface y cómo deben ser pasados los
mensajes e incluso el protocolo que debe ser utilizado para el
transporte. Finalmente, los *endpoints*, definen los puntos de conexión
con el servicio web.

Por otra parte, un mensaje SOAP debería verse de la siguiente manera:

```xml
    POST /InStock HTTP/1.1
    Host: www.example.org
    Content-Type: application/soap+xml; charset=utf-8
    Content-Length: 299
    SOAPAction: "http://www.w3.org/2003/05/soap-envelope"

    <?xml version="1.0"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
        <soap:Header>
        </soap:Header>
        <soap:Body>
            <m:GetStockPrice xmlns:m="http://www.example.org/stock">
                <m:StockName>IBM</m:StockName>
            </m:GetStockPrice>
        </soap:Body>
    </soap:Envelope>
```

En un mensaje, el *envelope* es lo que identifica el XML como un mensaje
SOAP, el *header* contiene información de encabezado, como por ejemplo,
llaves de autenticación o tokens de acceso. Finalmente, el *body* o
cuerpo del mensaje, es el que contiene el mensaje como tal que se está
enviando, ya sea en solicitud o respuesta del servicio.

En este caso, se está invocando una función remota *GetStockPrice*
definida en un namespace *m* del wsdl que describe este servicio. A esta
función remota se le está enviando un argumento llamado *StockName* y el
valor de este argumento es *IBM*, el servicio debería retornar el precio
del producto cuyo *StockName* sea *IBM*

## Inicializando el cliente SOAP consumiendo el WSDL del servicio
Para que pueda darse el intercambio de información entre un cliente y un
servidor SOAP, ambos deben tener conocimiento de lo que está definido en
el descriptor del servicio, es decir, ambos deben tener acceso al WSDL,
es por ello que lo usual es que el proveedor del servicio web exponga el
documento en un URL accesible.

Para este tutorial, usaremos este servicio web:
<http://www.webservicex.com/globalweather.asmx?WSDL>, que es un servicio
web de clima. Acá:
<http://www.service-repository.com/operation/operations?id=4> podemos
observar las operaciones y sus parámetros en un formato amigable al
humano :-).

Lo primero es, en nuestro caso, construir una instancia de
suds.client.Client que tenga conocimiento del WSDL que describe el
servicio que vamos a usar:

```python
    from suds.client import Client

    client = Client(url='http://www.webservicex.com/globalweather.asmx?WSDL')
```

Listo, ya tenemos un cliente SOAP listo para consumir el servicio desde
Python.

## Utilizando el servicio SOAP via el cliente en Python
Lo que nos queda es revisar la documentación del servicio o, si no la
hay, el WSDL para ver cuáles objetos pueden ser pasados como mensajes,
construir el request e invocar el método remoto, para ello nos
interesan: Client.factory y Client.service.

Por ejemplo, obtengamos el tiempo para Caracas - Venezuela:

```python
    request = client.factory.create('tns:GetWeather')
    request.CityName = 'Caracas'
    request.CountryName = 'Venezuela'

    response = client.service.GetWeather(request)
```

## Un vistazo a suds, por dentro
Explorando la documentación o el WSDL veremos que
hay un objeto llamado *GetWeather* definido en el namespace *tns*, este
objeto tiene dos campos *string*: *CityName* y *CountryName*, también,
si vemos la definición de la respuesta en el WSDL, podremos observar que
es un texto plano (es decir, viene un objeto primitivo *string* como
SOAPResponse). Vamos a ver cómo maneja suds ambos casos:

En el caso del `request`:

```python
    type(request)
    instance
    print request
    (GetWeather){
       CityName = "Caracas"
       CountryName = "Venezuela"
    }
```

Ahora, el `response` se ve de la siguiente manera:
```python
    type(response)
    suds.sax.text.Text
    print response
    <?xml version="1.0" encoding="utf-16"?>
    <CurrentWeather>
        <Location>Caracas / Maiquetia Aerop. Intl. Simon Bolivar, Venezuela (SVMI) 10-36N 066-59W 48M</Location>
        <Time>Aug 18, 2013 - 09:00 PM EDT / 2013.08.19 0100 UTC</Time>
        <Wind> Calm:0</Wind>
        <Visibility> greater than 7 mile(s):0</Visibility>
        <SkyConditions> partly cloudy</SkyConditions>
        <Temperature> 82 F (28 C)</Temperature>
        <DewPoint> 80 F (27 C)</DewPoint>
        <RelativeHumidity> 94%</RelativeHumidity>
        <Pressure> 29.88 in. Hg (1012 hPa)</Pressure>
        <Status>Success</Status>
    </CurrentWeather>
```

Como vemos, suds nos crea un objeto Python a partir de la definición
que obtuvo del WSDL en el caso del *request* que se construye a partir
de la fábrica del cliente usando el objeto remoto *tns:GetWeather* como
plantilla.

En el caso del response, que está declarada como string, nos envía un
objeto suds.sax.text.Text, que puede ser tratado como un objeto string o
unicode Python normalmente.

Suds, no sólo nos hace más fácil la interacción con servicios SOAP, sino
que también nos abstrae del hecho de que tratamos con objetos remotos,
convirtiendo todo a objetos Python por nosotros.

## Autenticación en SOAP usando suds
En algunos casos es necesario autenticarse contra un servicio web para
poder utilizar sus métodos remotos, usualmente eso se hace a través de
un método público de autenticación que revisa los permisos y retorna un
token de acceso encapsulado en un objeto, este objeto debe colocarse en
el header de los requests que van dirigidos a los métodos privados.

Debido a que no conseguí ningún servicio web que me permitiera hacer un
ejemplo de esto, simplemente haré un ejemplo *dummy* de cómo sería en
código:


```python
    from suds.client import Client

    auth_client = Client('http://www.servicio.com/authservice.wsdl')
    request = auth_client.factory.create('ns:AuthObjectRequest')
    request.login = 'MiUsuarioParaElServicio'
    request.password = 'MiClaveSuperSegura'

    auth_object = auth_client.service.GetAccessToken(request)

    client = Client('https://www.servicio.com/otras_cosas.wsdl')
    client.set_options(soapheaders=auth_object)
```

Algunas veces, basta sólo con un objeto que contenga el usuario y el
password para el servicio (como el request de este ejemplo) en el
soapheaders del client y listo.

## Agregando datos adjuntos en SOAP utilizando suds, claro que se puede!
La única desventaja que vi al trabajar con suds es que no viene con
soporte nativo para attachments, sin embargo, es relativamente fácil
añadir esta funcionalidad en [este
gist](https://gist.github.com/iferminm/6265400){.reference .external}
podemos ver el código para hacerlo.

La manera de utilizarlo es la siguiente:


```
    from suds.client import Client
    from soap_attachments import with_soap_attachment

    client = Client(url='http://www.servicio.com/wsdl/servicio.wsdl')
    f = open('/home/user/music/panama.mp3', 'rb')
    data = f.read()
    mime_type = 'audio/mpeg'
    bin_param = (data, mime_type)
    request = client.factory.create('ns0:RequestConAttachment')
    request.usuario = 'iferminm'
    request.nombre_audio = f.name

    response = with_soap_attachment(client.subir_pista, bin_param, endpoint, request)
```

Básicamente lo que se hace es leer los bytes que conforman el archivo y
colocarlos en el cuerpo del mensaje SOAP (eso hace
with\_soap\_attachment), lo único que hay que saber acá es que el
endpoint (que se ve como parámetro en la llamada a
with\_soap\_attachment) es el punto de conexión al servicio web
especificado en el WSDL.

De esta manera, colocamos un archivo adjunto al mensaje SOAP para que
sea subido al servidor vía SOAP.

# Lecturas recomendadas:
Para más información recomiendo revisar la documentación de la librería
[acá](https://github.com/suds-community/suds){.reference .external}, 
sin embargo, para hacer clientes para servicios SOAP básicos, con este 
tutorial debería ser suficiente.
