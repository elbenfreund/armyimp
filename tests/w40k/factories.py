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
