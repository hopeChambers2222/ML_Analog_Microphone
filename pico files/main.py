'''
Coded by : Hope M Chambers
May 2024
Applications of Sensing Systems
'''

import uasyncio
from machine import Pin, ADC, PWM
import utime
import uselect
from sys import stdin
import tm1637

# Define constants for audio sampling
SAMPLE_RATE = 441000  # Audio sampling rate in Hz
NUM_SAMPLES = 75  # Number of samples to capture in each frame


materials = {0: 'red', 1:'green',  2:'yellow', 3:'temperature'}

class LM35:
    def __init__(self, pin):
        self.LM35_pin = ADC(Pin(pin))
        self.read_val = 0
        self.farenheit = 0
        self.celsius = 0

    # Get raw value of the sensor
    def measure(self):   
        read_val = self.LM35_pin.read_u16()

        # Conversion factor
        conversion = 3.3 / 65535
        
        # Convert back to voltage
        volt = read_val * conversion
    
        # Celsius
        self.celsius = volt / (12.0 / 1000)


    def get_temperature(self):
        
        return self.celsius
'''
Define a class RGBLED to control the RGB LED
    - Initialize the pins for red, green, and blue colors
    - Define methods to set the LED color and intensity
'''
class RGBLED:
    def __init__(self, pin_red, pin_green, pin_blue):
        self.off = 1000000
        self.red = PWM(Pin(pin_red), freq=1000, duty_ns=self.off)
        self.green = PWM(Pin(pin_green), freq=1000, duty_ns=self.off)
        self.blue = PWM(Pin(pin_blue), freq=1000, duty_ns=self.off)
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
    
    def off(self):
        self.red.duty_ns(self.off)
        self.green.duty_ns(self.off)
        self.blue.duty_ns(self.off)
        
    def color_on(self, color):
        RGB = self.rainbow[color]
        for i, primary in enumerate(self.RGB_PWM):
            ratio = RGB[i]
            if ratio == 0:
                self.light_off(primary)
            else:
                self.light_on(primary, ratio)

# Define sensors
led = RGBLED(pin_red=2, pin_green=3, pin_blue=4)
lm_35= LM35(26)
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
mic = ADC(Pin(28))

'''
Define an asynchronous function 'capture_audio' to capture audio samples
    - Read audio samples from the microphone for a specified duration
    - Return the total sum of audio samples
'''
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
            await uasyncio.sleep_ms(int(100 / SAMPLE_RATE))  # Delay to maintain sample rate

        data.append(samples)
        volume += samples
    print(data)     

'''
Check if the button is pressed
        - If pressed, call the 'sum_readings' function to sum audio samples
        - Check for any input from stdin (serial input)
        - If there's input, read the color ID
        - Map the color ID to a color name using the 'materials' dictionary
        - Set the LED color based on the mapped color name
'''
async def main():
    while True:
        if button.value() == 0:
            await sum_readings()
            #select_result = uselect.select([stdin], [], [], 0)
            color_id = int(stdin.read(1))  # Read the color ID from serial
            color_name = materials.get(color_id, 'off')  # Get color name from materials dictionary
            
            if color_id != 3:
                led.color_on(color_name)  # Display the color on the LED
            else:
                led.color_on('off')
                lm_35.measure()
                tm.temperature(int(lm_35.get_temperature()))
              

        await uasyncio.sleep_ms(100)
uasyncio.run(main())
