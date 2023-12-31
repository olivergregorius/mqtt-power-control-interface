from umqtt import simple
import utime


class MQTTClient(simple.MQTTClient):
    def safe_connect(self):
        while True:
            try:
                super().disconnect()
            except:
                pass
            try:
                return super().connect()
            except OSError:
                utime.sleep(2)

    def publish(self, topic, msg: str):
        while True:
            try:
                return super().publish(topic, msg.encode())
            except OSError:
                pass
            self.safe_connect()

    def subscribe(self, topic):
        super().subscribe(topic)

    def set_callback(self, function):
        super().set_callback(function)

    def check_msg(self):
        try:
            super().check_msg()
        except OSError:
            self.safe_connect()
