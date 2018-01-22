Title: Django registration in no time!
Subtitle: Getting it done quick!
Author: Israel Fermín Montilla
Date: 2018-01-24
Tags: python, django, tutorial
Cover: https://dl.dropboxusercontent.com/s/d97lkag2ysfdqrc/evolve.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/d97lkag2ysfdqrc/evolve.jpg


What does 99% of the projects we work on have in common?, what's usually the first or the last
thing we start working on when building something, a personal project perhaps?. If you said
*dealing with users*, that's right. On each and every project we find ourselves writing different
registration or authentication flows, sometimes we use third party authentication services like
*Google* or *facebook* via their *API*s, but most of the times I'd say we start by asking our user's
to register using their `email` and a `password`.

## Common approaches
There are several approaches to user registration, we can do it on a single step, or we can do it on
2 steps with a confirmation email being sent to the given address. There are several ways you can structure
your registration flow, either two simple questions (`email` and `password`) or multiple questions through
several pages, you name it, we always write user registration flows.

Is you ask me, I've always preferred to write a simple one, ask for an `email` and a `password` and ask for the
rest of the information I need on a separate *User Profile* page, things like name, date of birth, country, city,
mobile number or other stuff I might need. But you want as least friction as possible on the registration process,
specially if you're trying to get your first users, that's why I don't even send confirmation emails when I just launched
something. I start asking for confirmation when I already got some users and I have people constantly signing up, otherwise,
it's not worth the effort or the network traffic, plus the complexity of sending it asynchronously with a message queue.

That's why I thought of writing a reusable django app to solve this, I was working on it for a while, taking the good parts
of all the registration flows I've written, until I found `django-registration` and just switched to that library.

## Enter django-registration
This is way better that anything I could have written myself, it's being used by many people, has an active maintainer, works
out of the box and supports single and two steps registration flows so, why *reinventing the wheel* if it's already there?,
I'm using it for a couple of personal projects I'll be in the upcoming months (or not... you know...) and it's
incredible how easy it makes it to implement user registration, allowing me to start working on actual features and functionality
in almost no time.

Let's get started

### Installation
To install it, you just need to `pip` it as any usual *Python* module

```
pip install django-registration
```

For the simple *one step* registration flow or the *HMAC Based* workflow, you don't need to do anything else.

### Registration workflows
*django-registration*, supports three different workflows:

- **One step:** this workflow consists of as few steps as possible, the user signs up by filling the registration form,
after submitting, the account is created without any intermediate verification and the user is logged in automatically.
- **HMAC Based:** it's a two steps registration workflow that doesn't store any verification key, it sends instead a
timestamped HMAC verified value to the user via email in order to verify the account.
- **Model based:** to use this workflow, you'll have to add `registration` to your `INSTALLED_APPS` as you will need
to install one model to perform the verification step. If you need a two steps account creation because you require email
verification, the recommended way is to use the *HMAC* flow.

The basic *one step* registration flow is the easiest way to register new users, if you're just deploying something for fun
and it's intended mostly for your personal use but want to allow other people to use it, I don't think you need to verify
email and go through all that hassle unless you get serious about it, so in my case, the intended user for my project is just myself,
but if someone else wants to use it, I'm OK with that, I assume if you want to use something you'll just provide a legit email
because it's on your own interest.

### Settings everything up
I decided to go for a *one step* flow, as I don't really care if anyone provides an nonexistent email, I'm the one who will mostly
be using this, so, I guess it's OK, *django-registration* allows me to restrict new accounts from being created just by adding 
`REGISTRATION_OPEN = False` on my `settings.py` file.

Each registration flow comes with its own set of views and urls and you'll have to create your custom template and form if you needed,
you'll most probably end up customizing some behavior, but it's really easy to do, most of the core, boring and repetitive work
of creating the registration workflow is done for you and works out of the box.

In this case, for the *one step* all I had to do was the following:

1.- Include `registration.backends.simple.urls` in my urls configuration

```
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    # Some url patterns
    url(r'accounts/', include('registration.backends.simple.urls')),
    # More url patterns
]
```

2.- Set `REGISTRATION_OPEN = True`, this is the default value, but *better explicit than implicit*

3.- By default, after successful registration the user will be redirected to `/`, so I had to customize this behavior by
subclassing `registration.backends.simple.views.RegistrationView` and overriding the method `get_success_url()`

4.- By default, *django-registration* will use `registration.forms.RegistrationForm`, this can be overridden by supplying your
own `form_class` argument when instantiating the default `RegistationView` or by subclassing it and setting the `form_class`
attribute or implementing `get_form_class()`.

5.- Customize the registration template, this flow only needs one template called `registration/registration_form.html` and it will
pick it up automatically, the `RegistrationView` will add the `form` variable to the `context` and it will contain a `RegistrationForm` instance,
all for free.

## Recommended readings
* [*django registration* docs](https://django-registration.readthedocs.io/en/2.4.1/index.html)
* Django docs on [class based views](https://docs.djangoproject.com/en/2.0/topics/class-based-views/)
