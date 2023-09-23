import gc

import machine
import micropython_ota
import ntptime
import ujson
import usys
import utime
from micropython_loki import Loki, LogLevel
from uio import StringIO

from config import led_pin, ntp_config, ota_config, mqtt_config, loki_config, devices
from mqtt import MQTTClient
from types import Device

check_msg_interval_seconds = 1
state_report_interval_seconds = 5

pin_led = machine.Pin(led_pin, machine.Pin.OUT)
ntptime.host = ntp_config.host


# Signals:
# Start: 5, 100, 100
# OTA update: 3, 500, 200
def blink(count: int, on_duration_ms=1000, off_duration_ms=1000) -> None:
    pin_led.off()
    for i in range(count):
        pin_led.on()
        utime.sleep_ms(on_duration_ms)
        pin_led.off()
        utime.sleep_ms(off_duration_ms)


def ntp_update(current_time: int) -> None:
    global last_ntp_update
    attempts = 0
    while attempts < ntp_config.update_attempts:
        attempts += 1
        try:
            ntptime.settime()
        except Exception as e:
            loki.log('Error synchronizing with time server, performing reset...', LogLevel.ERROR)
            stacktrace = StringIO()
            usys.print_exception(e, stacktrace)
            loki.log(f'ntp_update: {stacktrace.getvalue()}', LogLevel.ERROR)
            push_logs(current_time)
            machine.reset()
        if ntp_config.lower_bound < utime.time() < ntp_config.upper_bound:
            last_ntp_update = current_time
            return
    loki.log(f'Error synchronizing with time server, current time {utime.time()}, performing reset...', LogLevel.ERROR)
    push_logs(current_time)
    machine.reset()


def push_logs(current_time: int) -> None:
    global last_loki_push_logs
    last_loki_push_logs = current_time
    loki.push_logs()


def msg_callback(topic, msg):
    global triggered_devices
    msg_json = ujson.loads(msg.decode())
    loki.log(f'Received message: {msg_json}')
    device_name = msg_json['deviceName']
    matching_device = [device for device in devices if device.name == device_name]
    if not matching_device:
        loki.log(f'No matching device with name {device_name} could be found')
        return
    triggered_devices.extend(matching_device)


def push_pwr_button(device: Device) -> None:
    loki.log(f'Pushing power button for device {device.name}')
    device.pwr_btn_pin.value(1)
    utime.sleep_ms(500)
    device.pwr_btn_pin.value(0)


# main
blink(5, 100, 100)
current_time = utime.time()
last_state_report = current_time
last_loki_push_logs = 0
last_ota_update = current_time
last_ntp_update = current_time
loki = Loki(loki_config.url, loki_config.labels, max_stack_size=loki_config.max_stack_size, min_push_log_level=loki_config.min_push_log_level)
loki.log('Starting mqtt-power-control-interface')
mqtt = MQTTClient(client_id=mqtt_config.username, server=mqtt_config.host, port=mqtt_config.port, user=mqtt_config.username, password=mqtt_config.password)
mqtt.set_callback(msg_callback)
mqtt.safe_connect()
mqtt.subscribe(mqtt_config.topic_pwr_control)
triggered_devices = []
while True:
    try:
        current_time = utime.time()

        mqtt.check_msg()
        while triggered_devices:
            push_pwr_button(triggered_devices.pop())

        if current_time % state_report_interval_seconds == 0 or current_time >= last_state_report + state_report_interval_seconds:
            for device in devices:
                pwr_state = 'running' if device.pwr_led_pin.value() == 0 else 'stopped'
                loki.log(f'Determined power state for device {device.name}: {pwr_state}', LogLevel.DEBUG)
                mqtt.publish(topic=mqtt_config.topic_pwr_state, msg=f'{{"deviceName": "{device.name}", "state": "{pwr_state}"}}')
            last_state_report = current_time

        if current_time > last_ota_update + ota_config.interval_s:
            blink(3, 500, 200)
            loki.log('Checking for OTA update')
            last_ota_update = current_time
            micropython_ota.check_for_ota_update(ota_config.url, ota_config.project, soft_reset_device=True)
            gc.collect()

        if current_time > last_ntp_update + ntp_config.update_interval_s:
            ntp_update(current_time)

        if current_time > last_loki_push_logs + loki_config.push_interval_s:
            push_logs(current_time)

        utime.sleep(1)
    except KeyboardInterrupt:
        exit(1)
    except Exception as e:
        stacktrace = StringIO()
        usys.print_exception(e, stacktrace)
        loki.log(f'main.py: {stacktrace.getvalue()}', LogLevel.ERROR)
        push_logs(current_time)
