from rest_framework import serializers

from user.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    total_adverts = serializers.SerializerMethodField() #для вывода доп атрибута
    location=serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
        )

    def get_total_adverts(self, obj):   #для вывода доп атрибута
        try:
            return obj.total_adverts
        except:
            return None

    class Meta:
        model=User
        fields='__all__'


class UserDetailSerializer(serializers.ModelSerializer):

    location=serializers.SlugRelatedField(
                    many=True,
                    read_only=True,
                    slug_field="name"
                    )
    class Meta:
        model=User
        fields='__all__'


class UserCreateSerializer(serializers.ModelSerializer):

    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(user.password)  # для хеширования переданного пароля

        for location in self._location:
            location_object, created = Location.objects.get_or_create(name=location)
            user.location.add(location_object)

        user.save()
        return user



class UserUpdateSerializer(serializers.ModelSerializer):

    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("location"):   #если поле location будет передано
            self._location = self.initial_data.pop("location")

        if self.initial_data.get("password"):   #если поле password будет передано(для хеширования)
            self._password = self.initial_data.pop("password")

        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        if hasattr(self,"_location"):   #если поле location будет передано
            user.location.clear()
            for location in self._location:
                location_object, created = Location.objects.get_or_create(name=location)
                user.location.add(location_object)

        if hasattr(self, "_password"):  #если поле password будет передано(для хеширования)
            user.set_password(self._password)

        user.save()

        return user



class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']