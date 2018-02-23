import pytest
from django.urls import reverse


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
