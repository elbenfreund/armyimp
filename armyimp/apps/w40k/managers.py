from django.db import models


class WeaponProfileManager(models.Manager):
    """Custom manager class for ``WeaponProfile``."""

    def get_by_natural_key(self, name):
        """Return an instance by its natural key."""
        return self.get(name=name)


class ItemManager(models.Manager):
    """Custom manager class for ``Item``."""

    def get_by_natural_key(self, name):
        """Return an instance by its natural key."""
        return self.get(name=name)


class OrganizationItemIntermediateManager(models.Manager):
    """Custom manager class for ``Item``."""

    def get_by_natural_key(self, organization, item):
        """Return an instance by its natural key."""
        return self.get(organization=organization, item=item)


class OrganizationManager(models.Manager):
    """Custom manager class for ``Organization``."""

    def get_by_natural_key(self, name):
        """Return an instance by its natural key."""
        return self.get(name=name)


class WargearListManager(models.Manager):
    """Custom manager class for ``WargearList``."""

    def get_by_natural_key(self, name, organization):
        """Return an instance by its natural key."""
        return self.get(name=name, organization=organization)


class ModelProfileManager(models.Manager):
    """Custom manager class for ``ModelProfile``."""

    def get_by_natural_key(self, name):
        """Return an instance by its natural key."""
        return self.get(name=name)
