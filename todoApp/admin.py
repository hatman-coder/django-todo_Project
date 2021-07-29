from django.contrib import admin
from todoApp.models import todoModel
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(todoModel, TodoAdmin)
