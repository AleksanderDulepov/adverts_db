from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from selection.models import Selection
from selection.permissions import SelectionEditPermission
from selection.serializers import SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer, \
    SelectionUpdateSerializer, SelectionDestroySerializer, SelectionSerializer

# через APIviews
# class SelectionListView(ListAPIView):
# 	queryset=Selection.objects.all()
# 	serializer_class=SelectionListSerializer
# 	permission_classes=[AllowAny]
#
# class SelectionDetailView(RetrieveAPIView):
# 	queryset=Selection.objects.all().select_related('owner').prefetch_related('items')
# 	serializer_class=SelectionDetailSerializer
# 	permission_classes=[AllowAny]
#
# class SelectionCreateView(CreateAPIView):
# 	queryset=Selection.objects.all().select_related('owner').prefetch_related('items')
# 	serializer_class=SelectionCreateSerializer
# 	permission_classes=[IsAuthenticated]
#
# class SelectionUpdateView(UpdateAPIView):
# 	queryset=Selection.objects.all().select_related('owner').prefetch_related('items')
# 	serializer_class=SelectionUpdateSerializer
# 	permission_classes=[IsAuthenticated, SelectionEditPermission]
#
# class SelectionDeleteView(DestroyAPIView):
# 	queryset=Selection.objects.all()
# 	serializer_class=SelectionDestroySerializer
# 	permission_classes=[IsAuthenticated, SelectionEditPermission]

# -----------------------------------------------------------------------
# через ModelViewSet
class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all().select_related('owner').prefetch_related('items')
    default_permission = [AllowAny]

    default_serializer = SelectionSerializer
    serializer_classes = {"list": SelectionListSerializer,
                          "retrieve": SelectionDetailSerializer,
                          "create": SelectionCreateSerializer,
                          "partial_update": SelectionUpdateSerializer,
                          "destroy": SelectionDestroySerializer,
                          }
    permission_classes_by_action = {
                                    "create": [IsAuthenticated],
                                    "partial_update": [IsAuthenticated, SelectionEditPermission],
                                    "destroy": [IsAuthenticated, SelectionEditPermission],
                                    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def get_permissions(self):
        return [perm() for perm in self.permission_classes_by_action.get(self.action, self.default_permission)]

