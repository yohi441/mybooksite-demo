from django.contrib import admin
from . import models


admin.site.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("thumbnail",)
admin.site.register(models.Category)


