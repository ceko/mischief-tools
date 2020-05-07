from django.contrib import admin
from .models import Item, Token


class ItemAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'type', 'slot', 'zone')


admin.site.register(Item, ItemAdmin)
admin.site.register(Token, admin.ModelAdmin)
