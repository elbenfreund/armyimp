from random import randint

import factory
from factory import DjangoModelFactory, LazyAttribute, SubFactory

from armyimp.apps.w40k import models


class OrganizationFactory(DjangoModelFactory):
    """Factory for ``Organization`` instances."""

    name = factory.Faker('name')

    class Meta:
        model = models.Organization


class ArmyFactory(DjangoModelFactory):
    """Factory for ``Army`` instances."""

    name = factory.Faker('name')

    class Meta:
        model = models.Army


class ModelProfileFactory(DjangoModelFactory):
    """Factory for ``ModelProfile`` instances."""

    name = factory.Faker('name')
    weapon_skill = randint(1, 6)
    strength = randint(1, 6)
    toughness = randint(1, 15)
    wounds = randint(1, 20)
    leadership = randint(1, 10)
    saves = randint(1, 6)

    class Meta:
        model = models.ModelProfile


class UnitModelFactory(DjangoModelFactory):
    """Factory for ``UnitModel`` instances."""

    unit = SubFactory('tests.w40k.factories.UnitFactory')
    profile = SubFactory(ModelProfileFactory)
    min_amount = randint(1, 10)
    max_amount = LazyAttribute(lambda s: s.min_amount + randint(0, 10))

    class Meta:
        model = models.UnitModel


class UnitFactory(DjangoModelFactory):
    """Factory for ``Unit`` instances."""

    name = factory.Faker('name')
    organization = SubFactory(OrganizationFactory)
    is_named_character = factory.Faker('boolean')
    power_rating = randint(0, 20)
    model_price = randint(0, 200)
    models_min = randint(0, 20)
    models_max = LazyAttribute(lambda s: s.models_min + randint(0, 10))

    class Meta:
        model = models.Unit

    @factory.post_generation
    def create_unit_models(self, create, extracted, *args, **kwargs):
        """Create ``UnitModel`` instances related to this unit."""
        if not create:
            return
        UnitModelFactory.create_batch(3, unit=self)


class ArmyunitFactory(DjangoModelFactory):
    """Factory for ``ArmyUnit`` instances."""

    class Meta:
        model = models.ArmyUnit

    army = SubFactory(ArmyFactory)
    unit = SubFactory(UnitFactory)


class ArmyModelFactory(DjangoModelFactory):
    """Factory for ``ArmyModel`` instances."""

    class Meta:
        model = models.ArmyModel

    unit = SubFactory(UnitFactory)
    model = SubFactory(UnitModelFactory)


class ItemFactory(DjangoModelFactory):
    """Factory for ``Item`` instances."""

    class Meta:
        model = models.Item

    name = factory.Faker('name')


class OrganizationItemIntermediateFactory(DjangoModelFactory):
    """Factory for ``OrganizationItemIntermediate`` instances."""

    class Meta:
        model = models.OrganizationItemIntermediate

    organization = SubFactory(OrganizationFactory)
    item = SubFactory(ItemFactory)
    price = randint(0, 300)


class WeaponProfileFactory(DjangoModelFactory):
    """Factory for ``WeaponProfile`` instances."""

    class Meta:
        model = models.WeaponProfile

    name = factory.Faker('name')
    weapon = SubFactory(ItemFactory)
    category = models.WeaponProfile.ITEM_CATEGORIES[0][0]
    range_min = randint(0, 50)
    range_max = LazyAttribute(lambda s: s.range_min + randint(0, 200))
    attack_type = models.WeaponProfile.ATTACK_TYPES[0]
    number_of_attacks_min = randint(1, 4)
    number_of_attacks_max = LazyAttribute(lambda s: s.number_of_attacks_min + randint(0, 4))
    strength_min = randint(1, 4)
    strength_max = LazyAttribute(lambda s: s.strength_min + randint(0, 4))
    damage_min = randint(1, 4)
    damage_max = LazyAttribute(lambda s: s.damage_min + randint(0, 4))


class WargearListFactory(DjangoModelFactory):
    """Factory for ``WargearList`` instances."""

    class Meta:
        model = models.WargearList

    name = models.WargearList.WARGEAR_LISTS[0]
    organization = SubFactory(OrganizationFactory)


class UnitAbilityFactory(DjangoModelFactory):
    """Factory for ``UnitAbility`` instances."""

    class Meta:
        model = models.UnitAbility

    name = factory.Faker('name')


class UnitKeywordFactory(DjangoModelFactory):
    """Factory for ``UnitKeyword`` instances."""

    class Meta:
        model = models.UnitKeyword

    name = factory.Faker('name')


class FactionKeywordFactory(DjangoModelFactory):
    """Factory for ``FactionKeyword`` instances."""

    class Meta:
        model = models.FactionKeyword

    name = factory.Faker('name')
