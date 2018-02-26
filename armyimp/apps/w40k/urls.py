from django.urls import include, path
from django.views import generic as generic_views
from rest_framework import routers

from . import views, viewsets

app_name = 'w40k'

router = routers.DefaultRouter()
router.register(r'units', viewsets.UnitViewSet)

urlpatterns = [
    path(r'', generic_views.TemplateView.as_view(template_name='w40k/landing_page.html'),
         name='landing_page'),
    path(r'api/', include(router.urls)),
    path(r'army_unit/', views.ArmyUnitListView.as_view(), name='army_unit_list'),
    path(r'army_unit/create/', views.ArmyUnitCreateView.as_view(), name='army_unit_create'),
    path(r'army_unit/<int:pk>/', views.ArmyUnitDetailView.as_view(), name='army_unit_detail'),
    path(r'unit/', views.UnitListView.as_view(), name='unit_list'),
    path(r'unit/<int:pk>/', views.UnitDetailView.as_view(), name='unit_detail'),
]
