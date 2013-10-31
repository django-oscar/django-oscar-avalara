import logging

from oscar.apps.checkout import views
from django.contrib import messages
from django.template import loader

import avalara

logger = logging.getLogger('avalara')


class PaymentDetailsView(views.PaymentDetailsView):

    def build_submission(self, **kwargs):
        # Override the build_submission method so we can apply taxes to the
        # submission dict

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

    def get_context_data(self, **kwargs):
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['show_tax_separately'] = True
        return ctx

    def handle_successful_order(self, order):
        # Override the handle_successful_order method so we can submit the
        # order to Avalara for tax reporting

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
