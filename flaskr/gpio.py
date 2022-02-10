import lgpio
import time

def run_pwm(PIN = 12, FREQ = 1000):
    h = lgpio.gpiochip_open(0)

    while True:
        lgpio.tx_pwm(h, PIN, FREQ, 50)
        time.sleep(3)
        break
    lgpio.gpiochip_close(h)
