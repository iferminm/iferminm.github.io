Title: We always evolve
Subtitle: Don't look back unless it is to fix important stuff
Author: Israel Fermín Montilla
Date: 2017-12-14
Tags: software engineering, career, personal
Cover: https://dl.dropboxusercontent.com/s/d97lkag2ysfdqrc/evolve.jpg
Thumbnail: https://dl.dropboxusercontent.com/s/d97lkag2ysfdqrc/evolve.jpg


I've been going through code I wrote about two or maybe three years ago while cleaning up my working directory
and archiving old stuff and, I must say: what the hell did I have in my head by that time?, for real, there are
things that are over-engineered, very complicated solutions to simple problems, sub-optimal or inefficient code,
a lot of spaghetti code, highly coupled modules (or django apps), all of this to say the least.

I know, maybe, in a couple of months (or years) I'll go through the code I wrote today, or yesterday and say the
same thing *oh my god! was I stupid or what?*, but I believe this is part of every craftsmanship job like software
engineering, graphic design, cooking and even music. You come out of school with the knowledge, but only experience
doing what you're trained to do will give you elegant practices and make you a good professional.

The best way to evolve is to **never stop learning**, read a lot of technical stuff, also master your **soft skills**,
I wrote it bold because they're as important as your technical ones, try out new ways of doing things, programming
paradigms, new programming languages, new tools to add to your stack and adopt better practices or ease some
pains in your development, testing or deploy process, perhaps your company's or your employer's processes. Only by
learning and gaining knowledge and then putting it in practice you will gain experience and know what works, what doesn't
work and what work betters under some conditions.

> Knowledge is of no value unless you put it into practice.
> — Anton Chekhov

You might be asking what made me reflect on this, well, some time ago I wrote about [*The evilness of None*](the-evilness-of-none.html) and
how it is a bad practice to `return None` or `return null` from functions when you're expecting the output to meet
certain requirements (internal link). Since I wrote that, I've been going through old projects checking how common
this pattern was on my code and, unsurprisingly, I found some other bad practices.

So, if checking old code and surprising myself with *how stupid I was* is something that happens often, it is a good
thing, it means I've learned something I didn't know by the time I wrote that code. So, always move forward but,
from time to time, check backwards not to adopt bad old habits, but to see how much you've learned and also if there's
anything you need to fix on a project you're maintaining.
