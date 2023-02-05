from rest_framework import serializers

from db_manager.models import Vehicle, ParamsValue
from db_manager.models.vehicle.attributes import Attributes


class VehicleSerializer(serializers.ModelSerializer):
    """Сериализатор данных для получения ограничений."""
    attributes = serializers.SerializerMethodField(read_only=True)
    configurations = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def replace_ids_with_values(attributes: dict) -> dict:
        valued_attributes = Attributes.from_json(attributes)
        valued_attributes.map_values({choice.id: choice.value for choice in ParamsValue.objects.all()})
        return valued_attributes.to_json()

    def get_attributes(self, obj: Vehicle) -> dict:
        return self.replace_ids_with_values(obj.get_hierarchy_attributes_json)

    # attributes = serializers.SerializerMethodField(read_only=True)
    #
    # def get_attributes(self, obj):
    #     return obj.get_hierarchy_attributes().to_json()

    def get_configurations(self, obj: Vehicle) -> list[dict]:
        configurations = Vehicle.objects.filter(parent=obj)
        configurations_attrs = []
        for config in configurations:
            config_data = VehicleSerializer(config).data
            config_data.pop('configurations')
            config_data['attributes'] = self.replace_ids_with_values(config_data['attributes'])
            configurations_attrs.append(config_data)

        return configurations_attrs

    class Meta:
        model = Vehicle
        exclude = ['attrs', 'parent', '_type']


class GetDataByNameRequest(serializers.Serializer):
    """Схема запроса на эндпоинт."""

    brand = serializers.CharField(max_length=200)
    model = serializers.CharField(max_length=200)
    generation = serializers.CharField(max_length=200)
