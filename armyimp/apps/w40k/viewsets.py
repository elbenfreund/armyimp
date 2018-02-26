from rest_framework import viewsets

from . import models, serializers


class UnitViewSet(viewsets.ModelViewSet):
    """Viewset for ``Unit`` instances."""

    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer
