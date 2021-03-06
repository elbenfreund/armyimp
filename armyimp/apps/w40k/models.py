from collections import namedtuple

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from . import managers

RangeTuple = namedtuple('RangeTuple', ('min', 'max'))

# The way we handle constrains for what items a model in a unit may take/swap is
# by having those options/constrains represented on *a specific* model. That
# means that a particular (included) model can take those item options. That's
# still a bit hacky as the rules work on a unit level such as "(any one) model
# may take" but for now this appears to be easier.
# This approach does not account for rules that allow to swap models not just
# items. Prime example: Inf. Squats swapping to soldiers for a heavy weapon team
# model. For now, the workaround seems to be to create a separate (pseudo) unit
# that has the appropriate model composition


class WeaponProfile(models.Model):
    """
    These are the weapon stats.

    Note:
        The reason we need this as a separate model is that some weapons have
        multiple firing modes with varying stats.

        Strength_value/multiplier/user should be mutually exclusive.
    """

    ITEM_CATEGORIES = (('Ranged', _("Ranged")), ('Melee', _("Melee")))
    ATTACK_TYPES = ('Melee', 'Pistol', 'Rapid Fire', 'Assault', 'Heavy', 'Grenade')

    name = models.CharField(max_length=100, unique=True)
    weapon = models.ForeignKey('Item', related_name='weapon_profiles', on_delete=models.CASCADE)
    category = models.CharField(choices=ITEM_CATEGORIES, max_length=20)
    range_min = models.PositiveIntegerField(null=True, blank=True)
    range_max = models.PositiveIntegerField(null=True, blank=True)
    attack_type = models.CharField(
        choices=[(each, each) for each in ATTACK_TYPES],
        max_length=20, help_text=_("This specifies which attack specific extra rules apply.")
    )
    number_of_attacks_min = models.PositiveIntegerField()
    number_of_attacks_max = models.PositiveIntegerField()
    strength_min = models.PositiveIntegerField()
    strength_max = models.PositiveIntegerField()
    armor_penetration = models.IntegerField(null=True, blank=True)
    damage_min = models.PositiveIntegerField()
    damage_max = models.PositiveIntegerField()
    comments = models.TextField(blank=True)

    objects = managers.WeaponProfileManager()

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)

    @property
    def number_of_attacks(self):
        """Return this profile's number of attacks."""
        return RangeTuple(min=self.number_of_attacks_min, max=self.number_of_attacks_max)

    @property
    def strength(self):
        """Return this profile's strength."""
        return RangeTuple(min=self.strength_min, max=self.strength_max)

    @property
    def damage(self):
        """Return this profile's damage."""
        return RangeTuple(min=self.damage_min, max=self.damage_max)


class Item(models.Model):
    """An item as given in the codex."""

    name = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)

    objects = managers.ItemManager()

    def __str__(self):
        """Return string representation."""
        return '{s.name}'.format(s=self)

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)

    @property
    def per_organization_details(self):
        """Return all ``OrganizationItemIntermediate`` instances related to this item."""
        return OrganizationItemIntermediate.objects.filter(item=self)

    @property
    def price(self):
        """
        Return the items price.

        If the item can be used by more than one ``Organization`` and prices
        differ among them a tuple of tuples with the organization name and price
        is returned.

        Returns:
            int or dict: Returns the items price if its it is either linked only to one
            ``Organization`` or the price is identical among all. In case the price
            differs between organizations a dict with the following structure is returned:
                {organization.pk: (str(organization), int(price))}.

        Raises:
            ValueError: If the item is not linked to an organization.
        """
        detailed_items = self.per_organization_details

        if not detailed_items:
            raise ValueError(_(
                "It looks like this item is not related to any organization."
                " Such inconsistency should not be possible. Please investigate"
                " and consider filing a bug report."
            ))

        unique_prices = set([each.price for each in detailed_items])
        if len(unique_prices) == 1:
            result = unique_prices[0].price
        else:
            result = {}
            # We don't use dict-comprehension to exceeding line length.
            for each in detailed_items:
                orga = detailed_items.organization
                result[orga.pk] = (str(orga), each.price)
        return result


class OrganizationItemIntermediate(models.Model):
    """Intermediate model to add extra information about Items linked to an Organization."""

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(help_text=_(
        "This is the price (per point list) that the item costs for this organization."
        " Please take note that a UnitModel's default items are not included in the models price."
        " And need to be paid for just as any other item."
    ))

    objects = managers.OrganizationItemIntermediateManager()

    class Meta:
        unique_together = (('organization', 'item'),)

    def __str__(self):
        """Return string representation."""
        return '{s.item} ({s.organization})'.format(s=self)

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.organization, self.item)


