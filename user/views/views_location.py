from rest_framework.viewsets import ModelViewSet

from user.models import Location
from user.serializers.serializers_location import LocationSerializer


class LocationViewSet(ModelViewSet):
	queryset=Location.objects.all()
	serializer_class=LocationSerializer