from django.views import generic as generic_views

from . import models


class ArmyUnitDetailView(generic_views.DetailView):
    """Detail view for ``ArmyUnit`` instances."""

    model = models.ArmyUnit
    context_object_name = 'unit'


class ArmyUnitListView(generic_views.ListView):
    """List view for ``ArmyUnit`` instances."""

    model = models.ArmyUnit


class UnitDetailView(generic_views.DetailView):
    """Detail view for ``ArmyUnit`` instances."""

    model = models.Unit
    context_object_name = 'unit'


class UnitListView(generic_views.ListView):
    """List view for ``Unit`` instances."""

    model = models.Unit
