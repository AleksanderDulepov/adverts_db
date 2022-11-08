from rest_framework import serializers

from advert.models import Advert


class AdvertDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model=Advert
		fields='__all__'