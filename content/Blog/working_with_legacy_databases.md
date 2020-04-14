Title: Working with databases easier
Author: Israel Fermín Montilla
Date: 2020-04-01
Tags: python, databases, sqlalchemy, orm
Cover: https://dl.dropboxusercontent.com/s/e5f7as0ghmihdxn/header.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/e5f7as0ghmihdxn/header.jpg

This will be a short article, recently at work I had to build few reports on
top of two legacy databases, to be honest, the whole architecture and the way
the data is stored, in my opinion, is not optimal, a lot of things need to change
but, as usual, features and business take precedence over tech debt.

The whole stack is based on nodejs on top of typescript, which makes a bit more
enjoyable the fact that I'm now working in JavaScript. All the databases were
generated using knexjs so, these databases were there already and I only had to
connect to them.

I didn't want to spend too much time on the connection and mapping part, so
I wanted to see if an ORM would be of use here

## The overall idea
Since we will be integrating with other internal tools to generate these reports
the implementation I came up with is temporary, so I wanted to make as few changes
as possible in the current codebase for several reasons:

1. Once you add something temporary, it will be difficult to clean it up
after it's not needed anymore, the chances of someone building on top of it 
is high.

2. I don't like working with typescript, or JavaScript in general so if I could
get away with writing in some other language it could be more fun

3. The current application is a monolith and the logic is complex,
adding more would take longer than implementing something from scratch

So, I decided to implement the report generating logic in a Lambda function
which will be executed periodically, this meant I had to setup the connections
to the databases from scratch and map to my domain classes and types in order
to have a clean architecture.

## Enter Sqlalchemy
Sqlalchemy is the database Swiss army knife in python, it makes it very
easy to work with databases by mapping tables to domain classes, but it also
works the other way around by introspecting the database's schema metadata and
generating stub classes to deal with them in Python.

### Automap
Sqlalchemy has an Automap extension, which lets you connect to an existing database
and generate a domain model from the existing database schema and operate with it
from Python, trigger queries and use Sqlalchemy normally as if the schema was generated
by you.

It's very easy and it doesn't take 30 lines of code

```python
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


DATABASE_URL = os.getenv('DB_URL')

Base = automap_base()
engine = create_engine(DATABASE_URL)
session = Session(bind=engine)

Base.prepare(engine, reflect=True)
```

Then you can access the classes with the table name as it is in the database let's say you have a
`user_profile` database, then you can access it as

```python
Base.classes.user_profile
```

Trigger queries as

```python
UserProfile = Base.classes.user_profile

profile = session.query(UserProfile).filter(UserProfile.user_id == 123123).fist()
```

And you're good to go.

Of course, code conventions in SQL and Python are different, if you want your code to look more pythonic
and have `Base.classes.*` to be in PascalCase as well, you can write a function to override the table naming
when the automap is performed, it will add few lines but still below 20 lines in general

It looks something like this

```python
def snake_to_pascal(base, tablename, table):
    return ''.join([w.capitalize() for w in tablename.split('_')])
```

Of course, that assumes your tables are named as `this_is_a_table` and will be converted to `ThisIsATable`

You can use that function when you call `Base.prepare` as follows

```python
Base.prepare(engine, reflect=True, classname_for_table=snake_to_pascal)
```

And that's it. :-)
