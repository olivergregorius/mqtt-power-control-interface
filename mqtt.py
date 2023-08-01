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
                return super().connect(False)
            except OSError:
                utime.sleep(2)

    def publish(self, topic, msg: str):
        while True:
            try:
                return super().publish(topic, msg.encode(), retain=False, qos=1)
            except OSError:
                pass
            self.safe_connect()

    def subscribe(self, topic):
        super().subscribe(topic)

    def set_callback(self, function):
        super().set_callback(function)

    def check_msg(self):
        super().check_msg()
