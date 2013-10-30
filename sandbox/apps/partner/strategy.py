from oscar.apps.partner.strategy import US


class Selector(object):

    def strategy(self, request=None, user=None, **kwargs):
        return US(request)
