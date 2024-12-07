import uasyncio
from machine import Pin, ADC, PWM
import utime
import uselect
from sys import stdin

button = Pin(22, Pin.IN, Pin.PULL_DOWN)
mic = ADC(Pin(28))
# Define constants for audio sampling
SAMPLE_RATE = 441000  # Audio sampling rate in Hz
NUM_SAMPLES = 75  # Number of samples to capture in each frame


materials = {0: 'red', 1:'green',  2:'yellow',  3:'temperature'}

class RGBLED:
    def __init__(self, pin_red, pin_green, pin_blue, off=1000000):
        self.off = off
        self.red = PWM(Pin(pin_red), freq=1000, duty_ns=off)
        self.green = PWM(Pin(pin_green), freq=1000, duty_ns=off)
        self.blue = PWM(Pin(pin_blue), freq=1000, duty_ns=off)
        self.RGB_PWM = (self.red, self.green, self.blue)
        self.rainbow = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'orange': (255, 165, 0),
            'yellow': (185, 255, 0),
            'purple': (128, 0, 128),
            'off': (0, 0, 0)
        }
    
    def get_duty_from_RGB(self, val):
        return round(((255 - val) / 255) * 65535)

    def light_on(self, color, ratio):
        color.duty_u16(self.get_duty_from_RGB(ratio))

    def light_off(self, color):
        color.duty_ns(self.off)

    def color_on(self, color):
        RGB = self.rainbow[color]
        for i, primary in enumerate(self.RGB_PWM):
            ratio = RGB[i]
            if ratio == 0:
                self.light_off(primary)
            else:
                self.light_on(primary, ratio)


led = RGBLED(pin_red=2, pin_green=3, pin_blue=4)

async def capture_audio():
    samples = 0
    for _ in range(NUM_SAMPLES):
        sample = mic.read_u16()
        samples += sample
        await uasyncio.sleep_ms(int(1000 / SAMPLE_RATE))  # Delay to maintain sample rate

    return samples

'''
Define an asynchronous function 'sum_readings' to sum audio samples over time
    - Continuously read audio samples and sum them for a specified duration
    - Print the summed data
'''
async def sum_readings():
    volume = 0
    start_time = utime.ticks_ms()
    data = []
    while utime.ticks_diff(utime.ticks_ms(), start_time) < 1500:
        samples = 0
        for _ in range(NUM_SAMPLES):
            sample = mic.read_u16()
            samples += sample
            await uasyncio.sleep_ms(int(1000 / SAMPLE_RATE))  # Delay to maintain sample rate

        data.append('Word,', samples)
        volume += samples
    print(data)     
    
async def main():
    while True:
        if button.value() == 0:
            await sum_readings()
                         

        await uasyncio.sleep_ms(100)
        



uasyncio.run(main())

        
        