Title: Working with FileFields on the fly in django
Author: Israel Fermín Montilla
Date: 2018-03-30
Tags: python, django, web development
Cover: https://dl.dropboxusercontent.com/s/y7hf2p40crdu19y/careem.jpeg
Thumbnail: https://dl.dropboxusercontent.com/s/y7hf2p40crdu19y/careem.jpeg


This took me a couple of hours to figure out. I needed to process a csv file
stored in a `FileField`, the catch was I had to do it on the fly, before saving
the model to the database. Not only that, I also had to generate another file
by applying certain rules to the content of the original file. Let's use the
following model as an example, hopefully this will save you some time when you
need to implement something similar:

```python
from django.db import models


class TwoFiles(models.Model):
    original = models.FileField(upload_to='files')
    treated = models.FileField(upload_to='files')

    def save(self, *args, **kwargs):
        self._generate_treated_file()
        return super().save(*args, **kwargs)

    def _generate_treated_file(self):
        pass
```

We will focus on the `_generate_trated_file()` method.

At this point, we haven't saved anything so there's no physical file to read
everything is in-memory and `models.FileField()` has the necessary methods to
read the contents, in this case we will read the whole file into memory for the
sake of simplicity, but it has methods to read line by line as well.

The code to read the file would look something like this:

```
import csv
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models


class TwoFiles(models.Model):
    original = models.FileField(upload_to='files')
    treated = models.FileField(upload_to='files')

    def save(self, *args, **kwargs):
        self._generate_treated_file()
        return super().save(*args, **kwargs)

    def _generate_treated_file(self):
        self.original.file.seek(0)
        content = self.original.file.read().decode('utf-8').strip()

        lines = content.split('\n')
        reader = csv.reader(lines)
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        for line in reader:
            new_line = apply_teatment(line)
            writer.writerow(new_line)

        self.treated = SimpleUploadedFile(
            name='treated_file.csv'
            content=buffer.getvalue().encode('utf-8')
        )
```

First, we rewind the file so that we are sure we start reading from the beginning,
then, the `.read()` call on the `file` reference will return a `io.StringIO()`
object, which we need to decode and then strip to remove all the additional spaces
or `\n`s.  

After we split the lines we need some place to write to, we won't have a physical
file because we haven't saved the model so we need to write in-memory, hence, we
create a `io.StringIO()` buffer to write all the treated lines.

We iterate the lines, apply the treatment and write to the buffer. When we are done,
we dump everything into a `SimpleUploadedFile()`, `utf-8`-encode it and assign it
to the `treated` `FileField()`.

Then, when the `save()` method finishes running, the model instance will be
saved to the DB and both files created in the filesystem.

This took me a couple of hours to figure out, hopefully I saved you some time,
thanks for reading and don't forget to [follow me on twitter](https://twitter.com/iferminm).
