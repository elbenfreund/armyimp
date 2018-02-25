from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic as generic_views

from . import forms, models


class ArmyUnitCreateView(generic_views.CreateView):
    """View to create a new ``ArmyUnit`` instance."""

    model = models.ArmyUnit
    form_class = forms.ArmyUnitForm
    army_models_formset_prefix = 'models'

    def add_unit(self, data):
        """Add the related unit to the view."""
        unit_pk = data.get('unit')
        self.unit = get_object_or_404(models.Unit, pk=unit_pk)
        return self.unit

    def get(self, request, *args, **kwargs):
        """Use the GET context to fetch the unit."""
        self.add_unit(request.GET)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Use the POST context to fetch the unit."""
        self.add_unit(request.POST)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Extend default context.

        In particular:
            - Add ``self.unit``
            - If no army model formset is being passed to the method (due to a
            previous (failed) post request, add a new one.
        """
        context = super().get_context_data(**kwargs)
        context['unit'] = self.unit
        if not context.get('army_model_formset', None):
            context['army_model_formset'] = self.get_army_model_formset()
        return context

    def get_form_kwargs(self):
        """
        Extend default ``kwargs``.

        Include ``Unit`` instance so it can be passed to ``form_class`` as initial data.
        """
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'unit': self.unit}
        return kwargs

    def form_valid(self, form):
        """
        Custom handling of validated forms.

        As this function gets called once we successfully validated our main form, we now
        validate the dependent formsets. Only if those validate as well we actually commit
        the new instances to the database and redirect.

        Returns:
            HttpResponseRedirect or self.form_invalid: Redirect to ``self.success_url``
                if all 'child formsets' validated too. Otherwise call ``self.form_invalid``.
        """
        # We can not commit to the db already as we not yet know if the formsets
        # will be valid at all.
        army_unit = form.save(commit=False)
        army_model_formset = self.get_army_model_formset(army_unit)

        if army_model_formset.is_valid():
            self.object = form.save()
            army_model_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_army_model_formset_class(self):
        """
        Return a customized formset class in order to provide additional validation.

        Note:
            - This formset starts out with exactly the amount of forms
            needed to create this unit's minimal amount of models.
            - It validates that the total mount of forms is at least the model's
            ``models_min`` and does not exceed it's ``models_max``.
        """
        formset_class = inlineformset_factory(
            models.ArmyUnit, models.ArmyModel,
            form=forms.ArmyModelForm, fields=('model',),
            extra=self.unit.models_min, can_delete=False,
            min_num=self.unit.models_min, validate_min=True,
            max_num=self.unit.models_max, validate_max=True
        )
        return formset_class

    def get_army_model_formset(self, instance=None):
        """Construct a formset representing models for this unit."""
        def get_form_kwargs(unit):
            kwargs = {'unit': unit}
            return kwargs

        # Create a dummy instance for the forms 'parent' instance.
        # Needed for the initial GET request.
        if not instance:
            instance = models.ArmyUnit()

        FormsetClass = self.get_army_model_formset_class()  # NOQA

        if self.request.method in ('POST', 'PUT'):
            armymodel_formset = FormsetClass(
                self.request.POST,
                prefix=self.army_models_formset_prefix,
                form_kwargs=get_form_kwargs(self.unit),
                queryset=models.ArmyModel.objects.none(), instance=instance
            )
        else:
            armymodel_formset = FormsetClass(
                prefix=self.army_models_formset_prefix,
                form_kwargs=get_form_kwargs(self.unit),
                queryset=models.ArmyModel.objects.none(), instance=instance
            )
        return armymodel_formset


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
