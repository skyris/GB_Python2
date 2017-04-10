import json
import socket
import struct
import datetime

PACKET_HEADER = b'zz'
SERVICE_MAINTENANCE = b'\x00'
SWITCH_ON_CODE = b'\x00'
SWITCH_OFF_CODE = b'\x01'
REBOOT_CODE = b'\x02'
SENSOR_ACTIVATION_CODE = b'\x03'
ENCASHMENT_BLOCK_CODE = b'\x04'
PAYMENT_TRANSACTION_CODE = b'\x01'
ENCASHMENT_CODE = b'\x02'

HOST, PORT = 'localhost', 9999


class Config():
    def __init__(self, path):
        self._path = path

    def load(self):
        with open(self._path) as handle:
            config_dict = json.load(handle)
            for name, val in config_dict.items():
                setattr(self, name, val)
            print("config loaded")

    def save(self):
        with open(self._path, "w") as handle:
            config_dict = dict(self.__dict__)
            config_dict.pop("_path", None)
            json.dump(config_dict, handle, sort_keys=True, indent=4)
        print("config saved")


def handle_event(event, config):
    if event[0] == "service":
        binary_data = make_service_maintenance(event)
    elif event[0] == "transaction":
        binary_data = make_payment_transaction(event)
    elif event[0] == "encashment":
        binary_data = make_encashment(event)
    else:
        raise ValueError("unrecognized event")
    message = create_message(binary_data, config)
    return message


def make_service_maintenance(event):
    if event[1] == "switch_on":
        suffix = SWITCH_ON_CODE
    elif event[1] == "switch_off":
        suffix = SWITCH_OFF_CODE
    elif event[1] == "reboot":
        suffix = REBOOT_CODE
    elif event[1] == "encashment_block":
        suffix = ENCASHMENT_BLOCK_CODE
    elif event[1] == "sensor":
        if event[2] == 1:
            suffix = SENSOR_ACTIVATION_CODE + b'\x01'
        elif event[2] == 2:
            suffix = SENSOR_ACTIVATION_CODE + b'\x02'
        else:
            raise ValueError("unrecognized sensor")
    else:
        raise ValueError("unrecognized sub event")
    return SERVICE_MAINTENANCE + suffix


def make_payment_transaction(event):
    # Encode organization id and money in kopecks to bytes
    return PAYMENT_TRANSACTION_CODE + struct.pack(">lq", event[1], event[2])


def make_encashment(event):
    # Encode encashment id and money in kopecks to bytes
    return ENCASHMENT_CODE + struct.pack(">lq", event[1], event[2])


def create_message(transaction_data_b, configuration):
    configuration.transaction_id += 1
    term_and_trans_ids_b = struct.pack(">hl", configuration.terminal_id, configuration.transaction_id)
    time_b = encode_unixtime()
    pack_len_b = struct.pack(">h", len(time_b + term_and_trans_ids_b + transaction_data_b))
    print(PACKET_HEADER + pack_len_b + time_b + term_and_trans_ids_b + transaction_data_b)
    return PACKET_HEADER + pack_len_b + time_b + term_and_trans_ids_b + transaction_data_b


def encode_unixtime(date_time=None):
    # 4 bytes
    if not date_time:
        date_time = datetime.datetime.now()
    unixtimestamp = struct.pack(">l", int(date_time.timestamp()))
    return unixtimestamp


def decode_unixtime(data):
    return datetime.datetime.fromtimestamp(data)


def connect(message):
    global HOST, PORT
    print("Client started")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(message)
    sock.close()
    print("Closed")


"""
def encode_transaction():
    return b""


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


def _make_service_maintenance(type_of_service):
    date_time = encode_datetime()
    return PACKET_HEADER + date_time + PAYMENT_TRANSACTION_CODE + type_of_service


def _make_payment_transaction(organisation_id, summ):
    date_time = encode_datetime()
    bitstring = "{0:032b}{1:064b}".format(organisation_id, summ)
    transaction_data = bitstring_to_bytes(bitstring)
    return PACKET_HEADER + date_time + PAYMENT_TRANSACTION_CODE + transaction_data


def _make_encashment(operator_id, summ):
    date_time = encode_datetime()
    bitstring = "{0:032b}{1:064b}".format(operator_id, summ)
    transaction_data = bitstring_to_bytes(bitstring)
    return PACKET_HEADER + date_time + ENCASHMENT_CODE + transaction_data


"""
