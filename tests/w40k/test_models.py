import pytest


@pytest.mark.django_db
class TestWeaponProfile():
    """Unit tests for the ``WeaponProfile`` model."""

    def test_natural_key(self, weapon_profile):
        """Test that the returned natural key is the instances name."""
        assert weapon_profile.natural_key() == (weapon_profile.name,)

    def test_number_of_attacks_property(self, weapon_profile):
        """Test that the returned tuple values are correct."""
        min, max = weapon_profile.number_of_attacks
        assert min == weapon_profile.number_of_attacks_min
        assert max == weapon_profile.number_of_attacks_max

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


@pytest.mark.django_db
class TestItem():
    """Unit tests for the ``Item`` model."""

    def test_natural_key(self, item):
        """Test that the returned natural key is the instances name."""
        assert item.natural_key() == (item.name,)


@pytest.mark.django_db
class TestOrganizationItemIntermediate():
    """Unit tests for the ``OrganizationItemIntermediate`` model."""

    def test_natural_key(self, organization_item_intermediate):
        """Test that the returned natural key is the instances name."""
        expectation = (organization_item_intermediate.organization,
            organization_item_intermediate.item)
        assert organization_item_intermediate.natural_key() == expectation


@pytest.mark.django_db
class TestOrganization():
    """Unit tests for the ``Organization`` model."""

    def test_natural_key(self, organization):
        """Test that the returned natural key is the instances name."""
        assert organization.natural_key() == (organization.name,)


@pytest.mark.django_db
class TestWargearList():
    """Unit tests for the ``WargearList`` model."""

    def test_natural_key(self, wargear_list):
        """Test that the returned natural key is the instances name."""
        expectation = (wargear_list.name, wargear_list.organization)
        assert wargear_list.natural_key() == expectation


@pytest.mark.django_db
class TestModelProfile():
    """Unit tests for the ``ModelProfile`` model."""

    def test_natural_key(self, model_profile):
        """Test that the returned natural key is the instances name."""
        assert model_profile.natural_key() == (model_profile.name,)


@pytest.mark.django_db
class TestUnit():
    """Unit tests for the ``Unit`` model."""

    def test_natural_key(self, unit):
        """Test that the returned natural key is the instances name."""
        assert unit.natural_key() == (unit.name,)


@pytest.mark.django_db
class TestUnitAbility():
    """Unit tests for the ``UnitAbility`` model."""

    def test_natural_key(self, unit_ability):
        """Test that the returned natural key is the instances name."""
        assert unit_ability.natural_key() == (unit_ability.name,)
