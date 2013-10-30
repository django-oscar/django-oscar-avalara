from django.contrib import admin

from avalara import models


class RequestAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'method', 'url', 'date_created')
    readonly_fields = (
        'account_number',
        'method',
        'url',
        'request_html',
        'response_html',
        'request',
        'response',
        'date_created')


admin.site.register(models.Request, RequestAdmin)
