from rest_framework import serializers

from db_manager.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    """Сериализатор данных для получения ограничений."""

    class Meta:
        model = Vehicle
        fields = '__all__'


class GetDataByNameRequest(serializers.Serializer):
    """Схема запроса на эндпоинт."""

    brand = serializers.CharField(max_length=200)
    model = serializers.CharField(max_length=200)
    generation = serializers.CharField(max_length=200)
