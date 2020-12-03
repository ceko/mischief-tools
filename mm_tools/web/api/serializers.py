from django.contrib.auth.models import User, Group
from rest_framework import serializers
from mm_tools.web.models import Priority, Item, RAIDS, BLACKWING_LAIR, MOLTEN_CORE, ZUL_GURUB, ONYXIA, AQ_40, NAXX, ItemTier


class ItemTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTier
        fields = ('id', 'name', 'color')


class ItemSerializer(serializers.ModelSerializer):
    tiers = ItemTierSerializer(many=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'zone', 'type', 'slot', 'tiers']


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
        if len(ids) > 6:
            raise serializers.ValidationError("Too many items specified.")

        items = Item.objects.filter(id__in=ids).prefetch_related('tiers')

        def by_raid(items, raid):
            return [i for i in items if i.zone == raid]

        naxx_items = by_raid(items, NAXX)

        if len(naxx_items) > 3:
            raise serializers.ValidationError(
                "Too many Naxx items specified.")

        tier_count = {}

        for item in items:
            for tier in item.tiers.all():
                tier_count[tier.id] = tier_count.get(tier.id, 0) + 1

        if [i for i in tier_count.values() if i > 1]:
            raise serializers.ValidationError(
                "Only one of each tier allowed.")

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
