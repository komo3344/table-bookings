from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'address')
    fieldsets = [
        ('주요정보', {'fields': ['name', 'category', 'address', 'phone', 'visible']}),
        ('상세정보', {'fields': ['menu_info', 'description']})
    ]
