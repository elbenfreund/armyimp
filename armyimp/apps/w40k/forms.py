from django import forms
from django.forms import widgets

from . import models


class ArmyModelForm(forms.ModelForm):
    """Form primarily used to add custom validation."""

    def __init__(self, unit, *args, **kwargs):
        """
        Instantiate a new instance.

        Note:
            We require a ``Unit`` instance as an additional argument in order
            to limit the ``model`` queryset to only those ``UnitModel`` instances
            that are viable options for the given unit.
        """
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = unit.models.all()

    class Meta:
        model = models.ArmyModel
        fields = ('model',)


class ArmyUnitForm(forms.ModelForm):
    """
    Formclass for ``ArmyUnit`` instances.

    Note:
        We change the widget for the ``unit`` field to a ``HiddenInput`` as this should bit be
        user selectable (at least for not) within the form but is passed as a request parameter,
        so we simply need to store its value here.
    """

    class Meta:
        model = models.ArmyUnit
        fields = ('army', 'unit', 'name')
        widgets = {'unit': widgets.HiddenInput}
