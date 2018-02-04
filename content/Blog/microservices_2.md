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
and, **always** remember, *if something can fail, it will fail*.

### Increases overall response time
Take a look at the following figure: 


Response times are not taking into account the wait time while the downstream services
respond. This means, *service 1* queries *service 2*, it does *something* and takes 10ms to respond. Also, *Service 1* queries
*Service 3* which queries *Service 4* and *Service 5*. *Service 4* does *something* and takes 300ms to respond and *Service 5*
queries *Service 6* which takes 1000ms to respond, then *Service 5* does *something* and takes another 1200ms to come back to
*Service 3*, which has been waiting 2200ms to get all the data it needs to do *some stuff* which takes 300ms. By this time,
*Service 1* has been waiting 2500ms for all the data it needs to do a 120ms *something* and return back to the upstream caller,
which could be another service waiting or the end user. 

Note that the above flow paralelizes all the needed downstream calls per service, so in this case, the total response time will be
constrained by the slowest call chain. If you were using a stack where doing multiprocessing or async programming is not an easy
option, you'll have to add up the response time for all of the downstram calls because in reallity the service in question
is being blocked while waiting for the network call to finish and, only then, making the second call and blocking until it comes back
and so on.

There are several ways you can keep the same setup, you can add several levels of cache in between services, you can add a timeout
to the network calls but everything comes at a cost. If you're keeping a synchronous approach to answer certain questions it's because
you need your data as fresh as possible, so, the more cache you add the more stale your data could be. You could also add a timeout to
your calls but, if one of them times out, you'll fail in responding to the upstream caller and it will look like the system is down.


### What if someone is down?
Let imagine *Service 6* is down because we had a buggy release.


This means, *Service 1* will have to wait 1500ms before returning an error upstream, you can mitigate this
with a [short circuit]() approach or returning a cached response for the query you're trying to answer but,
again, unless you really need this to be synchronous, you'd be adding more complexity to an already complex
system.

Also, what if it isn't a *read* operation, what if we're actually *writing* downstream and the last write fails
because of *reasons*. You'll be half way a transaction and you'll have to deal with it somehow, wither queuing that
last write and hoping *Service 6* comes back soon or rolling back the whole transaction which would mean deleting from
the other services and returning an error, there are ways to solve this, but usually it doesn't need to be this hard.

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
