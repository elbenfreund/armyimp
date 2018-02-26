import nested_admin
from django.contrib import admin

from . import models


class ItemSlotInline(nested_admin.NestedTabularInline):
    """Inline ``ItemSlot`` admin representation."""

    model = models.ItemSlot
    extra = 0


class WeaponProfileAdmin(admin.ModelAdmin):
    """``WeaponProfile`` admin representation."""

    model = models.WeaponProfile
    search_fields = ('name',)
    list_display = ('name', 'weapon')
    list_editable = ('weapon',)
    list_filter = ('attack_type',)
    ordering = ('name', 'attack_type')


class ItemAdmin(admin.ModelAdmin):
    """``Item`` admin representation."""

    model = models.Item
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)


class UnitModelAdmin(admin.ModelAdmin):
    """``Model`` admin representation."""

    inlines = (ItemSlotInline,)


class UnitModelInline(nested_admin.NestedTabularInline):
    """Inline ``UnitModel`` admin representation."""

    model = models.UnitModel
    fields = ('profile', 'name_suffix', 'min_amount', 'max_amount')
    inlines = (ItemSlotInline,)
    extra = 0


class UnitAdmin(nested_admin.NestedModelAdmin):
    """"``Unit`` admin representation."""

    list_display = ('name', 'category', 'power_rating')
    search_fields = ('name',)
    list_editable = ('category', 'power_rating')
    list_filter = ('category', 'faction_keywords', 'keywords', 'organization')
    inlines = (UnitModelInline,)


# Army related classes
class ArmyModelItemSlotInline(nested_admin.NestedTabularInline):
    """``ArmyModelItemSlot`` admin inline representation."""

    model = models.ArmyModelItemSlot
    extra = 0


class ArmyModelInline(nested_admin.NestedTabularInline):
    """``ArmyModel`` admin inline representation."""

    model = models.ArmyModel
    fields = ('model',)
    inlines = (ArmyModelItemSlotInline,)
    extra = 0


class ArmyUnitAdmin(nested_admin.NestedModelAdmin):
    """``ArmyUnit`` admin representation."""

    fields = ('army', 'name', 'unit',)
    model = models.ArmyUnit
    inlines = (ArmyModelInline,)


admin.site.register(models.UnitModel, UnitModelAdmin)
admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.WeaponProfile, WeaponProfileAdmin)

admin.site.register(models.UnitAbility)
admin.site.register(models.Organization)
admin.site.register(models.WargearList)
admin.site.register(models.OrganizationItemIntermediate)
admin.site.register(models.FactionKeyword)
admin.site.register(models.UnitKeyword)
admin.site.register(models.ModelProfile)

# Army related register calls
admin.site.register(models.ArmyUnit, ArmyUnitAdmin)

admin.site.register(models.Army)
