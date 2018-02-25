from django.db import models


class WeaponProfileManager(models.Manager):
    """Custom manager class for ``WeaponProfile``."""

    def get_by_natural_key(self, name):
        """Return an instance by its natural key."""
        return self.get(name=name)
