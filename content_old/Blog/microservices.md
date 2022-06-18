Title: My take on microservices
Author: Israel Fermín Montilla
Date: 2017-11-30
Tags: software engineering, microservices
Cover: https://dl.dropboxusercontent.com/s/atrbesdhbsz2jpx/microservices.png
Thumbnail: https://dl.dropboxusercontent.com/s/atrbesdhbsz2jpx/microservices.png

There's been a lot of stuff going on these days on *Software Engineering*, it's hard to catch up on everything 
I would like to. I try to go one topic at a time and now, also because we are working with this at the office,
I'm hooked into microservices.

Microservices is a new word for an old concept, a concept I thought I will never see or play with in real life 
back in my University years, I remember my *Software Engineering* and *Distributed Systems* professors talking
about web services and *API*s and huge systems at IBM,
Sun Microsystems and Oracle, SOAP and REST interfaces and how they interacted with each other and, also, the mighty
Enterprise Service Bus with producers and consumers in Java, BPEL and C#, a very abstract
concept for me to grasp at that time and I thought **the only place** you could see that was working at **huge**, corporate
companies like the ones I mentioned above.

Nowadays, **any** internet *startup* can grow at a **huge scale** and you can play around with this kind of technologies 
if you're lucky enough to be part of one of those projects.

I was lucky to be part of the *dubizzle* team, a classifieds website that operates at a **massive scale** here in the middle east,
the architecture is a huge legacy **monolithic application** with all of the core functionality and several services surrounding this legacy app.
These services are, in my opinion, mostly **poorly integrated** and fault tolerance **is not the rule**, sometimes error responses
are silenced and bypassed which is quite bad. Also, the integration goes over *HTTP*, which could be very unreliable
even within the internal network and gives you a lot of headaches when you need to
integrate more and more services. But the whole point of migrating to *microservices* is to solve all those issues and have a better
engineered platform to keep both product and tech as happy as possible and be able to move faster at the same time.

We dedicated some time now to study **best practices** for implementing a microservices based architecture and built some proof of concepts and
deployed one of them to production here are some of my key learning and good practices taken from what I've read and personal experience actually
building stuff at *dubizzle* and playing around with technology on my personal projects.

## APIs should be business bounded
It's a common mistake to build *API*s as simple *CRUD* interfaces for *domain entities*.
This means, all the *business logic* must be written and rewritten in the *clients*, so, if you have, for instance, a *web client*,
a *desktop application*, an *Android* and an *iPhone* mobile apps, well, you can count yourself
how many times you'll have to write the *business logic* surrounding those *data models* with a *CRUD API*.

You have to build your API to encapsulate business processes, not just the objects creation and manipulation, so a single *API* call,
triggers all the needed processes to fulfill the request or the query the client just gave to the server.

## Services must be independent units
This means, **you must think** of each *microservice* as a project or a *product* on its own, this means each *service* 
has its own *box* and its own *release pipeline* and its own *life cycle*, but also, they don't rely on each other to function.
This means, if your *invoicing service* is down, your *payment service*
**don't need to suffer** because of this, you can always accept payments from your users and send the invoices later,
when your *invoicing service* comes up again.

## Rely on data, not services
In the previous example you might be thinking "dude, but if the *invoicing service* is down when the *payment service* hits it, how will it know
it needs to send an invoice to a user?". Well, you need some way to let it know once it wakes up, some *data sharing* mechanism like a shared
database (which is in general a bad idea because it creates *coupling* between our services) or some sort of *caching* on the services that needs
to *consume* that data.

In our example, we could make the *payment service* and the *invoicing service* share the same database, or, have a good separation of
concerns and lower the *coupling* and, since *invoicing* needs to know about *payments* but, *payments* have no need to know about *invoicing*,
we can just have a *caching* mechanism in place in our *invoicing service* and have a copy of the needed data about *payments* in order
to generate *invoices*, of course, this will add some complexity to our system because we need to be fault tolerant and make sure the data
still reaches the *cache* if the *invoicing service* is down and we need to put some cache update processes in order to keep it up to date.

## High cohesion, low coupling
This is a principle borrowed from *Object Oriented Programming*, let's remember what they mean

### Coupling
> **coupling** is the degree of interdependence between software modules.
> > Wikipedia

This means, if two *modules*, *functions* or *services* rely too much on each other, chances are if I make a change on one, I'll have to make
a change on the other one to compensate, this makes our code and architecture less orthogonal, which means exactly that, a change in one
part of the system, will affect other unrelated parts, just like driving a helicopter.

### Cohesion
> **cohesion** refers to the degree to which the elements inside a module belong together.
> > Wikipedia

This means, it's a measure of how much the *elements* inside a *module* belong together, not necessarily they rely on each other, but they
all **work together** towards a common objective.

In general *cohesion* is increased if:

* All the *elements* in the *module* have much in common. This means, access the same set of data, for example.
* The *elements* in the *module* carry out a **small** number of **related** activities. This means, each member of the
module does one and only one thing related to the task without side effects  

By keeping **related functionality** together, we are automatically increasing *cohesion* and lowering *coupling*, and this is exactly
what we want.

### What does this mean in microservices?
Well, it's easy to think of *coupling* and *cohesion* withing the same computer program or the same code base, but in *microservices* this
means exactly the same, **keep related functionality together** so you don't have that logic spread all over the place and duplicated
in more than one service. This also mean, keep services using similar or related data together, either logically or physically.

