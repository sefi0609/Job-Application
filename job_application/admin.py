from django.contrib import admin
from .models import Form


class FormAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'resume')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('start_date', 'occupation')
    ordering = ('first_name',)
    readonly_fields = ('first_name', 'last_name', 'email',
                       'start_date', 'resume', 'occupation')


admin.site.register(Form, FormAdmin)
