import utime
import ujson

from mqtt import MQTTClient
from config import devices, mqtt_config
from types import Device


def msg_callback(topic, msg):
    global triggered_devices
    msg_json = ujson.loads(msg.decode())
    print(f'Received message: {msg_json}')
    device_name = msg_json['deviceName']
    matching_device = [device for device in devices if device.name == device_name]
    if not matching_device:
        print(f'No matching device with name {device_name} could be found')
        return
    triggered_devices.extend(matching_device)


def push_pwr_button(device: Device) -> None:
    print(f'Pushing power button for device {device.name}')
    device.pwr_btn_pin.value(1)
    utime.sleep_ms(500)
    device.pwr_btn_pin.value(0)


mqtt = MQTTClient(client_id=mqtt_config.username, server=mqtt_config.host, port=mqtt_config.port, user=mqtt_config.username, password=mqtt_config.password)
mqtt.set_callback(msg_callback)
mqtt.safe_connect()
mqtt.subscribe(mqtt_config.topic_pwr_control)
triggered_devices = []
iterations = 0
print('Started mqtt-power-control-interface')

# main
while True:
    try:
        iterations += 1
        mqtt.check_msg()
        while triggered_devices:
            push_pwr_button(triggered_devices.pop())
        if iterations > 4:
            for device in devices:
                pwr_state = 'running' if device.pwr_led_pin.value() == 0 else 'stopped'
                print(f'Determined power state for device {device.name}: {pwr_state}')
                mqtt.publish(topic=mqtt_config.topic_pwr_status, msg=f'{{"deviceName": "{device.name}", "status": "{pwr_state}"}}')
                iterations = 0
        utime.sleep(1)
    except KeyboardInterrupt:
        exit(1)
    except:
        pass
