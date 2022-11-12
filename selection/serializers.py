from django.shortcuts import get_object_or_404
from rest_framework import serializers

from advert.serializers import AdvertSerializer
from selection.models import Selection
from user.models import User

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Selection
        fields=["id", "name"]

class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdvertSerializer(many=True, read_only=True)

    class Meta:
        model=Selection
        fields='__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = "__all__"

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        user_obj = get_object_or_404(User, pk=user_id)
        validated_data['owner'] = user_obj
        return super().create(validated_data)



class SelectionUpdateSerializer(serializers.ModelSerializer):
    # поля, которые НЕ должны быть обновлены
    id = serializers.IntegerField(read_only=True)
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Selection
        fields = "__all__"



class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model=Selection
        fields=['id']