import random

from factory import DjangoModelFactory, SubFactory
from faker import Faker

from armyimp.apps.w40k import models

fake = Faker()


class OrganizationFactory(DjangoModelFactory):
    """Factory for ``Organization`` instances."""

    name = fake.name()

    class Meta:
        model = models.Organization


class ArmyFactory(DjangoModelFactory):
    """Factory for ``Army`` instances."""

    name = fake.name()

    class Meta:
        model = models.Army


class UnitFactory(DjangoModelFactory):
    """Factory for ``Unit`` instances."""

    name = fake.name()
    organization = SubFactory(OrganizationFactory)
    is_named_character = fake.boolean()
    power_rating = random.randint(0, 20)
    model_price = random.randint(0, 200)
    models_max = random.randint(0, 20)

    class Meta:
        model = models.Unit


class ArmyunitFactory(DjangoModelFactory):
    """Factory for ``ArmyUnit`` instances."""

    class Meta:
        model = models.ArmyUnit

    army = SubFactory(ArmyFactory)
    unit = SubFactory(UnitFactory)
