from db_manager.models import Vehicle


class Brand(Vehicle):
    class Meta:
        proxy = True


class Configuration(Vehicle):
    class Meta:
        proxy = True


class VehicleModel(Vehicle):
    class Meta:
        proxy = True


class Generation(Vehicle):
    class Meta:
        proxy = True


class Restyling(Vehicle):
    class Meta:
        proxy = True
