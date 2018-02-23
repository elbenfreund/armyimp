from django.urls import path
from django.views import generic as generic_views

from . import views

app_name = 'w40k'

urlpatterns = [
    path(r'', generic_views.TemplateView.as_view(template_name='w40k/landing_page.html'),
         name='landing_page'),
    path(r'army_unit/', views.ArmyUnitListView.as_view(), name='army_unit_list'),
    path(r'army_unit/<int:pk>/', views.ArmyUnitDetailView.as_view(), name='army_unit_detail'),
    path(r'unit/', views.UnitListView.as_view(), name='unit_list'),
    path(r'unit/<int:pk>/', views.UnitDetailView.as_view(), name='unit_detail'),
]
