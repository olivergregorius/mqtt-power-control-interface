from types import WifiConfig, NTPConfig, OTAConfig, MQTTConfig, LokiConfig, Device
from micropython_loki import LogLabel, LogLevel
import utils

# Misc
led_pin = 'LED'

# Wifi settings
wifi_ssid = 'SSID'
wifi_passphrase = 'abcdef'
connect_retries_max = 10
connect_retry_wait_s = 3
wifi_config = WifiConfig(wifi_ssid, wifi_passphrase, connect_retries_max, connect_retry_wait_s)

# NTP config
ntp_host = '0.pool.ntp.org'
ntp_update_attempts = 3
ntp_update_interval_seconds = 3600
ntp_time_lower_bound = 1672531200  # 2023-01-01T00:00:00Z
ntp_time_upper_bound = 1893455999  # 2029-12-31T23:59:59Z
ntp_config = NTPConfig(ntp_host, ntp_update_attempts, ntp_update_interval_seconds, ntp_time_lower_bound, ntp_time_upper_bound)

# OTA config
ota_url = 'https://ota.example.org'
ota_project = 'mqtt-power-control-interface'
ota_files = ['boot.py', 'main.py', 'mqtt.py', 'config.py', 'types.py', 'utils.py']
ota_interval_s = 300
ota_config = OTAConfig(ota_url, ota_project, ota_files, ota_interval_s)

# MQTT config
mqtt_host = 'mqtt.example.org'
mqtt_port = 1883
mqtt_user = 'power-control'
mqtt_password = 'fedcba'
mqtt_topic_power_state = b'powercontrol/state'
mqtt_topic_power_control = b'powercontrol/control'
mqtt_config = MQTTConfig(mqtt_host, mqtt_port, mqtt_user, mqtt_password, mqtt_topic_power_state, mqtt_topic_power_control)

# Loki config
loki_url = 'https://loki.example.org'
loki_labels = [
    LogLabel('device', 'Raspberry Pi Pico W'),
    LogLabel('app', 'mqtt-power-control-interface'),
    LogLabel('version', utils.get_version())
]
loki_push_logs_interval_s = 30
loki_max_stack_size = 10
loki_min_push_log_level = LogLevel.INFO
loki_config = LokiConfig(loki_url, loki_labels, loki_push_logs_interval_s, loki_max_stack_size, loki_min_push_log_level)

# Controlled devices - Each device is declared as: Device(<deviceName>, <power state input pin>, <power control output pin>)
devices = [
    Device('device1', 2, 3)
]
