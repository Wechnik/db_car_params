from dataclasses import dataclass, is_dataclass


class BaseAttribute:
    """Базовый аттрибут. Вспомогательный класс для работы с dataclass."""

    @classmethod
    def from_json(cls, json_repr: dict):
        """
        Сформировать dataclass из JSON. Поддерживает неограниченную вложенность dataclass.
        :param json_repr: JSON-представление dataclass.
        :return: dataclass, заполненный из JSON.
        """
        json_repr = json_repr or {}

        init_data = {}
        for cls_field_name, cls_field_type in cls.__annotations__.items():
            if is_dataclass(cls_field_type):
                init_data[cls_field_name] = cls_field_type.from_json(json_repr.get(cls_field_name))
            else:
                init_data[cls_field_name] = json_repr.get(cls_field_name)

        return cls(**init_data)

    def to_json(self) -> dict:
        """Получить JSON-представление dataclass. Поддерживает неограниченный уровень вложенности dataclass."""
        json = {}
        for cls_field_name, cls_field_type in self.__annotations__.items():
            if is_dataclass(cls_field_type) and isinstance(getattr(self, cls_field_name), cls_field_type):
                json[cls_field_name] = getattr(self, cls_field_name).to_json()
            else:
                json[cls_field_name] = getattr(self, cls_field_name)

        return json

    def map_values(self, map_dict: dict) -> None:
        for cls_field_name, cls_field_type in self.__annotations__.items():
            attr = getattr(self, cls_field_name)
            if is_dataclass(cls_field_type) and isinstance(attr, cls_field_type):
                attr.map_values(map_dict)
            else:
                setattr(self, cls_field_name, map_dict.get(attr))


@dataclass
class YearsOfProduction(BaseAttribute):
    """Годы производства."""

    start: int
    end: int

    def __str__(self):
        if not self.start:
            return ''
        if self.end:
            return f'{self.start} - {self.end}'
        else:
            return f'С {self.start}'


@dataclass
class Measurement(BaseAttribute):
    """Измерение."""

    min: int
    max: int
    rec: int


@dataclass
class Tire(BaseAttribute):
    """Покрышка."""

    width: Measurement
    height: Measurement
    diameter: Measurement


@dataclass
class Oil(BaseAttribute):
    """Масло."""

    type: str
    viscosity: str


@dataclass
class Wiper(BaseAttribute):
    """Дворник."""

    length: Measurement


@dataclass
class Rim(BaseAttribute):
    """Диск."""

    width: Measurement
    diameter: Measurement
    # FIXME: У сверловки только rec
    drilling: Measurement
    offset: Measurement
    center_hole_diameter: Measurement


@dataclass
class Restrictions(BaseAttribute):
    """Ограничение."""

    tire: Tire
    rim: Rim
    oil: Oil
    wiper: Wiper


@dataclass
class Attributes(BaseAttribute):
    """Атрибуты."""

    years_of_production: YearsOfProduction
    restrictions: Restrictions
