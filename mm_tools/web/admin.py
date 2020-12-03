from django.contrib import admin
from .models import Item, Token, LootAwarded, Priority, ItemTier


class ItemAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'type', 'slot', 'zone')


class LootAwardedAdmin(admin.ModelAdmin):
    list_display = ('first_kill', 'raid', 'item', 'character')
    search_fields = ('character__name',
                     'raid__warcraft_logs_id', 'raid__title')

    def first_kill(self, obj):
        return obj.raid.started_on


class PriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'added', 'updated', 'user',
                    'item', 'zone')

    def zone(self, obj):
        return obj.item.zone


class ItemTierAdmin(admin.ModelAdmin):
    filter_vertical = ('items',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Token, admin.ModelAdmin)
admin.site.register(LootAwarded, LootAwardedAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(ItemTier, ItemTierAdmin)