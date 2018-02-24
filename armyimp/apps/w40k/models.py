from collections import namedtuple

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

Damagerange = namedtuple('Damagerange', ('min', 'max'))


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
    DIE_TYPES = (3, 6)

    name = models.CharField(max_length=100, unique=True)
    weapon = models.ForeignKey('Item', related_name='weapon_profiles', on_delete=models.CASCADE)
    category = models.CharField(choices=ITEM_CATEGORIES, max_length=20)
    min_range = models.PositiveIntegerField(null=True, blank=True)
    max_range = models.PositiveIntegerField(null=True, blank=True)
    attack_type = models.CharField(
        choices=[(each, each) for each in ATTACK_TYPES],
        max_length=20, help_text=_("This specifies which attack specific extra rules apply.")
    )
    number_of_attacks = models.CharField(max_length=5, null=False, blank=False)
    _strength_value = models.IntegerField(null=True, blank=True,
        help_text=_("Fix STRENGTH value."))
    _strength_multiplier = models.IntegerField(null=True, blank=True,
        help_text=_("Multiplier for effective STRENGTH value."))
    _strength_user = models.BooleanField(
        help_text=_("Set to TRUE if the STRENGTH is determined by the USER."))
    armor_penetration = models.IntegerField(null=True, blank=True)
    _damage_value = models.IntegerField(null=True, blank=True,
        help_text=_("Use this if the profile deals a fixed amount of DAMAGE."))
    _damage_die_type = models.IntegerField(
        choices=[(each, 'W{}'.format(each)) for each in DIE_TYPES],
        null=True, blank=True,
        help_text=_("Use his to specify which type of die is used, if any."))
    _damage_dice_amount = models.IntegerField(null=True, blank=True,
        help_text=_("Use thisi to specify how many die are used, if any."))

    comments = models.TextField(blank=True)

    def __str__(self):
        """Return string representation."""
        return self.name

    @property
    def strength(self):
        """
        Return this profile's effective STRENGTH value.

        Returns:
            string: Either the fix STRENGTH value, the multiplier or 'User'.

        Raises:
            ValueError: If more than one of the relevant private attributes has
            been populated with a value.

        Note:
            This is is exactly *one* of ``self.strength_value/multiplier/user``.
        """
        values = [bool(each) for each in (self._strength_value,
            self._strength_multiplier, self._strength_user)]

        if values.count(True) > 1:
            raise ValueError(_("More than one STRENGTH related attribute has been provided!"))

        if self._strength_value:
            result = str(self._strength_value)
        elif self._strength_multiplier:
            result = str(self._strength_multiplier)
        elif self._strength_user:
            result = _("User")
        elif values.count(True) == 0:
            raise ValueError(_("No STRENGTH related attribute has been provided!"))
        return result

    @property
    def damage(self):
        """
        Return this profile's damage.

        Returns:
            int or tuple: Either a fixed value as an integer or a min/max tuple in
                case the damage is a range (due to being dice-based).

        Raises:
            ValueError: If a fixed and dice based values are present.
            ValueError: If only one of ``_damage_die_type`` and ``_damage_dice_amount`` is present.
        """
        def get_damage_range(die_type, dice_amount):
            min_ = dice_amount
            max_ = dice_amount * die_type
            return Damagerange(min_, max_)

        if self._damage_value and (self._damage_die_type or self._damage_dice_amount):
            raise ValueError(_("Fixed as well as die based damage has been provided!"))
        if not (self._damage_die_type and self._damage_dice_amount):
            raise ValueError(
                _("In case of die based damage 'die_type' and 'dice_amount' need to be provided.")
            )

        if self._damage_value:
            result = self._damage_value
        else:
            result = get_damage_range(self._damage_die_type, self._damage_dice_amount)
        return result


class Item(models.Model):
    """An item as given in the codex."""

    name = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        """Return string representation."""
        return '{s.name}'.format(s=self)

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

    class Meta:
        unique_together = (('organization', 'item'),)

    def __str__(self):
        """Return string representation."""
        return '{s.item} ({s.organization})'.format(s=self)


class Organization(models.Model):
    """This is a party that has its own 'codex'."""

    name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField('Item', blank=True, through='OrganizationItemIntermediate',
        related_name='organizations',
        help_text=_("These are all items accessible to any unit of that organization.")
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name


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

    def __str__(self):
        """Return string representation."""
        return '{s.name} {s.organization} Weapons'.format(s=self)


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

    def __str__(self):
        """Return string representation."""
        return self.name

    @property
    def name(self):
        """Return this models name."""
        return self.profile.name


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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name


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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name

    def get_absolute_url(self):
        """Return this instances canonical url."""
        return reverse('w40k:unit_detail', kwargs={'pk': self.pk})


class UnitAbility(models.Model):
    """A unit ability as per codex."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name


class UnitKeyword(models.Model):
    """A unit keyword as per codex."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name


class FactionKeyword(models.Model):
    """A faction keyword as per codex."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """Return string representation."""
        return self.name


class Army(models.Model):
    """A particular army."""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        """Return string representation."""
        return self.name


class ArmyUnit(models.Model):
    """A particular unit that is part of an army."""

    army = models.ForeignKey("Army", related_name='units', on_delete=models.CASCADE,
        help_text=_("The army this unit is part of."))
    name = models.CharField(max_length=100, blank=True, unique=True)
    unit = models.ForeignKey("Unit", on_delete=models.CASCADE,
        help_text=_("The 'unittemplate' this unit is an instance of."))
    models = models.ManyToManyField('ArmyModel',
        help_text=_("The particular models (e.g. configurations present in this unit."))

    def __str__(self):
        """Return string representation."""
        return '{s.unit.name} ({s.army.name})'.format(s=self)

    def get_absolute_url(self):
        """Return this instances canonical url."""
        return reverse('w40k:armyunit_detail', kwargs={'pk': self.pk})


class ArmyModel(models.Model):
    """A particular model (e.g. configuration) that is part of a specific unit."""

    unit = models.ForeignKey("ArmyUnit", on_delete=models.CASCADE,
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
