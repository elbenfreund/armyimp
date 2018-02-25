import pytest

from armyimp.apps.w40k import forms


@pytest.mark.django_db
def test_army_model_form(unit):
    """Make the forms ``model`` field queryset is limited to passed units models."""
    form = forms.ArmyModelForm(unit)
    assert list(form.fields['model'].queryset) == list(unit.models.all())
