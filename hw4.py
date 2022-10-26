import json
import keyword
import functools
from typing import Callable


class ColorizeMixin:
    """Changes the color of the text when output to the console"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__repr__ = cls._replace_color(cls.__repr__)

    @classmethod
    def _replace_color(cls, func: Callable) -> Callable:
        """Replace text color"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            text: str = func(*args, **kwargs)
            replaced = f"\033[1;{cls.repr_color_code}m{text}"
            return replaced
        return wrapper


class Advert(ColorizeMixin):
    """A class whose instances allow fields to be accessed through a dot"""
    repr_color_code = 33

    def __init__(self, mapping):
        self.price = 0
        self.data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += "_"
            if key == "price":
                self.price = value
            else:
                self.data[key] = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be >=0")
        self._price = value

    def __getattr__(self, name):
        if hasattr(self.data, name):
            return getattr(self.data, name)
        return Advert.build(self.data[name])

    @classmethod
    def build(cls, obj):
        """Method for processing nested structures"""
        if isinstance(obj, dict):
            return cls(obj)
        elif isinstance(obj, list):
            return [cls.build(item) for item in obj]
        else:
            return obj

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


if __name__ == "__main__":
    test1 = """{
    "title" : "iPhone X",
    "price" : 100,
    "location" : {
        "address" : "город Самара, улица Мориса Тореза, 50",
        "metro_stations" :["Спортивная","Гагаринская"]
        }
        }"""
    ad1 = json.loads(test1)
    iphone_ad = Advert(ad1)
    assert iphone_ad.title == "iPhone X"
    assert iphone_ad.price == 100
    assert iphone_ad.location.address == "город Самара, улица Мориса Тореза, 50"
    assert iphone_ad.location.metro_stations == ["Спортивная", "Гагаринская"]

    test2 = """{
    "title": "python",
    "price" : -100
    }"""
    try:
        ad2 = json.loads(test2)
        python_ad1 = Advert(ad2)
    except ValueError as error:
        assert str(error) == "Price must be >=0"

    test3 = """{
    "title": "python",
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская", "Киевская"]
        }
    }"""
    ad3 = json.loads(test3)
    python_ad2 = Advert(ad3)
    assert python_ad2.price == 0

    test4 = """{
    "title" : "Вельш-корги",
    "price" : 1000,
    "class" : "dogs",
    "location" : {
        "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }"""
    ad4 = json.loads(test4)
    corgi = Advert(ad4)
    assert corgi.class_ == "dogs"
    print(corgi)
