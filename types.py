from machine import Pin


class WifiConfig:
    ssid: str
    passphrase: str

    def __init__(self, ssid, passphrase):
        self.ssid = ssid
        self.passphrase = passphrase


class MQTTConfig:
    host: str
    port: int
    username: str
    password: str
    topic_pwr_status: str
    topic_pwr_control: str

    def __init__(self, host, port, username, password, topic_pwr_status, topic_pwr_control):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic_pwr_status = topic_pwr_status
        self.topic_pwr_control = topic_pwr_control


class Device:
    name: str
    pwr_led_pin: Pin
    pwr_btn_pin: Pin

    def __init__(self, name, pwr_led_pin, pwr_btn_pin):
        self.name = name
        self.pwr_led_pin = Pin(pwr_led_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pwr_btn_pin = Pin(pwr_btn_pin, mode=Pin.OUT)
