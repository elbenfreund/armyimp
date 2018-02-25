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