## One hit, one transaction
This means, avoid distributed transaction at all costs, they are difficult to implement and even more difficult to debug if something
goes wrong, ideally one *write* operation to your system should directly affect **one** service, what happens *offline* could be a different
story. For example, we could have our *payments service* which deals with a third party payment gateway to charge our users' credit cards,
to keep things under *Single Responsibility Pattern* (SRP), we will have a separate *invoicing service* which handles generating and
sending invoices to the users (I know, we could separate things even more by having a separate *notification service* that handles
sending the emails but let's keep it at this level for the sake of simplicity). 

So, the only thing my client needs to know is *I need to make a payment*, whatever happens afterwards it's not my client's problem, it
only needs to hit the *payments service* with the needed *payload* and get the response to show it to the user. What happens under the hood
is my *payments service*'s problem, it needs to *somehow* notify the *invoicing service* that it needs to email an invoice to a specific
user, this has to happen *offline*, either we start a separate *thread* or use a message queue for it and we notify either generating an
*event* or via an *HTTP* call, but this needs to happen offline and be fault tolerant so we don't keep the *client* waiting for something
that is *our* internal process, as well as updating the inventory, generating accounting ledger entries, etc.

## Choreography over orchestration
This is, to me, one of the most important best practices I've learned then it comes to microservices oriented architecture, when we think of
distributed transactions we often have some sort of *director* or *conductor*, which is the service that initiated the transaction, it will
know, what needs to happen and in which order, also, it will be the responsible to roll everything back if any part of the transaction fails,
transactions need to be *Atomic*, right?. This is a very dangerous approach because, if something goes wrong while performing the transaction,
nothing can guarantee something won't happen while rolling it back, leaving the system in an inconsistent state and giving us lots of
headaches down the road when having to debug some weird behavior in our system.

The best way to implement these kind of *distributed* transactions, i.e., business processes that need to update more than one service
is through *Choreography*, if you think about a *choreography*, there's no *conductor*, everyone knows what they need to do, where they
need to go, the only signal is the music. This means, in *microservices*, we just need to *notify* everyone *something* happened, and
the concerning *services* will react accordingly, either updating their database, emitting another *event* or sending a notification to
the user.

In order to properly implement *choreography* we need to build *resilient* services by putting in place fault tolerance logic or processes
so, if some service fails to react, it can heal itself or someone gets notified.

## Don't rely on HTTP
[Peter Deutsch](https://en.wikipedia.org/wiki/L._Peter_Deutsch) and [James Gosling](https://en.wikipedia.org/wiki/James_Gosling) wrote about the
*8 fallacies of distributed computing* and the first one was

> The network is reliable

A million things can happen when you rely on the network, maybe the requests times out, maybe there's a broken link, maybe subnet permissions
were changed maybe the host we are trying to reach is unavailable, maybe a rat ate a network cable, lots of things can happen and we are
not in control of all of them, even withing our own private network.

What I'd recommend instead is to have a *communication layer* in the form of a *message bus*, it can be a *queue* like 
[RabbitMQ](https://www.rabbitmq.com/) or a *data streaming pipeline* like [Apache Kafka](https://kafka.apache.org/)
of course there will be a bit of network communication between your services and the communication
layer, or your services and the database system, but that's being taken care of by the corresponding drivers or libraries or deal with those,
so, you can assume they're fault tolerant and the data will reach its destination.

There will be cases where you can't avoid rely on *HTTP* or any network protocol, for example, you need to serve your website somehow, and
you need to query your services somehow too, so, in this case I'd recommend to go for a *REST API* or whatever protocol you prefer for external
communication (third party services and *client-server*) and using a *message bus* for inter-service communication.

### A note about the fallacies
Some people will say that the *8 fallacies of distributed computing* are obsolete nowadays because there are tools already that handle
everything for us, replication, secure networking, authentication, networks are sophisticated so, latency is not a problem anymore but,
just because *someone* is taking care of *something* for us, doesn't mean that *something* isn't there, imagine building a system without
these tools, you'll have to face them anyways, besides, there are countries where the computer networks are not as good as in the US or
Europe for example, so, I wouldn't say these *fallacies* are becoming irrelevant. Even if you're not implementing replication or security
yourself, you need to think about it and use *something* that handles that for you.

## Recommended readings
* [Building Microservices](http://amzn.to/2AkhBdU) by [Sam Newman](http://samnewman.io/)
* [RESTful API Design: Best Practices in API Design with REST](http://amzn.to/2Am0eZW) by [Matthias Biehl](https://twitter.com/mattbiehl)
* [The Pragmatic Programmer](http://amzn.to/2ngI1dI) by [David Thomas](https://en.wikipedia.org/wiki/Dave_Thomas_(programmer)) and 
[Andrew Hunt](https://en.wikipedia.org/wiki/Andy_Hunt_(author))
* [Coupling (computer programming)](https://en.wikipedia.org/wiki/Coupling_(computer_programming)) (Wikipedia article)
* [Cohesion (computer science)](https://en.wikipedia.org/wiki/Cohesion_(computer_science)) (Wikipedia article)
* [Fallacies of distributed computing](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing) (Wikipedia article)
* [The 8 fallacies of distributed computing are becoming irrelevant](https://www.infoworld.com/article/3114195/system-management/the-8-fallacies-of-distributed-computing-are-becoming-irrelevant.html) build your own opinion, are they?, comment!.
