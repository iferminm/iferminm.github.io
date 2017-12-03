Title: My take on microservices
Subtitle: Avoiding the network
Author: Israel Fermín Montilla
Date: 2017-11-30
Tags: software engineering, microservices
Cover: https://dl.dropboxusercontent.com/s/atrbesdhbsz2jpx/microservices.png
Thumbnail: https://dl.dropboxusercontent.com/s/atrbesdhbsz2jpx/microservices.png


On a previous article on *microservices* **external link**, we went through the best practices I've seen,
which doesn't mean those are the only ones, it only means that those are the ones I've seen work for me
and the ones I've tried.

This time, I would like to focus on **Choreography over Orchestration** and **Rely on data, not services** because
I feed I didn't develop enough on these ones and those are really importand for my approach on *microservices*, if
you paid attention to the subtitle, these are also the two *principles* that will help you *avoid the network*, well,
not 100% true because you still need to communicate with your clients and that involves network calls but, at least,
it will help you take them to a minimum on internal communication or *message passing*.

But first:

## Internal *REST* services, why not?
Don't get me wrong, I love *REST*, I like building *API*s and I enjoy using a well designed one for sure, but for internal
communication I prefer to avoid it unless the communication **needs** to be synchronous, there are some cases where you can't
help it and it's not always because of a bad design, sometimes the use case itself enforces that restriction.

If you find yourself using network calls most of the time, something will most likely go wrong. Network is not 100% reliable
and, **always** remembet, *if something can fail, it will fail*.

### Increases overall response time
**chained network calls**

### What if someone is down?
**not able to always give an answer**

### Sometimes you will violate *SRP*
**Innecesary deployments of services when they need to hit another one**

### When should I go synchronous?
**cases when I need the latest available information**
* Credit counts
* Warehouse availability


## Choreography over Orchestration
**Director vs Music**

### An example
**step by step an event triggering other stuff**


## Rely on data, not services
We spoke about *low coupling and high cohession* in *microservices* in a previous article, relying on
a service to be up so 


### Eventual consistency
