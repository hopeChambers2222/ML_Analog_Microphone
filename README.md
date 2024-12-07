## Sensing Systems Project

**Coded by**: Hope M Chambers  
**Date**: May 2024  
**Project Description**: This project involves the development of a sensing system that captures audio samples, processes them using machine learning models, and controls an RGB LED based on the input received. Building a voice activation system using machine learning. The system will use your voice to turn on a led, and read and display the current temperature. 

**Demo Link** [[Analog Microphone Machine Learning Project]](https://youtu.be/rLVGm9qQUQo)

### Components Used
- Microcontroller: Raspberry Pi Pico
- Microphone: Analog Sound Sensor
- RGB LED: Common Anode RGB LED
- Temperature Sensor: LM35
- Display: TM1637 Quad 7-Segment LED Display
- Button: Active Low button

### Code Overview

#### FInal_Machine_Learning\pico files\main.py
- **Audio Sampling**: The program captures audio samples from the microphone using the `capture_audio` function. It reads a specified number of samples and returns their sum.
- **LED Control**: An `RGBLED` class is defined to control the RGB LED. It allows setting the LED color based on RGB values.
- **Main Loop**: The `main` function continuously checks for button presses. When the button is pressed, it sums audio samples and reads color IDs from serial input. It then maps the color ID to a color name and sets the LED color accordingly.

#### FInal_Machine_Learning\Predicting_Audio_From_Serial.py
- **Data Cleaning**: The data received from the serial port is cleaned to remove square brackets and commas.
- **Feature Extraction**: Audio samples are processed to calculate statistics such as skewness, kurtosis, and standard deviation.
- **Model Prediction**: The trained machine learning model predicts the material based on the extracted features.
- **Serial Communication**: The predicted material is sent back to the microcontroller via serial communication.


### File Structure
- **FInal_Machine_Learning\pico files\main.py**: Contains code for the sensing system.
- **FInal_Machine_Learning\pico files\tm1637.py**: Library for Display
- **FInal_Machine_Learning\pico files\Collecting_Audio_Data.py**: Optional software to collect your own data for training
- **FInal_Machine_Learning\Predicting_Audio_From_Serial.py**: Contains code for machine learning model prediction.
- **FInal_Machine_Learning\trained_model_audio.pkl**: Serialized machine learning model.
- **FInal_Machine_Learning\samples\volume_arrays.csv.txt**: Training audio data
- **FInal_Machine_Learning\ML_Model_Arrays.ipynb**: Jupeter Notebook for Machine Learning Training. 
- **README.md**: Project documentation.

### Instructions for Use
1. Connect the Raspberry Pi Pico to the microphone, button, LM35, 7 segment display and RGB LED.
2. Upload the `main.py` and `tm1637` code to the Pico.
3. Connect the Pico to the computer via USB.
4. Run the `Predicting_Audio_From_Serial.py` script on the computer.
5. Press the button on the Pico to capture audio samples and control the LED color.

### Training New Data
1. Connect the Raspberry Pi Pico to the microphone, button, LM35, 7 segment display and RGB LED.
2. Open `Collecting_Audio_Data.py`
3. Change line 79 `data.append('Word,', samples)` Word to the word you will be saying.
4. Run code, click button, say word, repeat for 60 seconds
5. Copy printed arrays into the `volume_arrays.csv.txt` file
6. Repeat steps 3-5 for all colors and temperature. 
7. Note: if training new words do not forget to go through other files and update dictonary information.  

### Additional Notes
- Make sure to install the required libraries before running the scripts.
- Adjust the COM port and baud rate in the `Predicting_Audio_From_Serial.py` script according to your setup.
- Experiment with different machine learning models and features for better prediction accuracy.
