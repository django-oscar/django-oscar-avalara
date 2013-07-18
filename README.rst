====================================
Avalara integration for django-oscar
====================================

This package provides integration between Avalara_ and Oscar_.

.. _Avalara: http://avalara.com
.. _Oscar: http://oscarcommerce.com

Useful documentation:

* `Avalara docs <http://developer.avalara.com/api-docs/>`_

Contributing
============

Clone the repo, create a virtualenv and run::

    make install

to install all dependencies.  Run the tests with::

    ./runtests.py

There is a sandbox site that you can browse and use to test the Avalara
integration.  Create is using::

    make sandbox

and browse it after::

    cd sandbox
    ./manage.py runserver
