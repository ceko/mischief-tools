from django.contrib.auth.models import User, Group
from rest_framework import serializers
from mm_tools.web.models import Priority, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'zone', 'type', 'slot']


class PrioritySerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Priority
        fields = ['id', 'added', 'updated', 'item']


class BulkPriorityUpdateSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        item_ids = validated_data.get('items', [])
        user = validated_data.get('user')

        # delete items not in the priority list
        Priority.objects.filter(
            user=user
        ).exclude(
            item__id__in=item_ids
        ).delete()

        # get items that exist
        existing_ids = [i.item_id for i in Priority.objects.filter(
            user=user, item__id__in=item_ids)]
        new_ids = set(item_ids) - set(existing_ids)

        new_items = [Priority(
            item_id=id,
            user=user
        ) for id in new_ids]
        Priority.objects.bulk_create(new_items)

        return new_items
