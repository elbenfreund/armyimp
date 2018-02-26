import pytest
from django.urls import reverse

from armyimp.apps.w40k import models


@pytest.mark.django_db
def test_unit_detail_view_reachable(client, unit):
    """Test the list view is reachable under the intended urlname."""
    response = client.get(reverse('w40k:unit_detail', kwargs={'pk': unit.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_unit_list_view_reachable(client):
    """Test the list view is reachable under the intended urlname."""
    response = client.get(reverse('w40k:unit_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_army_unit_detail_view_reachable(client, army_unit):
    """Test the list view is reachable under the intended urlname."""
    response = client.get(reverse('w40k:army_unit_detail', kwargs={'pk': army_unit.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_army_unit_list_view_reachable(client):
    """Test the list view is reachable under the intended urlname."""
    response = client.get(reverse('w40k:army_unit_list'))
    assert response.status_code == 200


@pytest.mark.django_db
class TestArmyUnitCreateView():
    """Unittest for ``ArmyUnitCreateView``."""

    def test_get_success(self, client, unit):
        """Test that request is successful if required parameters are provided."""
        response = client.get(reverse('w40k:army_unit_create'), {'unit': unit.pk})
        assert response.status_code == 200

    def test_get_missing_unit_parameter(self, client):
        """Test that request fails if required parameters are missing."""
        response = client.get(reverse('w40k:army_unit_create'))
        assert response.status_code == 404

    def test_post_missing_unit_parameter(self, client):
        """Test that request fails if required parameters are missing."""
        response = client.post(reverse('w40k:army_unit_create'))
        assert response.status_code == 404

    def test_correct_nr_army_model_formset_extras(self, client, unit):
        """
        Test that we get the right number of extra army model formset forms.

        We expect as many forms as the unit has min. models.
        """
        response = client.get(reverse('w40k:army_unit_create'), {'unit': unit.pk})
        context_formset = response.context['army_model_formset']
        assert context_formset.extra == unit.models_min

    def test_post_valid_data_creates_instances(self, client, unit, army_unit_data):
        """Test that passing valid data creates the expected instances."""
        old_army_unit_count = models.ArmyUnit.objects.all().count()
        old_army_models_count = models.ArmyUnit.objects.all().count()
        response = client.post(reverse('w40k:army_unit_create'), army_unit_data)
        assert response.status_code == 302
        assert models.ArmyUnit.objects.all().count() == old_army_unit_count + 1
        assert models.ArmyModel.objects.all().count() == old_army_models_count + unit.models_min

    def test_post_missing_army_model_model(self, client, unit, army_unit_data):
        """Test that a formset form missing a value for ``model`` will raise an error."""
        model_count = unit.models_min
        # Set the last forms ``model`` value ``empty``.
        army_unit_data['models-{}-model'.format(model_count - 1)] = ''

        old_army_unit_count = models.ArmyUnit.objects.all().count()
        response = client.post(reverse('w40k:army_unit_create'), army_unit_data)
        assert response.status_code == 200
        assert models.ArmyUnit.objects.all().count() == old_army_unit_count
        assert response.context['form'].is_valid()
        formset = response.context['army_model_formset']
        assert not formset.is_valid()
        assert formset.errors[model_count - 1]
