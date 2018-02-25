import pytest
from faker import Faker
from pytest_factoryboy import register

import factories

fake = Faker()

register(factories.OrganizationFactory)
register(factories.ArmyFactory)
register(factories.UnitFactory)
register(factories.ModelProfileFactory)
register(factories.UnitModelFactory)
register(factories.ArmyunitFactory)
register(factories.ItemFactory)
register(factories.OrganizationItemIntermediateFactory)
register(factories.WeaponProfileFactory)


@pytest.fixture(scope='function')
def army_unit_data(request, army, unit):
    """A dict suitable as POST data to create an ``ArmyUnit``."""
    data = {
        'army': army.pk,
        'name': fake.name(),
        'unit': unit.pk,
    }

    management_data = {
        'models-INITIAL_FORMS': 0,
        'models-MAX_NUM_FORMS': unit.models_max,
        'models-MIN_NUM_FORMS': unit.models_min,
        'models-TOTAL_FORMS': unit.models_min,
    }

    army_model_formset_data = {}
    for i in range(unit.models_min):
        key = 'models-{}-model'.format(i)
        army_model_formset_data[key] = unit.models.all().first().pk

    data.update(management_data)
    data.update(army_model_formset_data)
    return data
