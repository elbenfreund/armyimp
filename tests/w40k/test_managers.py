import pytest

from armyimp.apps.w40k import models


@pytest.mark.django_db
class TestWeaponProfileManager():
    """Unit tests for ``WeaponProfileManager``."""

    def test_get_by_natural_key(self, weapon_profile):
        """Test that the returned instance is the correct one."""
        key = (weapon_profile.name,)
        assert models.WeaponProfile.objects.get_by_natural_key(*key) == weapon_profile
