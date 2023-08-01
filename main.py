import utime

from mqtt import MQTTClient
from settings import devices, mqtt_settings
from types import Device


def msg_callback(topic, msg):
    global triggered_devices
    msg_str = msg.decode()
    print(f'Received message: {msg_str}')
    matching_device = [device for device in devices if device.name == msg_str]
    if not matching_device:
        print(f'No matching device with name {msg_str} could be found')
        return
    triggered_devices.extend(matching_device)


def push_pwr_button(device: Device) -> None:
    print(f'Pushing power button for device {device.name}')
    device.pwr_btn_pin.value(1)
    utime.sleep_ms(500)
    device.pwr_btn_pin.value(0)


mqtt = MQTTClient(client_id=mqtt_settings.username, server=mqtt_settings.host, port=mqtt_settings.port, user=mqtt_settings.username, password=mqtt_settings.password)
mqtt.set_callback(msg_callback)
mqtt.safe_connect()
mqtt.subscribe(mqtt_settings.topic_pwr_control)
triggered_devices = []
iterations = 0

# main
while True:
    try:
        iterations += 1
        mqtt.check_msg()
        while triggered_devices:
            push_pwr_button(triggered_devices.pop())
        if iterations > 4:
            for device in devices:
                pwr_state = 1 if device.pwr_led_pin.value() == 0 else 0
                print(f'Determined power state for device {device.name}: {pwr_state}')
                mqtt.publish(topic=mqtt_settings.topic_pwr_status, msg=f'{{"name": "{device.name}", "pwrState": "{pwr_state}"}}')
                iterations = 0
        utime.sleep(1)
    except:
        pass
