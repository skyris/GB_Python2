"""
Работа с ООП:

Создать мета-класс, определяющий в переменную класса Journal имя списка,
с которым работает создаваемый класс. Имя списка должно генерироваться автоматически и соответствовать имени класса,
написанного с большой буквы.

На основе созданного мета-класса создать класс с именем 'BlackPirate'. При этом экземпляр такого класса имеет
обязательный строковый атрибут 'id' длиной ровно 13 символов.

"""


class MyMeta(type):
    def __init__(cls, name, bases, attr_dict):
        pass


class BlackPirate(metaclass=MyMeta):
    def __init__(self):
        self._id = "8" * 13
    @property
    def id(self):
        try:
            return self._id
        except AttributeError:
            raise AttributeError("{} object has no attribute 'id'".format(self.__class__.__name__))
    @id.setter
    def id(self, val):
        if isinstance(val, str) and len(val) == 13:
            self._id = val
        else:
            raise ValueError("Can't assign value to attribute 'id' if it's not 13 symbols long string")
    @id.deleter
    def id(self):
        del (self._id)
