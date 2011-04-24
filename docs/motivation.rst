Motivation
======================================

Why not just put these on `djangosnippets <http://djangonsnippets.org/>`_? Well some
of these can be found there or inspired work in this project and I've tried to note those cases.
My primary problem with djangosnippets is:

1. Lack of tests
2. Lack of portablity
3. Lack of maintenance

Some might feel that the snippets are small enough that they don't need tests. Those
people are wrong. Am I really supposed to stick code in my project that someone else
wrote and isn't tested?

None of the snippets are pip installable. That is not the purpose of the site. However,
that means the most useful snippets are repeated in a number projects and there is no way
to push improvements upstream. Combined with the lack of tests this can make for a
maintenance nightmare.

Snippets can indicate the Django version they were written against but they typically
aren't maintained as Django deprecates functions, improves common idioms, and even
elimates the need for the original snippet.

While any one of these problems could be ignored, together they have caused many to
create similar snippet collections to alleviate some of these problems. I think that
djangosnippets has some great content but that doesn't mean that it stops
people from writing it over and over again. This project is not meant to be a
replacement for djangosnippets but more a supplement to maintain my personal
sanity.


Related Projects
-----------------------------------

There are some similar projects. If interested you should check out:

1. `django-annoying <https://bitbucket.org/offline/django-annoying>`_
2. `djblets <https://github.com/djblets/djblets>`_
3. `django-utils <https://github.com/ojii/django-utils>`_

I appologize in advance if you felt I've left out a project.

