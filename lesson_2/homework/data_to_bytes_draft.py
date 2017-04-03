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

PACKET_HEADER = bytes([122, 122])
SWITCH_ON = bytes([0])
SWITCH_OFF = bytes([1])
REBOOT = bytes([2])
SENSOR_ACTIVATION = bytes([3])
ENCASHMENT_BLOCK = bytes([4])
PAYMENT_TRANSACTION = bytes([1])
ENCASHMENT = bytes([2])

year = 2017 - 2000
month = 4
day = 1
seconds = 800

bitstring_date_time = "{0:07b}{0:04b}{0:05b}{0:024b}".format(year, month, day, seconds)


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


print(bitstring_to_bytes(bitstring_date_time))
