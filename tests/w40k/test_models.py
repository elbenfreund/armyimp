import pytest


@pytest.mark.django_db
class TestWeaponProfile():
    """Unit tests for the ``WeaponProfile`` model."""

    def test_strength_property(self, weapon_profile):
        """Test that the returned tuple values are correct."""
        min, max = weapon_profile.strength
        assert min == weapon_profile.strength_min
        assert max == weapon_profile.strength_max

    def test_damage_property(self, weapon_profile):
        """Test that the returned tuple values are correct."""
        min, max = weapon_profile.damage
        assert min == weapon_profile.damage_min
        assert max == weapon_profile.damage_max
