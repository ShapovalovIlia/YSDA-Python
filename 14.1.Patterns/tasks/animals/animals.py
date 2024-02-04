from abc import ABC, abstractmethod


class Cat:
    def say(self) -> str:
        return "meow"


class Dog:
    def say(self, what: str) -> str:
        return what


class Cow:
    def talk(self) -> str:
        return "moo"


class Animal(ABC):
    @abstractmethod
    def say(self) -> str:
        pass
