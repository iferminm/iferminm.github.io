Title: Django registration in no time!
Subtitle: Getting it done quick!
Author: Israel Fermín Montilla
Date: 2017-12-20
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

Is you ask me, I've always prefered to write a simple one, ask for an `email` and a `password` and ask for the
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
I'm using it for a couple of personal projects I'll be launching by the beggining of 2018 (or not... you know...) and it's
incredible how easy it makes it to implement user registration, allowing me to start working on actual features and functionality
in almost no time.

Let's get started

### Installation


