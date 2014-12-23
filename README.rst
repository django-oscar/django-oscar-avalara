====================================
Avalara integration for django-oscar
====================================

This package provides integration between Avalara_ and Oscar_.  Avalara is a
service that provides accurate sales tax calculations in the US.

.. _Avalara: http://avalara.com
.. _Oscar: http://oscarcommerce.com

Useful documentation:

* `Avalara docs <http://developer.avalara.com/api-docs/>`_

Status:

.. image:: https://secure.travis-ci.org/tangentlabs/django-oscar-avalara.png?branch=master
    :target: http://travis-ci.org/#!/tangentlabs/django-oscar-avalara

Installation
============

Install from PyPI::

    $ pip install django-oscar-avalara

or Github::

    $ pip install git+https://github.com/tangentlabs/django-oscar-avalara.git

then add ``'avalara'`` to ``INSTALLED_APPS``.

Specify the following settings:

* ``AVALARA_ACCOUNT_NUMBER``
* ``AVALARA_LICENSE_KEY`` 
* ``AVALARA_COMPANY_CODE`` 

You should have been provided with these details when you signed up with Avalara.

When not in production, set ``AVALARA_TEST_MODE = True`` to make requests
to the Avalara development server.

This package uses a named logger ``'avalara'`` so it is normally useful to
define handlers to this logger.

Usage
=====

To integrate Avalara into checkout, you need to override two methods from the
checkout view class ``PaymentDetailsView``.

First override ``build_submission`` to apply taxes to the basket and shipping
method:

.. code:: python

    from oscar.apps.checkout import views
    from django.contrib import messages
    from django.template import loader

    import avalara

    class PaymentDetailsView(views.PaymentDetailsView):

        ...

        def build_submission(self, **kwargs):
            submission = super(PaymentDetailsView, self).build_submission(**kwargs)

            # Fetch and apply taxes to submission dict
            try:
                avalara.apply_taxes_to_submission(submission)
            except avalara.InvalidAddress, e:
                msg = loader.render_to_string(
                    'avalara/messages/invalid_address.html',
                    {'error': e.message})
                messages.error(self.request, msg, extra_tags="safe noicon")

            return submission

Here we are passing the submission dict to ``apply_taxes_to_submission`` which
will look up the appropriate taxes and apply them in place to the basket and
shipping method instances.

We also watch out for ``InvalidAddress`` exceptions which will be raised if
Avalara is unable to find a tax jurisdiction for the passed shipping address.

Finally, override ``handle_successful_order`` to submit the placed order to
Avalara:

.. code:: python

    from oscar.apps.checkout import views
    from django.contrib import messages
    from django.template import loader

    import avalara

    class PaymentDetailsView(views.PaymentDetailsView):

        ...

        def handle_successful_order(self, order):
            response = super(PaymentDetailsView, self).handle_successful_order(
                order)

            # Submit tax information to Avalara
            try:
                avalara.submit(order)
            except Exception:
                # Tax can be re-submitted later so we swallow all possible
                # exceptions and log them.
                logger.error("Unable to submit tax information for order %s",
                             order.number, exc_info=True)

            return response

Here we pass the order instance to ``submit`` which will submit the tax
information to Avalara for reporting.  We also catch and log any exception as
we don't want order placement to show an error screen.  If there is a problem
talking to Avalara, we can manually resubmit the order later on.

Contributing
============

Clone the repo, create a virtualenv and run::

    make install

to install all dependencies.  Run the tests with::

    ./runtests.py

There is a sandbox site that you can browse and use to test the Avalara
integration.  Create it using::

    make sandbox

and browse it after::

    cd sandbox
    ./manage.py runserver

Note that you will need to have test credentials for Avalara in a private
``integration.py`` module.

Changelog
=========

0.2.1
-----

Fix a few issues with submitting orders.

0.2
---

Support Oscar 1.0 and solve a cache key issue.

0.1.1
-----

Patch release to limit support to ``django-oscar>=0.6,<1.0``.

0.1
---

Initial version - supports ``django-oscar>=0.6``.

