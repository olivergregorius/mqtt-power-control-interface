from types import Device, WifiSettings, MQTTSettings

# Misc
led_pin = 'LED'

# Wifi settings
wifi_ssid = 'SSID'
wifi_passphrase = 'abcdef'
wifi_settings = WifiSettings(wifi_ssid, wifi_passphrase)

# MQTT settings
mqtt_host = 'mqtt.example.org'
mqtt_port = 1883
mqtt_user = 'power-control'
mqtt_password = 'fedcba'
mqtt_topic_power_control = b'powercontrol/control'
mqtt_topic_power_status = b'powercontrol/status'
mqtt_settings = MQTTSettings(mqtt_host, mqtt_port, mqtt_user, mqtt_password, mqtt_topic_power_control, mqtt_topic_power_status)

# Controlled devices
devices = [
    Device('device1', 2, 3)
]
