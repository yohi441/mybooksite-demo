from django.contrib import admin
from django.contrib.auth.models import Group
from . import models


admin.site.unregister(Group)

admin.site.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("thumbnail",)
admin.site.register(models.Category)


