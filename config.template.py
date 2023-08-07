from types import Device, WifiConfig, MQTTConfig

# Misc
led_pin = 'LED'

# Wifi settings
wifi_ssid = 'SSID'
wifi_passphrase = 'abcdef'
wifi_config = WifiConfig(wifi_ssid, wifi_passphrase)

# MQTT settings
mqtt_host = 'mqtt.example.org'
mqtt_port = 1883
mqtt_user = 'power-control'
mqtt_password = 'fedcba'
mqtt_topic_power_state = b'powercontrol/state'
mqtt_topic_power_control = b'powercontrol/control'
mqtt_config = MQTTConfig(mqtt_host, mqtt_port, mqtt_user, mqtt_password, mqtt_topic_power_state, mqtt_topic_power_control)

# Controlled devices - Each device is declared as: Device(<deviceName>, <power state input pin>, <power control output pin>)
devices = [
    Device('device1', 2, 3)
]
