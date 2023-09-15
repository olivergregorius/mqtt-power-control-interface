import machine
import micropython_ota
import mip
import network
import ntptime
import uos
import utime

from config import led_pin, wifi_config, ntp_config, ota_config

micropython_ota_version = '2.1.0'
micropython_loki_version = '1.1.1'

pin_led = machine.Pin(led_pin, machine.Pin.OUT)
ntptime.host = ntp_config.host


# Signals:
# Bootup: 3, 200, 200
# Wifi connection: 3, 500, 500
def blink(led: machine.Pin, count: int, on_duration_ms=1000, off_duration_ms=1000) -> None:
    led.off()
    for i in range(count):
        led.on()
        utime.sleep_ms(on_duration_ms)
        led.off()
        utime.sleep_ms(off_duration_ms)


def wifi_connect() -> None:
    interface = network.WLAN(network.STA_IF)
    if not interface.isconnected():
        print(f'Connecting to Wifi {wifi_config.ssid}')
        interface.active(True)
        interface.connect(wifi_config.ssid, wifi_config.passphrase)
        attempts = 0
        while not interface.isconnected() and attempts < wifi_config.connect_retries_max:
            attempts += 1
            utime.sleep(wifi_config.connect_retry_wait_s)
        if not interface.isconnected():
            print(f'Failed connecting to Wifi {wifi_config.ssid}, performing reset...')
            machine.reset()
    print(f'Connected to Wifi {wifi_config.ssid}, connection information:')
    print(interface.ifconfig())
    blink(pin_led, 3, 500, 500)


def ntp_update() -> None:
    attempts = 0
    while attempts < ntp_config.update_attempts:
        attempts += 1
        try:
            ntptime.settime()
        except Exception:
            print(f'Error synchronizing with time server, performing reset...')
            machine.reset()
        if ntp_config.lower_bound < utime.time() < ntp_config.upper_bound:
            return
    machine.reset()


def install_package(package_name: str, version: str) -> None:
    update = False
    if f'{package_name}.version' not in uos.listdir():
        update = True
    else:
        with open(f'{package_name}.version', 'r', encoding='utf-8') as version_file:
            if version_file.read().strip() != version:
                update = True
    if update:
        mip.install(f'https://github.com/olivergregorius/{package_name}/releases/download/v{version}/{package_name}.mpy')
        with open(f'{package_name}.version', 'w', encoding='utf-8') as version_file:
            version_file.write(f'{version}')
        machine.reset()


def install_packages() -> None:
    install_package('micropython_ota', micropython_ota_version)
    install_package('micropython_loki', micropython_loki_version)
    mip.install('umqtt.simple')


blink(pin_led, 3, 200, 200)
wifi_connect()
ntp_update()
install_packages()
micropython_ota.ota_update(ota_config.url, ota_config.project, ota_config.files)
