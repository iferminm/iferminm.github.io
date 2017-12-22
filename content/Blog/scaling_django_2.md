Title: Making django scale Pt.2
Subtitle: Profiling
Author: Israel Fermín Montilla
Date: 2017-12-24
Tags: Python, django, scaling
Cover: https://dl.dropboxusercontent.com/s/nofhzatwj098ntz/measure.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/nofhzatwj098ntz/measure.jpg


It's been a while since the [first post](/making-django-scale-pt1.html) about scaling web applications using *django*, last time we
spoke about some basic concepts about scalability, buzz words we hear everyday and we also use but
always struggle when we need to give a formal definition to someone.

Once we have clear basic concepts about scalability, performance and we are familiar with the Pareto
Principle, we are ready to start optimizing and improving our system's performance, right?. Not so fast
cowboy!, if you remember the Pareto Principle most of the negative performance impact is coming for 20%
of the negative impacters. We need to manage somehow to solve that 20% so we are sure we are making a
significant improvement.

> *You can't manage what you don't measure* - Peter Ducker

This means, we need to gain visibility inside our system to be able to detect those bottlenecks and 
work on solving or easing them. For that, we will need a set of tools to monitor and profile our
application.


## The tools
There are a lot of monitoring tools for Linux and for *django* out there, you can use the ones you like
the most, but I'm going to showcase some here as a starting point. I'm not going to go deep into how to
install them and set them up or customize them because it's out of the scope of this post, but I might
post some individual howtos later, here I'll just point you to the corresponding documentation.


### django debug toolbar
This is my all time favorite, it's a pip-installable module for *django* and you'll need to add some
settings variables and a template tag and you're done.


![Image of django-debug-toolbar](https://dl.dropboxusercontent.com/s/bykbb9iryv1m6io/django_debug_toolbar.png)


As you can see on the screenshot it will give you a lot of relevant information about what happened under
the hood to serve that request, it will tell you the missed cache hits, which static files and templates
are being served, the current request headers and request parameters but my favorite feature is the SQL viewer,
it will show you the queries that ran on that view, with a timeline and their run time so you get to see
which ones are taking long time and take action, it gives you also the option to see an `EXPLAIN` of the query
to check what the query planner did.

To install it and use it, you can refer to the [official docs](https://django-debug-toolbar.readthedocs.io/en/stable/)


### vprof
This is a visual profiler for *Python*, although it isn't made for *django*, you can plug it in and take advantage
of all the cool graphs it will draw for you out of the box.

A profiler will measure how your code is behaving and tell you where the hot points are as well as your call
stack, vprof will give you an insight also on how much memory your program is consuming so it's easier to detect
memory leaks.

Here are some of the graphs *vprof* will produce for you

- Flame diagram to allow you see your function call stack
![*vprof* flame diagram](https://dl.dropboxusercontent.com/s/lvi3sxxhgmjccax/vprof_flame_diagram.png)
- Memory profiler
![*vprof* memory profiler](https://dl.dropboxusercontent.com/s/zv1o87ebms7humr/vprof_mem_profiler.png)


To set it up you can refer to the [official docs](https://github.com/nvdv/vprof)


### CProfile
Setting up *vprof* for *django* might be tricky depending of your application architecture and setup, *CProfile* is
pretty much the defacto standard on *Python* profilers, it will produce an output on an standard format you can plug into
any profiling reporting tool such as *SnakeViz* to produce cool graphs that will help you understand what's going on.

You can easily set it up in *django* by using *[django-cprofile-middleware](https://github.com/omarish/django-cprofile-middleware)* 
this app will also add one endpoint any
*staff* user can hit to get data about the performance and, also, *CProfile* can produce an output file you can
pipe into *[SnakeViz](http://jiffyclub.github.io/snakeviz/)*

This is how *SnakeViz* graphs would look like:

![*SnakeViz* list view](https://dl.dropboxusercontent.com/s/0uxf12rxx562t6z/snake_list_view.png)
![*SnakeViz* sunburst diagram](https://dl.dropboxusercontent.com/s/hx9cfdxvn1dqq4o/snake_sun_diagram.png)


### StatsD
This is an external stats collecting system built by *Etsy*, they [blogged](https://codeascraft.com/2011/02/15/measure-anything-measure-everything/)
about it and how it works and it's also [open source](https://github.com/etsy/statsd), you can set it up in *django* through a third
party app called [django-statsd](http://django-statsd.readthedocs.io/en/latest/).

Using this is a bit manual, you will need to send out your stats the same way you use log statements to add entries
with messages about what your system is going. In this case what StatsD will do is keep a log on counts and timing
of the events you are sending stats about.

The coolest thing about *StatsD* is that you can set it up to periodically flush data to [*Graphite*](http://graphiteapp.org/)
where you can then produce this kind of graphs on top of *StatsD*'s data

![*Graphite* dashboard](https://dl.dropboxusercontent.com/s/mns9m1htvqvxr5k/graphite.jpg)


### Use the logging subsystem
Logging can save you a lot of time if you do it right, it can also clutter your code with `logger.info()` statements everywhere
if you over do it, you need to log everything so you know what your app is doing at each step of the different processes it performs,
but log even more on the critical ones.

These log files need to go somewhere, maybe you're familiar with [syslog](https://syslog-ng.org/) to concentrate your logs in a single server so you
have only one place to go when you need to do some text-processing-fu with `sed`, `awk`, `sort` and `grep`, but as your system grows
and also the amount of different loggers storing messages, it will get trickier and trickier to keep track of every action across
all the different modules of your system, an *ELK* system can help you to ease the search through your log files and also generate
reports and graphs on top of your log data using *Kibana*.

You can read more about the *ELK* or *Elastic* stack [here](https://www.elastic.co/webinars/introduction-elk-stack)


### newrelic
If you have some budget to invest on this, [*newrelic*](http://newrelic.com) will give you most of these features
out of the box just by installing and setting up their *Python* tracker, it will start pushing data to *newrelic* and
you can see your system's performance in real time, it will show you data such as the average response time as well as
response time in percentiles, average throughput, average error rate, error data and even transaction data like the one
you get from *django-debug-toolbar*.

- *newrelic*'s main dashboard
![*newrelic* main dashboard](https://dl.dropboxusercontent.com/s/zs0m9ozgktnhl1n/newrelic_main.png)

- Transactions dashboard
![*newrelic* transactions dashboard](https://dl.dropboxusercontent.com/s/vuxlqnexow0srj8/newrelic_transactions.png)

- Errors dashboard
![*newrelic* errors dashboard](https://dl.dropboxusercontent.com/s/iw0zhoum8hv60xw/newrelic_errors.png)

If you have the budget, *newrelic* is a *no-brainer* it will be a valuable tool for you and your team and save you
a lot of time when you need to debug a live issue.


## Final words
Before you even think of optimizing anything, you need to measure, there is no point in blindly going through the
code and, for example, indexing fields in your models if you don't know the impact of that, if any at all. The tools
mentioned here are not a definitive guide to profiling *django* applications but they provide a nice starting point
to begging playing with them and choosing which ones work for you and which ones doesn't so you can improve your
tool belt, your stack and the quality of the products you're building.

Monitoring and measuring shouldn't be an optional thing, it should be there if not since day one, at least added within
the first months of life of your project, that's the only way you get to see inside your application, detect bottlenecks
and potential bugs, debug them, measure their impact, prioritize them and be sure that by rolling out the optimizations
you will have an improvement of ~X percent in your performance.

