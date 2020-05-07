from django.contrib.auth.models import User, Group
from rest_framework import viewsets, filters
from rest_framework import permissions
from mm_tools.web.models import Priority, Item
from mm_tools.web.permissions import EXPORT_PRIORITIES
from .serializers import BulkPriorityUpdateSerializer, AllPrioritySerializer, PrioritySerializer, ItemSerializer
import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, exceptions, settings as api_settings
from rest_framework_csv.renderers import CSVRenderer

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

DEFAULT_RENDERERS = [JSONRenderer, BrowsableAPIRenderer]

# TODO: Add validation (MC/BWL/ZG validation)


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all().select_related(
        'user', 'item').order_by('item__zone', 'item__name')
    serializer_class = PrioritySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'bulk_update':
            return BulkPriorityUpdateSerializer
        elif self.action == 'all':
            return AllPrioritySerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False, renderer_classes=DEFAULT_RENDERERS + [CSVRenderer, ])
    def all(self, request):
        if not request.user.has_perm(EXPORT_PRIORITIES):
            raise exceptions.PermissionDenied()

        serializer = AllPrioritySerializer(self.queryset.all(), many=True)
        if isinstance(request.accepted_renderer, CSVRenderer):
            return Response(serializer.data)
        else:
            return Response({'results': serializer.data})

    @action(methods=['post'], detail=False)
    def bulk_update(self, request):
        serializer = BulkPriorityUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(status=status.HTTP_201_CREATED)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['zone', 'name']
    search_fields = ['name', ]
