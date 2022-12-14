from rest_framework import serializers

from db_manager.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    """Сериализатор данных для получения ограничений."""
    attributes = serializers.ReadOnlyField(source='get_hierarchy_attributes_json')
    # attributes = serializers.SerializerMethodField(read_only=True)
    #
    # def get_attributes(self, obj):
    #     return obj.get_hierarchy_attributes().to_json()

    class Meta:
        model = Vehicle
        exclude = ['attrs']


class GetDataByNameRequest(serializers.Serializer):
    """Схема запроса на эндпоинт."""

    brand = serializers.CharField(max_length=200)
    model = serializers.CharField(max_length=200)
    generation = serializers.CharField(max_length=200)
