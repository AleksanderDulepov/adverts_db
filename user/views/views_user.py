from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from user.models import User
from user.serializers.serializers_user import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    # переопределение метода для добавления колонки total_adverts
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(total_adverts=Count('advert', filter=Q(advert__is_published=True)))
        return super().get(request, *args, **kwargs)


class UserDetailView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserCreateSerializer

class UserUpdateView(UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserDestroySerializer

