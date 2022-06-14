Title: Processing CSV files in Go
Author: Israel Fermín Montilla
Date: 2018-03-30
Tags: programming, go, csv
Cover: https://dl.dropboxusercontent.com/s/y7hf2p40crdu19y/careem.jpeg
Thumbnail: https://dl.dropboxusercontent.com/s/y7hf2p40crdu19y/careem.jpeg


Lately, I've been interested in learning Go, the main reason is we're starting
to use it more and more at Careem, so, in line with my philosophy of learning,
I should master it, even if I don't like it, at least to a point where I can
be useful and write it without having to google *how to write a for loop in Go*.

I'm working on a personal project in which I have to generate and process a lot
of CSV files, so, I thought I could write part of it using Go. Using a language
I'm not super familiar with would make me slow in terms of progress in my project,
but since it's not super critical to finish on time I'm ok with that. Most of the
other parts of it are written in Python, using, of course Django and Django Rest
Framework, so, not all the project will progress as slow.

## Types...
The first thing I thought I was going to struggle when programming with Go was
its type system. Different types of `integer` and `float` and having to declare
basically every variable and give it a type is something I'm not used to anymore
after so long working with dynamically typed languages like Python and PHP.

So, the first thing I had to do was to declare a `struct` `type` for holding
the data I need from the CSV I'm going to parse.

The program generating these CSVs already makes sure the structure is as expected,
no pre-validation is required in this case because I have full control on how
the CSV is generated. I'll use a very basic example.

```
package csv


type Person struct {
    FirstName string `csv:"first_name"`
    LastName string `csv:"last_name"`
}

```
