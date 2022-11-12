from rest_framework import serializers

from advert.models import Advert
from advert.validators import bool_valid


class AdvertSerializer(serializers.ModelSerializer):
	class Meta:
		model=Advert
		fields='__all__'


class AdvertCreateSerializer(serializers.ModelSerializer):

	is_published = serializers.BooleanField(validators=[bool_valid])

	class Meta:
		model=Advert
		fields='__all__'