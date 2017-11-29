Title: Making django scale Pt.1
Subtitle: Getting the basic concepts
Author: Israel Fermín Montilla
Date: 2017-09-24
Tags: python, django, scaling


I gave a talk on PyConPL this year about scaling django, obviously on a 35min talk you don't have enough
time to outline all the strategies and go deeper, so I thought it might be a cool idea to write a series
of blog posts  about this topic, not only to help someone who needs to optimize his django app, but also
to help myself have it for future reference.

There are a lot of django apps out there, in most cases the default setup and basic deployment strategy
would be fine, and your application will perform OK, but in some cases you will need to make it scale
to serve thousands or millions of requests per day. There's no recipe for optimization or scalability,
but there are a lot of technology or stack agnostic strategies you can use to make your systems scale
well, here I'll show how to implement them with django.

## Basic concepts
First things first, we need to have clear and solid concepts in mind, we use these words on a daily basis
if we're Software Engineers but when we need to say what they mean we sometimes struggle, so, I'll write
them down here for future reference.

### Scalability
> Scalability is the capability of a system or process to handle a growing amount of work or its potential
> to be enlarged to accommodate it
> - Wikipedia

What this means is the amount of work processed by a system must grow in proportion to how much it is enlarged,
for example, if I have a cashier at a bank, and that cashier is able to serve 10 people per minute, if I add one
more cashier to my system, it should be able to serve rightly 20 people per minute depending on the training of
the other cashier and some other conditions. Luckily, servers are more homogenize than people's abilities, 
for servers or applications, if I have a service that handles 1000 requests per minute, if I add another 
instance of the same service I should be able to handle 2000 requests per minute.

### Performance
> *Computer performance* is the amount of work accomplished by a computer system.
> - Wikipedia

You usually want to measure performance by some metric, for example:

* *Response time:* which you want to minimize
* *Throughput:* throughput is the rate of processing work, this one you want to maximize
* *Resource utilization:* which you want to minimize, you want to accomplish more with less
* *Availability:* you want to maximize your uptime

The performance metrics are relative to the type of system you're building, for web applications
you usually go for low response time and high throughput.

### Pareto principle
This isn't actually a concept, but it is incredible how things always turn out like this. The Pareto
principle states what follows:

> For many events, roughly 80% of the effects come from 20% of the causes

For example, 80% of the work will be done in 20% of the time, the other 80% will be spent on small issues
or small tangential work not directly related to the main objective. 80% of the bugs is caused by 20% of the
code and, in this case, 80% of the performance impact is caused by 20% of the issues.

This is interesting because it makes you see that not all issues affect your system's performance the same way,
there are some issues that are more serious and not necessarily the same issue on a different project will impact
it the same way. Find that 20% and gain an 80% on performance, sounds easy, right?, but it isn't.

### Takeaways
As a Software Engineer, sometimes I become so obsessed about performance I sometimes write things *already optimized*,
this is a big fallacy and a huge mistake, premature optimization is bad because you don't know if what you're doing
is actually going to have a significative impact on your system's performance, blind optimization is worse, because
you might have some ways to get data or an insight on how your program is running but you're just too naive or lazy
to go get it.

In the following posts, I'll recommend some tools to measure and later on some strategies to make your django site scale,
so, what you'll see in part 2 will be a set of tools to monitor your app's health.

Don't forget to subscribe! I rarely send emails but when I do, It's interesting, I promise.
