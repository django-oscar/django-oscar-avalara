from django.contrib import admin

from avalara import models


class RequestAdmin(admin.ModelAdmin):
    list_display = ('doc_code', 'doc_type',
                    'result_code', 'total_taxable', 'total_tax',
                    'error_message', 'date_created')
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
