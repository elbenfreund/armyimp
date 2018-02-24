from django import forms
from django.forms import widgets

from . import models


class ArmyModelForm(forms.ModelForm):
    """Form primarily used to add custom validation."""

    def __init__(self, unit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = unit.models.all()

    class Meta:
        model = models.ArmyModel
        fields = ('model',)


class ArmyUnitForm(forms.ModelForm):

    class Meta:
        model = models.ArmyUnit
        fields = ('army', 'unit', 'name')
        widgets = {'unit': widgets.HiddenInput}
