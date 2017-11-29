Title: My take on microservices
Status: draft
Author: Israel Fermín Montilla
Date: 2017-10-15
Tags: python, django, scaling

There's been a lot of stuff going on there days on Software Engineering, it's hard to catch up on everything I would like to. I try to go one topic at
a time and now, also because we are working with this at the office, I'm hooked into microservices.

Microservices is a new word for an old concept, a concept I thought I will never see or play with in real life back in my University years, I remember
my Software Engineering professor talking about web services and APIs and huge systems at IBM, Sun Microsystems and Oracle, SOAP and REST interfaces
and how they interacted with each other and also the mighty Enterprise Service Bus with producers and consumers in Java, BPEL and C#, an very abstract
concept for me to grasp at that time and I thought the only place you could see that was working at huge, corporate companies like the ones I
mentioned above. 

Nowadays, any internet startup can grow at a huge scale and you can play around with this kind of technologies if you're lucky enough to be part of
one of those projects.

I'm lucky to be part of the dubizzle team, a classifieds website that operates at a massive scale here in the middle east, the architecture isa huge
legacy monolithic application with all of the core functionality and several services surrounding this legacy app, these services are, in my opinion,
mostly poorly integrated and fault tolerance is not the rule, sometimes error responses are silenced and bypassed which is quite bad. Also, the
integration goes over HTTP, which could be very unreliable even within the internal network and gives you a lot of headaches when you need to
integrate more and more services.

We've dedicated some time now to study best practices for implementing a microservices based architecture and built some proof of concepts and
deployed one of them to production here are some of my key learning and good practices taken from what I've read and personal experience actually
building stuff at dubizzle.

## APIs should be business bounded
It's a common mistake to build APIs as simple CRUD interfaces for domain entities. This means, all the business logic must be written and rewritten in
the clients, so, if you have, for instance, a web client, a desktop application, an android and an iPhone mobile apps, well, you can count yourself
how many times you'll have to write the business logic surrounding those models with a CRUD API.

You have to build your API to encapsulate business processes, not just the objects creation and manipulation
