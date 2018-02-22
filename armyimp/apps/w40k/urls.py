from django.urls import path
from django.views import generic as generic_views


app_name = 'w40k'

urlpatterns = [
    path(r'', generic_views.TemplateView.as_view(template_name='w40k/landing_page.html'),
         name='landing_page'),
]
