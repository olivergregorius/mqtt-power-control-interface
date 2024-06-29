from umqtt import simple
import utime

from config import mqtt_config


class MQTTClient(simple.MQTTClient):

    def safe_connect_and_subscribe(self):
        while True:
            try:
                super().disconnect()
            except:
                pass
            try:
                result = super().connect()
                self.subscribe(topic=mqtt_config.topic_pwr_control)
                return result
            except OSError:
                utime.sleep(2)

    def publish(self, topic, msg: str):
        while True:
            try:
                return super().publish(topic, msg.encode())
            except OSError:
                pass
            self.safe_connect_and_subscribe()

    def subscribe(self, topic):
        super().subscribe(topic)

    def set_callback(self, function):
        super().set_callback(function)

    def check_msg(self):
        try:
            super().check_msg()
        except OSError:
            self.safe_connect_and_subscribe()
