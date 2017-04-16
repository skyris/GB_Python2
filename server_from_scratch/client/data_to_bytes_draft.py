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
"""
import datetime

PACKET_HEADER = bytes([122, 122])
SERVICE_CODE = bytes([0])
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

# for 5 bytes version---------------------------------------------
bytestrint = b'zz"\x83\x013i\x01N\x00\x00\x00\x00\x00\x00\x07\xd1'
if bytestrint[:2] == b"zz":
    bin_date = "".join(bin(byte)[2:].zfill(8) for byte in bytestrint[2:4])
    bin_time = "".join(bin(byte)[2:].zfill(8) for byte in bytestrint[4:7])
    year = int(bin_date[:7], 2)
    mounth = int(bin_date[7:11], 2)
    day = int(bin_date[11:], 2)
    seconds_since_midnight = int(bin_time, 2)
# -----------------------------------------------------------------


# for 4 bytes version---------------------------------------------
bytestrint = b''


def get_time_from_bytes(utime):
    if bytestrint[:2] == b"zz":
        unixtime = int("".join(bin(byte)[2:].zfill(8) for byte in utime), 2)
        return datetime.datetime.fromtimestamp(unixtime)

# -----------------------------------------------------------------
(17<<9)|(4<<5)|(3&31)
# Нам нужно записать год в 7 первых бит, 2**7 == 128 (от 2000 до 2127)
# месяц в 4 следующих бита, 2**4 == 16 (от 1 до 12)
# день в следующие 5 бит 2**5 = 32 (от 1 до 31)
# вся дата должна уложиться в 2 байта, те двоичное число от 00000000 00000000 до 11111111 11111111 от (0 до 65025)
year = 2017 - 2000 # 17
bin(17) == '0b10001'
это число надо сдвинуть в сторону старших битов на (16 - 7) 9 бит
(17<<9)
'0b10001000000000'
в это же число добавляем месяц, поставив его после года и перед днем. Те сдвигаем на 5 бит
bin(4) '0b100'
(17<<9) | (4<<5)
'0b10001010000000'

"{0:07b}{0:04b}{0:05b}".format(17, 4, 3)
"""

i = 0

try:
    while True:
        print(i)
        i += 1
except KeyboardInterrupt:
    print("exit")
