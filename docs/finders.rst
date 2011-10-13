Finders
======================================

The finders module defines a new staticfiles storage and finder.


.. _AppMediaStorage:

AppMediaStorage/AppMediaDirectoriesFinder
--------------------------------------

.. versionadded:: 0.3

There are still a number of Django applications out in the wild which put their
static files (js/css/images) in a media folder rather than a static folder. This
finder extends the built-in `AppDirectoriesFinder <>`_ to gather files from the
media directories.

To use simply add to your `STATICFILES_FINDERS` setting.

.. code-block:: python

    STATICFILES_FINDERS = (
        ...
        'hilbert.finders.AppMediaDirectoriesFinder',
        ...
    )  
