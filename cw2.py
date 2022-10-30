import functools
from typing import Callable


class EmojiMixin:
    """Заменяет категорию покемона на эмоджи"""
    ICON = {
        'grass': '🌿',
        'fire': '🔥',
        'water': '🌊',
        'electric': '⚡'
    }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__str__ = cls._replace_str(cls.__str__)

    @classmethod
    def _replace_str(cls, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            text: str = func(*args, **kwargs)
            for word, emoji in cls.ICON.items():
                replaced = text.replace(word, emoji)
                if replaced != text:
                    return replaced
            return text
        return wrapper


class Pokemon(EmojiMixin):
    """Класс Покемон, который выводит имя и категорию покемона"""
    def __init__(self, name: str, poketype: str):
        self.name = name
        self.poketype = poketype

    def __str__(self):
        return f'{self.name}/{self.poketype}'


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    print(bulbasaur)
    pikachu = Pokemon(name='Pikachu', poketype='electric')
    print(pikachu)
