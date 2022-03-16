Title: Why I am considering getting into management
Author: Israel Fermin Montilla
Date: 2022-03-16
Tags: career, personal
Cover: https://dl.dropboxusercontent.com/s/dz1lifonh07ecd9/header.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/dz1lifonh07ecd9/header.jpg


I've reached a point in my career in which I'm questioning a lot of things about
being a Software Engineer, don't misunderstand me, I love being a Software
Engineer and getting my hands dirty writing code, implementing things, designing
systems and discussing architectural trade-offs with other Engineers, the mix of
art and science in what we do is amazing, but I'm afraid growth paths as an
Individual Contributor (IC) are more complicated and less documented than the ones
for People Managers (PM).

As an C, it seems like your growth will depend on the
impression others have about your individual work, those others are usually
PMs, as a PM, your growth depends on the performance
of your team and the ability to achieve those quarterly goals.

Here are a few things I think are a bit odd when it comes to growing as an IC.

## Product > Engineering
It might seem strange because in some companies the organization in charge of
building and maintaining the user-facing systems it's called *Product Engineering*,
but quite often *Engineering* is a sidecar of *Product* which is supposed to
**only** support *Product*, with that in mind, all of the *Product*-related goals
are to be supported by *Engineering* efforts: building new features, enabling
experiments, investigating/fixing bugs and other types of issues, you name it.

Engineering is a feature factory for *Product* to a point that in some organizations,
Product Managers even estimate Engineering effort and commits time and deadlines
to Senior Management on behalf of Engineering teams.

This also translates on how everyone is rewarded, if you build new features, you
get recognized and attention, if you reduce the latency on an endpoint by 20%
by optimizing the database calls and indexing a few columns, you get a pat on the
back.

This also has a huge influence in the accumulation of technical debt, which is
one of the main elements of frustration for Software Engineers.

## IC goals are subjective
Quite often, your growth is linked to your day-to-day job plus a set of goals
set with your manager. These goals could be improve some system's reliability,
become better at some skill or learning some technology and implement a poof of
concept. But, how do you measure success on those goals? how do you measure a
skill? are you going to apply a test?, what if throughout the performance cycle
there's no project where a new technology can be used? what if throughout the 
performance cycle I don't get to work on the system I had to improve reliability
on? What if I got to work on it but the reliability was improved as a byproduct
of another project done by another engineer?.

Management goals are related to the team's performance, improving some business
metric, improving talent retention. All your team knows they have to perform well
because part of their growth depends on it, so, as long as you're gentle and have
a little common sense treating people fairly, half of the work is done for you.

## It's OK to be wasteful
When an Engineer is leading a construction, they calculate how much material is
going to be needed and how much debris will be left to be managed and disposed
and they purchase based on that. Any miscalculation is not good, they try to
optimize resources to the minimum, the same happens with everything else outside
software. Chefs optimize ingredients in their recipes and try to reuse as much 
as possible to reduce waste, tailors also optimize the use of the fabric.

Software Engineers on the other hand, well, we design and implement something
and never look back. It's consuming too much memory, let's throw some more RAM
into the servers and that's it. CPU is spiking, let's buy instances with more
computing power. Servers can't handle the load, throw more servers in. We just
throw resources at the problem without thinking whether our system design and
and implementation can be better, without revisiting for improvements. This is 
also aligned with the previous item, because Engineering takes the back seat while
product drives the car, Engineering pains are postponed until they're hurting
really bad, and even then the solutions are rushed!. "Will it take more than 
1 sprint?, we can't afford to delay features X, Y and Z"

The main reason I've heard is that "Engineering time is more expensive than
machine time", but then, machines won't solve scalability issues caused by lack
of design and rushed implementation, you're just paying interest on that loan
given in "machine time".

## Hiring ICs is broken
Yes, if you need/want to switch jobs, your options are limited to the companies
working with technologies you have experience with. It doesn't matter how quick
you can pick things up and learn new languages or technologies, if you have no
experience some companies won't even consider you.

Just an example, in my current role at Careem I've worked with Java, maintaining
services built with Springboot, Groovy, Bash, Terraform, CloudFormation, Python
and Jenkins, building a CICD platform, Nodejs, Typescript and Expressjs building
and maintaining services for another business vertical and PHP, Go, Elasticsearch
and Kafka, building a search platform for the Food and Shops business verticals.
Prior to Careem, I worked about 6 years in Python and Django, I had zero experience
with any of the technologies I've worked with at Careem, where the main language
is Java, if the interview process was focused only on Java and JVM tuning, they
wouldn't have hired me. All of the technologies I had to learn them on the job.
Asking other Engineers, reading documentation, reading a book, doing an online
course and getting my hands dirty doing toy projects to learn.

Then, there's the coding interview. Complex algorithms and data structures
questions I've only seen in programming competitions, infinite space search, 
optimal routes finding, graphs or 3D matrices traversing. Things I was once quite
good at because I was really into it, when I was in Uni, but now, it would take
me some time to dust off that knowledge. If I find one of those problems in my
day-to-day work, I know I'd be able to figure it out with some thought and research,
but in interviews you're often asked to solve 3 to 4 problems in a 90min time.

Systems design interviews are fine, you must be able to architect a system and
think of the components you'll need to built in order to have an optimal behavior.
But coding interviews feels like fighting Godzilla with a screwdriver while the
day-to-day work is actually playing UNO with Barney and his friends.

## Management skills are transferable
Engineering skills are not, well, they're partially transferable. Good engineering
practices, Architecture and Systems Design can be applied at any company you land at.
Unfortunately the skills with the specific technical stack can't be taken from
one place to another if the technologies are different. A lot of companies will
hire "Experienced Java Developers" and just cut the interview cold or just
don't take your profile into consideration if you don't have 5+ years of Java
programming experience.

Now, let's talk about the coding interview, the skills to pass a coding interview
are not maintained by your day-to-day job, you won't work with graphs or puzzle-like
problems every day, every time you're going for a technical interview you must spend
a few weeks preparing, some people solve 400+ problems in leetcode in order to
be prepared for the coding interview.

Management skills are practiced every day at work. Looking at metrics, dealing with
people, negotiating deadlines, planning a roadmap strategically, evaluating
trade-offs, mediating conflicts, even experimenting with team topology and different
methodologies. All these skills are valuable at the time of the interview and also
at the new company you land at.

## Conclusion
Well... switching to management is not a decision I've made already, it's just
something I'm considering, for all the reasons I listed above. I love getting my
hands dirty with technology, designing and implementing a system and watching it
work and serve millions of requests per minute. I enjoy working on refactors and
tuning systems for better behavior, but the manager path seems to be much more
straightforward than the IC path. The one thing I'm not so comfortable with is
having so much impact on other people's career and life in general and, in crisis
times, manager heads are the first to roll but, again, then landing in another
job doesn't require solving 400 leetcode questions and pray you get some similar
problems in the coding interview.

What do you think? have you ever thought the same?
