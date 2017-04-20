import datetime
import socketserver
import struct
import db

HOST, PORT = 'localhost', 9999
PACKET_HEADER = b'zz'
SERVICE_MAINTENANCE = 0
SWITCH_ON_CODE = 0
SWITCH_OFF_CODE = 1
REBOOT_CODE = 2
SENSOR_ACTIVATION_CODE = 3
ENCASHMENT_BLOCK_CODE = 4
PAYMENT_TRANSACTION_CODE = 1
ENCASHMENT_CODE = 2


class TCPserver(socketserver.TCPServer):
    pass


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Handled")
        self.data = self.request.recv(1024)
        if self.data[:2] == b"zz":
            length = struct.unpack(">h", self.data[2:4])[0]
            if length == len(self.data) - 4:
                self.parse_packet()
            else:
                write_to_log(self.data)
        else:
            write_to_log(self.data)
        print("End of connection")

    def parse_packet(self):
        unixtime, self.terminal_id, self.transaction_id, transaction_type = struct.unpack(">lhlb", self.data[4:15])
        self.date_time = datetime.datetime.fromtimestamp(unixtime)
        if transaction_type == SERVICE_MAINTENANCE:
            event_text = self.parse_service_message()
            db.add_service(date_time=self.date_time, terminal_id=self.terminal_id,
                           transaction_id=self.transaction_id, event_type=event_text)
        elif transaction_type == PAYMENT_TRANSACTION_CODE:
            partner_id, summ = struct.unpack(">lq", self.data[15:])
            db.add_payment(date_time=self.date_time, terminal_id=self.terminal_id,
                           transaction_id=self.transaction_id, partner_id=partner_id, summ=summ)
        elif transaction_type == ENCASHMENT_CODE:
            accumulator_id, summ = struct.unpack(">lq", self.data[15:])
            db.add_encashment(date_time=self.date_time, terminal_id=self.terminal_id,
                              transaction_id=self.transaction_id, accumulator_id=accumulator_id, summ=summ)
        else:
            raise ValueError("unrecognized transaction code")

    def parse_service_message(self):
        event_type = self.data[15]
        if event_type == SWITCH_ON_CODE:
            event_text = "switch_on"
        elif event_type == SWITCH_OFF_CODE:
            event_text = "switch_off"
        elif event_type == REBOOT_CODE:
            event_text = "reboot"
        elif event_type == SENSOR_ACTIVATION_CODE:
            event_text = "sensor " + str(self.data[16])
        elif event_type == ENCASHMENT_BLOCK_CODE:
            event_text = "encashment_block"
        else:
            raise ValueError("unrecognized service subcode")

        return event_text


def write_to_log(data):
    pass


try:
    server = TCPserver((HOST, PORT), RequestHandler)
    print("Server started")
    server.serve_forever()
except KeyboardInterrupt:  # control-C
    print("exit")
