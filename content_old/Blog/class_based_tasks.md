Title: Classy Tasks with Celery
Author: Israel Fermín Montilla
Date: 2017-03-23
Tags: python, programming, celery


This will be a short article, I just want to share something I learned this week.

If you work with *Python* and chances are you've ran into *celery* at least once, hopefully more than once, depending on how complex the projects
you've worked on are.

If you don't know it yet, *Celery* is a task scheduling library that lets you schedule heavy tasks to be ran later, for example, resizing an image, sending an email or posting data to a 3rd party service, those are things that can be done *later* so you don't have to keep your users waiting online for something to finish and could actually fail.

*Celery* lets you `delay` the execution of those tasks and put retry policies in place so you can re-run them after a given time under certain conditions, for example, a 3rd party service returned `500` or `502`, you might want to retry after, let's say, 20min to see if the issue is gone.

This won't be an in depth tutorial, you can check *Celery* [here](http://docs.celeryproject.org/en) if you don't know it yet.

Let's see this example in *Flask*

```python
@app.route('/')
def process_image(image_url):
    try:
        image = download_image(image_url)
        resized = resize_image(image)
        upload_image(resized)
    except Exception:
        return 'Failure, please try again'
    return 'Success'
```

This is a very basic example, full of bad practices and code like this shouldn't be pushed to production but it serves to illustrate what I need to explain.

Normally, what you might do is just call those three functions inside a task and just call the `task.delay()` from the request handler, something like:

```python
@app.route('/')
def process_image(image_url):
    tasks.process_image.delay(image_url)
    return 'Success'

# tasks.py
from celery.task import task

@task
def process_image(image_url):
    image = download_image(image_url)
    resized = resize_image(image)
    upload_image(resized)
```

But, those three functions are not supposed to be called synchronously, so, I don't want them laying in some module waiting for someone to call them outside a task. Reason being that, as said before, these are heavy processes that might keep my web server busy and prevent it from taking new requests for a while and also keep my users waiting on a *loading* screen for a long time, which isn't a good user experience.

I could delete them and copy all the code in my task function but it will lead to a potentially long function which will do a lot of things, it will be difficult to read and difficult to maintain, so... bad idea.

*Celery*'s `@task` decorator, actually works as an object factory of `Task` objects, and what it does is, it puts the decorated function in the `run()` method, so, I could take advantage of the object oriented paradigm to encapsulate all that logic inside a task avoiding the risk of having those functions called synchronously.

It would look something like this

```python
from celery import Task


class ProcessImage(Task):
    ignore_result = True

    def run(self, image_url):
        image = self.download_image(image_url)
        resized = self.resize_image(image)
        self.upload_image(resized)

    def download_image(image_url):
        # Code to download the image from a given url

    def resize_image(image):
        # Code to resize the image

    def upload_image(image):
        # Code to upload an image to a certain location


# We need an instance we can call delay() on
process_image = ProcessImage()
```

And done, we can implement also a notification logic to inform the user if there's any issue processing the image after retrying and that kind of
things, but I'll leave that for another post.

By doing a *class based task* for complex background jobs, we can produce cleaner code which is easier to maintain and to read and keep those heavy tasks encapsulated so no one calls them directly from a controller or a django view.

I know this is not the best way to implement this use case, we could have done it with a `TaskTree` or with callbacks, but I wanted to show how to use classes to define tasks. I'll explain those approaches in future posts. :-)
