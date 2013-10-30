from oscar.apps.checkout import views
from django.contrib import messages
from django.template import loader

import avalara


class PaymentDetailsView(views.PaymentDetailsView):

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
