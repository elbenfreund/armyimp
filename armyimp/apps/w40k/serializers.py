from rest_framework import serializers

from . import models


class ItemInlineSerializer(serializers.ModelSerializer):
    """
    Inline serializer for the ``Item`` model.

    This class is not suitable for a complete representation of instances.
    Its use case is to include just the relevant information to its parent
    serializer.
    """

    class Meta:
        model = models.Item
        fields = ('pk', 'name')


class ItemSlotInlineSerializer(serializers.ModelSerializer):
    """
    Inline serializer for the ``ItemSlot`` model.

    This class is not suitable for a complete representation of instances.
    Its use case is to include just the relevant information to its parent
    serializer.
    """

    default = ItemInlineSerializer()

    class Meta:
        model = models.ItemSlot
        fields = ('pk', 'default')


class UnitModelInlineSerializer(serializers.ModelSerializer):
    """Inline serializer for the ``UnitModel`` model.

    This class is not suitable for a complete representation of instances.
    Its use case is to include just the relevant information to its parent
    serializer.
    """

    item_slots = ItemSlotInlineSerializer(many=True)

    class Meta:
        model = models.UnitModel
        fields = ('pk', 'name_suffix', 'profile', 'min_amount', 'max_amount', 'item_slots')


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for the ``Unit`` model."""

    models = UnitModelInlineSerializer(many=True)

    class Meta:
        model = models.Unit
        fields = ('pk', 'name', 'models')
