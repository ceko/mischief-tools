from django.contrib.auth.models import User, Group
from rest_framework import serializers
from mm_tools.web.models import Priority, Item, RAIDS, BLACKWING_LAIR, MOLTEN_CORE, ZUL_GURUB, ONYXIA, AQ_40


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'zone', 'type', 'slot']


class PrioritySerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Priority
        fields = ['id', 'added', 'updated', 'item']


class AllPrioritySerializer(PrioritySerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta(PrioritySerializer.Meta):
        fields = PrioritySerializer.Meta.fields + ['user', ]


class BulkPriorityUpdateSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.IntegerField())

    def validate(self, data):
        ids = data.get('items')
        if len(ids) > 9:
            raise serializers.ValidationError("Too many items specified.")

        items = Item.objects.filter(id__in=ids)

        def by_raid(items, raid):
            return [i for i in items if i.zone == raid]

        aq_40_items = by_raid(items, AQ_40)
        bwl_items = by_raid(items, BLACKWING_LAIR)
        mc_items = by_raid(items, MOLTEN_CORE)
        ony_items = by_raid(items, ONYXIA)

        if len(aq_40_items) > 3:
            raise serializers.ValidationError(
                "Too many AQ 40 items specified.")

        if len(bwl_items) > 3:
            raise serializers.ValidationError(
                "Too many tier 3 items specified.")

        if len(mc_items) + len(ony_items) > 3:
            raise serializers.ValidationError(
                "Too many tier 1 items specified.")

        return data

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
