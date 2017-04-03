import socket
import datetime

PACKET_HEADER = bytes([122, 122])
SERVICE_MAINTENANCE = bytes([0])
SWITCH_ON_CODE = bytes([0])
SWITCH_OFF_CODE = bytes([1])
REBOOT_CODE = bytes([2])
SENSOR_ACTIVATION_CODE = bytes([3])
ENCASHMENT_BLOCK_CODE = bytes([4])
PAYMENT_TRANSACTION_CODE = bytes([1])
ENCASHMENT_CODE = bytes([2])

HOST, PORT = 'localhost', 9999


def create_message():
    massage = PACKET_HEADER + encode_datetime()


def encode_unixtime(date_time=None):
    # 4 bytes
    if not date_time:
        date_time = datetime.datetime.now()
    unixtimestamp = int(date_time.timestamp())
    return (unixtimestamp).to_bytes(4, byteorder='big')


def decode_unixtime(data):
    return datetime.datetime.fromtimestamp(data)


def encode_datetime(date_time=None):
    # 5 bytes
    if not date_time:
        date_time = datetime.datetime.now()
    year = date_time.year - 2000
    month = date_time.month
    day = date_time.day
    seconds_since_midnight = int(
        (date_time - date_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    bitstring_date_time = "{0:07b}{1:04b}{2:05b}{3:024b}".format(year, month, day, seconds_since_midnight)
    return bitstring_to_bytes(bitstring_date_time)


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def make_service_maintenance(type_of_service):
    date_time = encode_datetime()
    return PACKET_HEADER + date_time + PAYMENT_TRANSACTION_CODE + type_of_service


def make_payment_transaction(organisation_id, summ):
    date_time = encode_datetime()
    bitstring = "{0:032b}{1:064b}".format(organisation_id, summ)
    transaction_data = bitstring_to_bytes(bitstring)
    return PACKET_HEADER + date_time + PAYMENT_TRANSACTION_CODE + transaction_data


def make_encashment(operator_id, summ):
    date_time = encode_datetime()
    bitstring = "{0:032b}{1:064b}".format(operator_id, summ)
    transaction_data = bitstring_to_bytes(bitstring)
    return PACKET_HEADER + date_time + ENCASHMENT_CODE + transaction_data


message = make_payment_transaction(78, 2001)

print("Client started")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(message)
sock.close()
print("the end")