class Organization(models.Model):
    """This is a party that has its own 'codex'."""

    name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField('Item', blank=True, through='OrganizationItemIntermediate',
        related_name='organizations',
        help_text=_("These are all items accessible to any unit of that organization.")
    )

    objects = managers.OrganizationManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class WargearList(models.Model):
    """
    A codexes dedicated 'wargear lists'.

    Note:
        While this appears to be redundant with ``Item.category`` only a (small) subset of items
        may actually be included in dedicated 'Wargear lists'. These lists are often used to
        specify alternative/additional alternative item options for a model (e.g. 'may be swap for
        an item from the ranged weapons list').
    """

    WARGEAR_LISTS = (_("Ranged"), _("Special"), _("Heavy"), _("Melee"), _("Vehicle Equipment"))

    name = models.CharField(choices=[(each, each) for each in WARGEAR_LISTS], max_length=60)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    items = models.ManyToManyField('Item', related_name='wargear_lists')

    objects = managers.WargearListManager()

    class Meta:
        unique_together = ('name', 'organization')

    def __str__(self):
        """Return string representation."""
        return '{s.name} {s.organization} Weapons'.format(s=self)

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name, self.organization)


class UnitModel(models.Model):
    """
    A model is a *particular model* that is part of a unit.

    Such a model describes a specific (default) configuration as part of the unit as well as all
    substitution and extension options and their constrains.

    Note:
        While its data structure seems like just a trivial intermediate model that does not
        own any extra data we still use this stand alone model in order to provide additional
        methods as well as to use it's instances as foreign keys for ``ModelItems`` instances.
        Also note: A models price (without items) is defined by its ``Unit``.
    """

    unit = models.ForeignKey('Unit', related_name='models', on_delete=models.CASCADE)
    profile = models.ForeignKey('ModelProfile', on_delete=models.CASCADE)
    name_suffix = models.CharField(max_length=80, blank=True,
        help_text=_("Identifier for this particular configuration."))
    min_amount = models.PositiveIntegerField(help_text=_(
        "How many models with this specific setup must the parent unit include at least?"))
    max_amount = models.PositiveIntegerField(help_text=_(
        "How many models with this specific setup may the parent unit include at maximum?"))

    def __str__(self):
        """Return string representation."""
        return self.name

    @property
    def name(self):
        """Return this models name."""
        if not self.name_suffix:
            result = self.profile.name
        else:
            result = '{s.profile.name} ({s.name_suffix})'.format(s=self)
        return result


class ModelProfile(models.Model):
    """A models stats."""

    name = models.CharField(max_length=100, unique=True)
    # Where relevant we omit the '+' as it provides no extra information.
    movement = models.PositiveIntegerField(null=True, blank=True)
    weapon_skill = models.PositiveIntegerField()
    balistic_skill = models.PositiveIntegerField(null=True, blank=True)
    strength = models.PositiveIntegerField()
    toughness = models.PositiveIntegerField()
    wounds = models.PositiveIntegerField()
    attacks = models.PositiveIntegerField(null=True, blank=True)
    leadership = models.PositiveIntegerField()
    saves = models.PositiveIntegerField()

    objects = managers.ModelProfileManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class ItemSlot(models.Model):
    """
    Items options and their defaults for a particular Model (as per codex).

    Note:
        It is important to keep in mind that a model in this framework
        is a specific configuration.
        This is not a mere intermediate model as ``self.default`` may very well be None.
    """

    model = models.ForeignKey('UnitModel', related_name='item_slots', on_delete=models.CASCADE)
    default = models.ForeignKey('Item', null=True, blank=True, related_name='slot_defaults',
        on_delete=models.CASCADE)
    options = models.ManyToManyField('Item', blank=True, related_name='slot_options')
    option_from_list = models.ManyToManyField('WargearList', blank=True)
    min_amount = models.PositiveIntegerField(null=True, blank=True, default=1,
        help_text=_("Min. amount of eligible items this slot takes."))
    max_amount = models.PositiveIntegerField(null=True, blank=True, default=1,
        help_text=_("Max. amount of eligible items this slot takes."))

    def __str__(self):
        """Return string representation."""
        return 'Weaponslot for {}'.format(self.model.name)


