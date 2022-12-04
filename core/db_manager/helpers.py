from copy import deepcopy


def deepmerge(base_dict: dict, add_dict: dict, include_nulls: bool = False) -> dict:
    """
    Объединить второй словарь с первым, с поддержкой неограниченного уровня вложенности.
    Первый словарь будет изменен.
    Элементы второго словаря извлекаются через deepcopy.
    :param base_dict: Базовый словарь.
    :param add_dict: Словарь, дополняющий базовый словарь.
    :param include_nulls:
    :return: Измененный base_dict.
    """
    for key, value in add_dict.items():
        if isinstance(value, dict) and isinstance(base_dict.get(key), dict):
            deepmerge(base_dict[key], value)
        else:
            if not include_nulls and value is None:
                continue

            base_dict[key] = deepcopy(value)

    return base_dict


def deep_set(base_dict: dict, path: str, value) -> None:
    """Установить значение по ключу с неограниченным уровнем вложенности."""
    keys = path.split('__')

    last_level = base_dict
    for i, key in enumerate(keys[:-1]):
        if key not in last_level or not isinstance(last_level[key], dict):
            last_level[key] = {}
        last_level = last_level[key]
    last_level[keys[-1]] = value
