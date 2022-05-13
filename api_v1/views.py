from rest_framework import viewsets
from chem.serializers import ChemicalSerializer
from chem.models import Chemical, ChemicalSynonym
from rest_framework import permissions
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication
)
from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination
)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api_v1.authentication import TokenAuthWithQueryString


class ChemicalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Query for chemicals in our database
    """
    model = Chemical
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthWithQueryString,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['=iupac', '=name', '=synonyms__name', 'smiles', 'inchi']
    filterset_fields = ['name', 'smiles', 'iupac', 'inchi', 'synonyms__name']

    def get_queryset(self):
        if self.request.GET:
            return self.model.objects.all()
        return self.model.objects.none()
