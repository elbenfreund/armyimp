from pytest_factoryboy import register

import factories

register(factories.OrganizationFactory)
register(factories.ArmyFactory)
register(factories.UnitFactory)
register(factories.ArmyunitFactory)