class Unit(models.Model):
    """
    A particular unit.

    Besides its own direct attributes units are also a collection of (default) ``UnitModel``s
    that govern what items Models in a unit may carry.
    """

    UNIT_CATEGORIES = (('HQ', _("HQ")), ('Elites', _("Elites")), ('Troops', _("Troops")),
        ('Fast Attack', _("Fast Attack")), ('Heavy Support', _("Heavy Support")),
        ('Flyers', _("Flyers")), ('Dedicated Transport', _("Dedicated Transport")))

    name = models.CharField(max_length=100, unique=True)
    organization = models.ForeignKey('Organization', related_name='units',
        on_delete=models.CASCADE)
    category = models.CharField(choices=[(value, label) for value, label in UNIT_CATEGORIES],
        max_length=20)
    is_named_character = models.BooleanField(help_text=_(
        "Set to true if this is a named Character. This changes how equipped items get handled."))
    power_rating = models.PositiveIntegerField()
    model_price = models.PositiveIntegerField(help_text=_("Points per model"))
    max_per_army = models.PositiveIntegerField(null=True, blank=True,
        help_text=_("How many of this unit an army may include at max."))
    models_min = models.PositiveIntegerField(default=1,
        help_text=_("Minimal amount of models this unit needs to include"))
    models_max = models.PositiveIntegerField(help_text=_(
        "Maximum amount of models this unit may include"))
    transport = models.TextField(blank=True, help_text=_(
        "If this unit has transportation capabilities, specify details here."))
    abilities = models.ManyToManyField('UnitAbility', blank=True)
    keywords = models.ManyToManyField('UnitKeyword', blank=True)
    faction_keywords = models.ManyToManyField('FactionKeyword', blank=True)
    comment = models.TextField(blank=True)

    objects = managers.UnitManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)

    def get_absolute_url(self):
        """Return this instances canonical url."""
        return reverse('w40k:unit_detail', kwargs={'pk': self.pk})


class UnitAbility(models.Model):
    """A unit ability as per codex."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    objects = managers.UnitAbilityManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class UnitKeyword(models.Model):
    """A unit keyword as per codex."""

    name = models.CharField(max_length=100, unique=True)

    objects = managers.UnitKeywordManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class FactionKeyword(models.Model):
    """A faction keyword as per codex."""

    name = models.CharField(max_length=100, unique=True)

    objects = managers.FactionKeywordManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class Army(models.Model):
    """A particular army."""

    name = models.CharField(max_length=200, unique=True)

    objects = managers.ArmyManager()

    def __str__(self):
        """Return string representation."""
        return self.name

    def natural_key(self):
        """Return this instances ``natural_key``."""
        return (self.name,)


class ArmyUnit(models.Model):
    """A particular unit that is part of an army."""

    army = models.ForeignKey("Army", related_name='units', on_delete=models.CASCADE,
        help_text=_("The army this unit is part of."))
    name = models.CharField(max_length=100, blank=True)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE,
        help_text=_("The 'unittemplate' this unit is an instance of."))

    def __str__(self):
        """Return string representation."""
        if self.name:
            result = '{s.name} [{s.unit.name} ({s.army.name})]'.format(s=self)
        else:
            result = '{s.unit.name} ({s.army.name})'.format(s=self)
        return result

    def get_absolute_url(self):
        """Return this instances canonical url."""
        return reverse('w40k:army_unit_detail', kwargs={'pk': self.pk})


class ArmyModel(models.Model):
    """A particular model (e.g. configuration) that is part of a specific unit."""

    unit = models.ForeignKey("ArmyUnit", related_name='models', on_delete=models.CASCADE,
        help_text=_("The specific army unit this model is part of."))
    model = models.ForeignKey("UnitModel", on_delete=models.CASCADE,
        help_text=_("The 'generic unit model' that is the 'template' for this specific model."))
    itemslots = models.ManyToManyField('Item', through='ArmyModelItemSlot',
        help_text=_("The specific itemslot configuration for this model."))

    def __str__(self):
        """Return string representation."""
        return '{s.model.name} ({s.unit.name})'.format(s=self)


class ArmyModelItemSlot(models.Model):
    """
    Specific itemslot configuration for a given ``ArmyModel`` instance.

    Note:
        This is mainly needed in order to account for slots that contain more than one (identical)
        item.
    """

    item = models.ForeignKey('Item', on_delete=models.CASCADE, help_text=_("Equipped item(s)."))
    army_model = models.ForeignKey('ArmyModel', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1,
        help_text=_("Amount of identical! items in this slot."))

    def __str__(self):
        """Return string representation."""
        return 'ArmyModelItemSlot with PK: {s.pk}'.format(s=self)
