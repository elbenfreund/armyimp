import pytest

from armyimp.apps.w40k import models


@pytest.mark.django_db
class TestWeaponProfileManager():
    """Unit tests for ``WeaponProfileManager``."""

    def test_get_by_natural_key(self, weapon_profile):
        """Test that the returned instance is the correct one."""
        key = (weapon_profile.name,)
        assert models.WeaponProfile.objects.get_by_natural_key(*key) == weapon_profile


@pytest.mark.django_db
class TestItemManager():
    """Unit tests for ``ItemManager``."""

    def test_get_by_natural_key(self, item):
        """Test that the returned instance is the correct one."""
        key = (item.name,)
        assert models.Item.objects.get_by_natural_key(*key) == item


@pytest.mark.django_db
class TestOrganizationIntermediateManager():
    """Unit tests for ``OrganizationIntermediateManager``."""

    def test_get_by_natural_key(self, organization_item_intermediate):
        """Test that the returned instance is the correct one."""
        key = (organization_item_intermediate.organization, organization_item_intermediate.item)
        assert models.OrganizationItemIntermediate.objects.get_by_natural_key(*key) == (
            organization_item_intermediate)


@pytest.mark.django_db
class TestOrganizationManager():
    """Unit tests for ``OrganizationManager``."""

    def test_get_by_natural_key(self, organization):
        """Test that the returned instance is the correct one."""
        key = (organization.name,)
        assert models.Organization.objects.get_by_natural_key(*key) == organization


@pytest.mark.django_db
class TestModelProfileManager():
    """Unit tests for ``ModelProfile``."""

    def test_get_by_natural_key(self, model_profile):
        """Test that the returned instance is the correct one."""
        key = (model_profile.name,)
        assert models.ModelProfile.objects.get_by_natural_key(*key) == model_profile


@pytest.mark.django_db
class TestUnitManager():
    """Unit tests for ``Unit``."""

    def test_get_by_natural_key(self, unit):
        """Test that the returned instance is the correct one."""
        key = (unit.name,)
        assert models.Unit.objects.get_by_natural_key(*key) == unit


@pytest.mark.django_db
class TestUnitAbilityManager():
    """Unit tests for ``UnitAbility``."""

    def test_get_by_natural_key(self, unit_ability):
        """Test that the returned instance is the correct one."""
        key = (unit_ability.name,)
        assert models.UnitAbility.objects.get_by_natural_key(*key) == unit_ability


@pytest.mark.django_db
class TestUnitKeywordManager():
    """Unit tests for ``UnitKeyword``."""

    def test_get_by_natural_key(self, unit_keyword):
        """Test that the returned instance is the correct one."""
        key = (unit_keyword.name,)
        assert models.UnitKeyword.objects.get_by_natural_key(*key) == unit_keyword


@pytest.mark.django_db
class TestFactionKeywordManager():
    """Unit tests for ``FactionKeyword``."""

    def test_get_by_natural_key(self, faction_keyword):
        """Test that the returned instance is the correct one."""
        key = (faction_keyword.name,)
        assert models.FactionKeyword.objects.get_by_natural_key(*key) == faction_keyword


@pytest.mark.django_db
class TestArmyManager():
    """Unit tests for ``Army``."""

    def test_get_by_natural_key(self, army):
        """Test that the returned instance is the correct one."""
        key = (army.name,)
        assert models.Army.objects.get_by_natural_key(*key) == army
