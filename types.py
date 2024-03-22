from machine import Pin
from micropython_loki import LogLevel


class WifiConfig:
    ssid: str
    passphrase: str
    connect_retries_max: int
    connect_retry_wait_s: int

    def __init__(self, ssid, passphrase, connect_retries_max, connect_retry_wait_s):
        self.ssid = ssid
        self.passphrase = passphrase
        self.connect_retries_max = connect_retries_max
        self.connect_retry_wait_s = connect_retry_wait_s


class NTPConfig:
    host: str
    update_attempts: int
    update_interval_s: int
    lower_bound: int
    upper_bound: int

    def __init__(self, host, update_attempts, update_interval_s, lower_bound, upper_bound):
        self.host = host
        self.update_attempts = update_attempts
        self.update_interval_s = update_interval_s
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


class OTAConfig:
    url: str
    project: str
    files: list
    interval_s: int

    def __init__(self, url, project, files, interval_s):
        self.url = url
        self.project = project
        self.files = files
        self.interval_s = interval_s


class MQTTConfig:
    host: str
    port: int
    client_id: str
    username: str
    password: str
    topic_pwr_state: str
    topic_pwr_control: str

    def __init__(self, host, port, client_id, username, password, topic_pwr_state, topic_pwr_control):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.topic_pwr_state = topic_pwr_state
        self.topic_pwr_control = topic_pwr_control


class LokiConfig:
    url: str
    labels: list
    push_interval_s: int
    max_stack_size: int
    min_push_log_level: LogLevel

    def __init__(self, url, labels, push_interval_s, max_stack_size, min_push_log_level):
        self.url = url
        self.labels = labels
        self.push_interval_s = push_interval_s
        self.max_stack_size = max_stack_size
        self.min_push_log_level = min_push_log_level


class Device:
    name: str
    pwr_led_pin: Pin
    pwr_btn_pin: Pin

    def __init__(self, name, pwr_led_pin, pwr_btn_pin):
        self.name = name
        self.pwr_led_pin = Pin(pwr_led_pin, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pwr_btn_pin = Pin(pwr_btn_pin, mode=Pin.OUT)
