"""
Работа с ООП:

В задании по ООП "Создать мета-класс, определяющий в переменную класса Journal имя списка,
с которым работает создаваемый класс. Имя списка должно генерироваться автоматически и соответствовать имени класса,
написанного с большой буквы."

На основе созданного мета-класса создать класс с именем 'BlackPirate'. При этом экземпляр такого класса имеет
обязательный строковый атрибут 'id' длиной ровно 13 символов.

"""


class TypeDescriptor():
    def __init__(self, value):
        if isinstance(value, str) and len(value) == 13:
            self.value = value
    def __set__(self, instance, value):
        print("inst", instance)
        print("val", value)
        if isinstance(value, str) and len(value) == 13:
            self.value = value
    def __get__(self, instance, owner):
        print("inst", instance)
        print("owner", owner)
        return self.value
    def __delete__(self, instance):
        print("inst", instance)
        del self.value

class NewClass():
    id = TypeDescriptor("B"*13)


class NewClass():
    def __init__(self):
        self.id = TypeDescriptor("B"*13)

class MyMeta(type):
    def __init__(cls, name, bases, attr_dict):
        new_attr = name.capitalize()
        setattr(cls, new_attr, [])
        cls.id = TypeDescriptor("A" * 13)


class SOME(metaclass=MyMeta):
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


class MyClass(metaclass=MyMeta):
    id = TypeDescriptor("8" * 13)

#
# class TypedProperty():
#     def __init__(self, name, type_, default=None):
#         self.name = name
#         self.type = type_
#         self.default = default if default else type_()
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа {}".format(self.type))
#         setattr(instance, self.name, value)
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
#
# class Simple():
#     somename = TypedProperty("somename", str)
#     num = TypedProperty("num", int, 42)
#
# f = Simple()
# f.somename = "vasya"
#
#
# class RevealAccess(object):
#     """Дескриптор данных, который устанавливает и возвращает значения,
#        и печатает сообщение о том, что к атрибуту был доступ.
#     """
#     def __init__(self, initval=None, name='var'):
#         self.val = initval
#         self.name = name
#     def __get__(self, obj, objtype):
#         print('Получаю', self.name)
#         print('obj', obj)
#         print('objtype', objtype)
#         return self.val
#     def __set__(self, obj, val):
#         print('Обновляю', self.name)
#         print('obj', obj)
#         self.val = val
#
#
#
# class MyClass(object):
#     x = RevealAccess(10, 'var "x"')
#     y = 5
