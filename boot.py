import machine
import mip
import network
import utime
from settings import wifi_settings, led_pin


pin_led = machine.Pin(led_pin, machine.Pin.OUT)


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
        print(f'Connecting to Wifi {wifi_settings.ssid}')
        interface.active(True)
        interface.connect(wifi_settings.ssid, wifi_settings.passphrase)
        while not interface.isconnected():
            pass
    print(f'Connected to Wifi {wifi_settings.ssid}, connection information:')
    print(interface.ifconfig())
    blink(pin_led, 3, 500, 500)


def install_packages() -> None:
    mip.install('umqtt.simple')


blink(pin_led, 3, 200, 200)
wifi_connect()
install_packages()
