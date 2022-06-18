Title: The evilness of None!
Date: 2017-03-13
Author: Israel Fermín Montilla
Tags: programming, python

Recently at work, i was solving one bug on one of our services, it was popping up in newrelic at least 9 times a week, this is one of the services we use in the monetization process at the office, so, it's a critical one, the least errors we 
see in newrelic for this service, the better.

The error looked a bit like a nonsense, basically some user's subscriptions were coming as `null` values or `None`, in Python.

Debugging the code and tracing the logs I found the like where it was failing and it looked something like this:

```python
subscription = user.get_oldest_subscription_for_addon(addon_id)
package = subscription.package  # This was the failing line
```

The method says it returns a `subscription` object, but it's returning `None`, why?

I digged deeper and opened the `models.py` file I searched for the method's name and bingo! I got it!

```python
    # ...
    def get_oldest_subscription_for_addon(self, addon_id):
        subscriptions = self.get_active_subscriptions().order_by('created')
        for subscription in subscriptions:
            if subscription.addon_credits_left.get(addon_id, 0):
                return subscription
        return None
```

And... that's where the `None` is coming from...

## What's wrong about this?

I'm sure we all have written similar pieces of code, search for something meeting certain conditions and, if we get nothing, `return null` or, `nil` or `None` or whatever you call it in your language of choice. And it's wrong in so many ways.

Truth is, [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare) , the creator of the Null instance while he was developing the type system for ALGOL, called it his *billion-dollar mistake*. I'm sure this bug affected our revenue in some way, maybe the impact wasn't that much because it was in some cases when a user was going to highlight his publication (feature an ad, in dubizzle lingo) and... yes, we were giving away free highlights because of this bug.

Returning `null` or `None` is usually a way to handle a case when we didn't find what we were looking for and it leads us to check for the result after calling the function which causes a bifurcation in the program flow, yes, it generates a different execution path which gives us one more place to introduce bugs or to check for errors. And we have to do this every time we call that function or method.

Now, imagine we call that function 500 times within the program, it will generate 1000 branches, 500 when we found what we were looking for and other 500 where we returned `None`.

Since i read *Clean Code* by Robert Martin, I try to keep in mind the key principles of what we call **clean code**. Everything from naming to design patterns, single responsibility principle, the newspaper principle, keeping things as short and simple as possible, doing one thing and one thing only on every entity of our program (classes, functions, variables, etc) and also the [Zen of Python](https://www.python.org/dev/peps/pep-0020/).

## How can we make it right?

One of the principles shown in *Clean Code* has to do with naming. All names should be intuitive, it should describe in few words what the `class` is, what the method does or what the attribute or variable holds. No matter how long the name is, with some limits and without exaggerating or being too verbose, which takes me to the second principle I'm going to talk about, *A function must perform one and only one action*, so, if a method should return a `subscription` object, it must always return a `subscription` object. If we stick to these two rules, the name of our functions should intuitive, because it will describe the action, and short enough because it will do only one thing.

This is also a good way to diagnose if I'm writing good code, whenever I'm naming a function and I'm being forced by rule number 1 to add an *and* or an *or* to the name of the function, I'm probably breaking rule number 2.

With some exceptions, for example, some functions could take a different course of action under certain conditions for a very good reason, for example, django's `get_object_or_404()` shortcut, and also manager methods `get_or_create()` and `update_or_create()` are keeping us from taking care of very common web  application and databases flows like returning 404 if we don't find an object, creating an object if it's not there yet and it has to be or performing an upsert operation.

This could lead to long names sometimes but nowadays we have auto-completion tools and flexible line length rules (even PEP8 is flexible about the 79 characters line length) so i don't think it's too much of a big deal.

## How can we avoid this?

There are several ways we could have avoided this, some of them cleaner than others, let's see.

1.- **Docstring:** nowadays we use integrated development environments (IDE) and all of them provide some meta information about the objects in our code by hovering over the name, there are also plugins for most of the editors out there... vim, Emacs, sublime, atom you name it. By writing a proper docstring for that method, it will be picked up and shown as a tooltip by one of these tools, no matter which editor we use, if we have one of those code completion plugins, it will show up. This isn't too intuitive, and doesn't provide the information right away, you have to read the docstring somehow and, if you don't have a good code completion tool, you will still need to open the `models.py` file and read what the code does. This option is probably the easiest one also the least clean one. 

2.- **Correct naming:** Function should had been called `get_oldest_subscription_for_addon_or_none()`, yes, name is too long, but at least the programmer using that function would be aware of the `return None` behavior  while using that function without having to open the file that defines it. The length of the function name is not an issue if we have an auto-completion tool, but the main issue remains, the fact that we are returning `None`, we shouldn't do that, still cleaner than option 1.

3.- **Raise an exception:**  the right way to handle this is to `raise` an unchecked exception and and handle it. The method should return a `subscription` object and it assumes it will find one and not being able to return one is an anomaly, so, we could raise an unchecked exception and handle it in the upper levels.

4.- **Null Object Pattern:** I don't know if it makes sense to implement such thing in Python, but there's a design pattern to take care of this kind of cases. Basically, you define an object that meets the same interface of the object you are expecting only that it's empty, this helps you continue with the same execution flow without any problem, you can read about it [here](https://en.wikipedia.org/wiki/Null_Object_pattern).

## What did I do?

I opted for option 2, although is not the cleanest one, because of the way the code was written it was the one that supposed less changes to the code. To be honest, the right refactor would be option 3.

I just renamed the function and changed all of the invocations and moved that `package = subscription.package` line below a check for the `subscription` to exist that was already there. Committed, pushed and released the bug-fix and that was it. After that, i got curious about who wrote that code, so, i went back on git's history and ran a git blame.

Surprise :) it was me :).

I'll refactor it the right way soon.