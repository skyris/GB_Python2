import random
import time
from simple_client import *

"""
* Заголовок пакета: 2 байта 0x7A7A ('zz' по таблице ASCII)
        * Длина пакета: длина поля "дата-время" + длина поля "Транзакция"
        * Дата-время:
            * дата в 2 байта:
|7 бит: год-2000
|4 бита: месяц
|5 бит: число
|
            Так, дата 2017.04.01 будет закодирована 2 байтами: 0x2281 (в двоичном виде: 0010001010000001)
            * количество секунд в течение дня от 00:00:00, записана в 3 байта.

        * Транзакция состоит из 2-х полей - тип транзакции и данные:
            * Тип транзакции:
                * 0x00 - сервисная транзакция. bytes([0])
                      Данные:
                    * 0x00 - включение bytes([0])
                    * 0x01 - перезагрузка bytes([1])
                    * 0x02 - выключение bytes([2])
                    * 0x03 - активация датчика X bytes([3])
                    * 0x04 - блокировка, требуется инкассация bytes([4])
                * 0x01 - платёжная транзакция. bytes([1])
                      Данные:
                    * 4 байта: id организации для перевода средств
                    * 8 байт: сумма транзакции в копейках
                * 0x02 - инкассация. bytes([2])
                      Данные:
                    * 4 байта: id сотрудника-инкассатора
                    * 8 байт: сумма инкассации в копейках
"""
data_samples = [
    # ("service", "switch_on"),
    # ("service", "switch_off"),
    # ("service", "reboot"),
    # ("service", "sensor", 1),
    # ("service", "sensor", 2),
    # ("service", "encashment_block"),
    # ('transaction', 555, 200), ('transaction', 444, 300), ('transaction', 333, 150), ('transaction', 555, 500),
    # ('transaction', 333, 400), ('transaction', 444, 500), ('transaction', 555, 200), ('transaction', 222, 100),
    # ('transaction', 333, 200), ('transaction', 222, 300), ('transaction', 333, 400), ('transaction', 555, 150),
    # ('transaction', 222, 100), ('transaction', 222, 250), ('transaction', 333, 200), ('transaction', 111, 100),
    # ('transaction', 444, 300), ('transaction', 333, 400), ('transaction', 222, 300), ('transaction', 444, 300),
    # ('transaction', 222, 350), ('transaction', 111, 250), ('transaction', 444, 200), ('transaction', 444, 300),
    # ('transaction', 222, 150), ('transaction', 333, 500), ('transaction', 111, 400), ('transaction', 222, 500),
    # ('transaction', 333, 200), ('transaction', 111, 100), ('transaction', 555, 200), ('transaction', 555, 300),
    # ('transaction', 111, 400), ('transaction', 444, 150), ('transaction', 111, 100), ('transaction', 222, 250),
    # ('transaction', 555, 200), ('transaction', 555, 100), ('transaction', 222, 300), ('transaction', 111, 400),
    # ('transaction', 222, 300), ('transaction', 555, 300), ('transaction', 222, 350), ('transaction', 333, 250),
    ("encashment", 60, 150000)
]

path = "terminal_config.json"
config = Config(path)
config.load()
x = 0
while x < 50:
    time.sleep(random.random() * 1)
    current_event = random.choice(data_samples)
    print(current_event)
    message_ = handle_event(current_event, config)
    connect(message_)
    config.save()
    x += 1
