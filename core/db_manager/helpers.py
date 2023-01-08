import re
from copy import deepcopy
from typing import Union, List, Any, Optional


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


def deepset(base_dict: dict, path: Union[List[str], str], value, delimiter: str = '__') -> None:
    """Установить значение по ключу с неограниченным уровнем вложенности."""
    keys = path.split(delimiter) if isinstance(path, str) else path.copy()

    last_level = base_dict
    for i, key in enumerate(keys[:-1]):
        if key not in last_level or not isinstance(last_level[key], dict):
            last_level[key] = {}
        last_level = last_level[key]
    last_level[keys[-1]] = value


def deepget(base_dict: Optional[dict], keys: Union[str, List[Any]], default: Any = None) -> Any:
    """
    Получить значение ключа из словаря, с поддержкой неограниченного уровня вложенности.

    :param base_dict: Словарь.
    :param keys: Имена ключей в виде массива или "описания пути" через "/".
    :param default: Значение по-умолчанию.
    """
    _keys = keys.split('/') if isinstance(keys, str) else keys

    result = base_dict or {}
    for i, key in enumerate(_keys):
        result = result.get(key, {} if i < len(_keys) - 1 else default)

    return result


class CaseHelper:
    """Вспомогательный класс для работы с регистрами."""

    @staticmethod
    def snake_to_camel(text: str) -> str:
        """Преобразовать строку из snake_case в camelCase."""
        words = text.split('_')
        if len(words) > 1:
            first, *rest = words
            words = [first] + list(map(lambda word: word.capitalize(), rest))
        return ''.join(words)

    @staticmethod
    def camel_to_snake(text: str) -> str:
        """Преобразовать строку из camelCase в snake_case."""
        return '_'.join(map(lambda txt: txt.lower(), re.findall(r'((?:[A-Z]+|\A)[a-z]*)', text)))
