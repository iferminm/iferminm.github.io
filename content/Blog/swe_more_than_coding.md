Title: Software Engineering
Subtitle: More than writing code
Author: Israel Fermín Montilla
Date: 2020-05-01
Tags: career, software engineering
Cover: https://dl.dropboxusercontent.com/s/e5f7as0ghmihdxn/header.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/e5f7as0ghmihdxn/header.jpg


At work, my Engineering Manager asked me to start sharing my knowledge
with the rest of the team more often. Of course, we do code reviews and
we have some other ways to get the knowledge spread across the team, we have
a wiki on confluence, we have tech meetings where we talk about how we will
solve the problems at hand, those are good opportunities for very specific
knowledge sharing, which would be in the form of advice or guidance on the
approach to follow to implement something, but it would be nice to have
some other kind of sessions to keep the team motivated, active and seeing
each other while the lockdown lasts.

I thought of several topics I could talk about, all technical ones:
DevOps, Distributed Systems, Functional Programming, very exciting ones
but then I realized, the team is very very good technically, everyone is
a very capable *programmer*, and then I stopped. See, I said *programmer*,
is that what we are?, nope, definitely not. The job title says **Software
Engineer**, is that all we do? write code?, I don't think so. I started writing
my thoughts and put them together in the form of a talk I'll summarize in this blog
post. Thinking about it, most of us don't realize the complexity around
**Software Engineering** and we minimize our work to *yeah, I write code and
stuff* or *I maintain and implement new features* but everything is much more
complex than that.

# Programmer vs Developer vs Engineer
Don't misunderstand me, there are plenty of roles our there and we call ourselves
in many ways: *Software Engineer*, *Software Developer*, *Programmer*, *Computer
Programmer* but words have an impact and everything has a meaning, I believe
we should name things correctly. I'm not asking everyone to think or name things the same
as I do, but I do think we should separate things and roles in a better way and with
different expectations.

## Programmer
A programmer is someone who writes code, that's it, a programmer wouldn't care
too much about Software Architecture or Design, neither about the whole lifestyle.
A programmer gets the full spec of what they need to implement, they write the code
and they deliver it, not much thoughts about how it's going to be deployed, where it's
going to run or how it's going to be used.

## Developer
A software developer will care about the software, a bit of design and architecture
but that's it, not much interest in where it's going to be deployed, how it's going to
run or how it's going to be used.

I'm not saying all programmer or developers are like that, I'm just saying these should be
the concerns of those roles. If you consider yourself a Programmer or a Developer and you go
beyond that, great!, now, the whole point of this article is to share my views and definition
about the **Software Engineer** role.

# Software Engineer
A Software Engineer, just like a Programmer and Developer, they care about Software,
they also write code and make sure it works as expected but also worry about design,
architecture and implementing best practices on every aspect about software

* **Building:** as a Software Engineer, we worry about building good software, not only
about the software itself, we worry about the building blocks, choosing (or building) the 
correct ones, implementing the right levels of abstraction so that maintainability is
easier.

* **Operating:** as a Software Engineer, we know we don't have to always build something
new, we can just run existing software and operate it, monitor, manage and make sure
it runs smoothly so that every user can accomplish their goals with it. Also, we know that
the software we build needs to be operated by someone (sometimes ourselves) so we need to build
ways to interface and interact with it from an admin perspective.

* **Documentation:** this is a usually forgotten one, we read ridiculous amounts of manuals and
other types of documentation and interpret them in order to use third party software, but we also
need to write docs in order for other to use our software or understand and contribute to our code.

## We know about software
And we need to know a lot about it, not only to write it, but also to use it effectively, when building
it:

* **We know it has to be well done:** so we worry about architecture, design and making the right decisions
from the ground up: choosing the right stack, building the right abstractions and applying the best
practices we know.

* **We know it has to be operable:** so we worry about things like CICD, monitoring, logging. Building it
in a way so that it is easy to debug and find issues while running on production as well as building ways
to interact with it to gather information, metrics or reports via command line if needed.

* **We know it has to work:** so we worry about testing and verification so that the behavior of the systems
we build is predictable, injective and idempotent. For a set of inputs, the output is something we expect.


## We know around software
We not only know how to build software, we also know many things around it.

* **We know it has to run somewhere:** so we know about infrastructure and operating systems, but we're not
sysadmins.

* **We know it talks to other software:** so we know about network and communication protocols as well as
distributed systems, but we're not network engineers.

* **We know it has to store data somewhere:** so we know about databases and data modeling, we have to do it
efficiently and we have to know how to tune performance if needed, but we're not sysadmins.

* **We know it has to function in a certain way:** so we worry about testing at several levels and of different kind:
performance, unit testing, integration, UX and UI testing, API tests. But we're not QA engineers


## We are part of a team
All I mentioned before is very difficult and complex and, to add to that, we need to work with other humans,
we are part of a team which usually has people from diverse backgrounds and specialties, a (sometimes non technical)
Product or Project Manager, an Engineering Manager, some front end engineers, QA specialists and so on, we need to
communicate in different ways and keep everyone aligned on the same page.

* **Meetings:** we need to attend meetings in order to brief about the technicalities if the work being done
and unblock if someone needs help with something we know.

* **Documentation:** this comes in many forms, technical specs, API documentation, all of this is, at the end of the day,
communication that needs to flow constantly, just that we choose to store it in the form of text to that we don't have
to repeat ourselves every time when someone needs to use the API or go through how something was implemented and the thought
process behind it.

* **Code Review:** this is a good one, this is when we get to mentor people and help them get their work into a better shape,
also when we get help to improve ours and learn from others, this is also another form of communication.


### Communication is everything
If you're not taking anything from this post, the only thing I'd like you to think about is that, yes, hard skills are very important
for the Software Engineering role, we need to think about how we write code that performs better, but none of that is useful if we are unable
to work with others. To work with others, communication is everything.

* Don't assume the people you're talking to knows or has the same context you have, always start by sharing the contextual information
needed to understand the problem at hand or the solution you'll present

* Know your audience, it's not like you're performing a stand-up comedy routine but, when you're communicating, you do have an audience,
setting the tone and language is important, it's not the same talking (or writing for) API users than writing (or talking) to someone
whose code you're reviewing.

* Always ask, you never know if the others are assuming some context, the only way to find out is asking. When something is not clear
or you find yourself assuming something, that's when you need to ask. You can ask a question because you don't know something or a
clarifying question, which might seem redundant, just to make sure everyone is on the same page and getting the same understanding.

Once you realize you don't know it all and you don't have to know everything, you also realize the rest of the people
also don't know everything, and they also don't have to know it all, everyone comes from different backgrounds and knows some things
they've been exposed to or studied and ignore some others. Only by talking to each other, communicating and sharing knowledge we all
become stronger engineers.


