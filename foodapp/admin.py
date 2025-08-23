from django.contrib import admin

from foodapp import models

# Register your models here.

class FoodZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_approved')

admin.site.register(models.Contact, FoodZoneAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Category)
admin.site.register(models.Dish)
admin.site.register(models.Order)
