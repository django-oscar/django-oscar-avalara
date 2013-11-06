from django.contrib.localflavor.us import forms as us_forms
from oscar.apps.checkout import forms


class ShippingAddressForm(forms.ShippingAddressForm):
    postcode = us_forms.USZipCodeField(label="Zip code")
    state = us_forms.USStateField(label="State", widget=us_forms.USStateSelect)
