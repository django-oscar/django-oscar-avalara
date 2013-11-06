from oscar.apps.checkout.app import CheckoutApplication

from . import views


class AvalaraCheckoutApplication(CheckoutApplication):
    # Use custom payment details view so we can interact with Avalara
    payment_details_view = views.PaymentDetailsView
    thankyou_view = views.ThankYouView


application = AvalaraCheckoutApplication()
