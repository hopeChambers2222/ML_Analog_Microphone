import joblib
import serial
import numpy as np
from sklearn.preprocessing import StandardScaler
import time

# Set up serial
COM_PORT = 'COM14'
BAUD_RATE = 9600
# Open the serial port
ser = serial.Serial(COM_PORT, BAUD_RATE)

materials = {0: 'Red', 1:'Green',  2:'Yellow',  3:'Temperature'}

# Load the trained model from the file
loaded_model = joblib.load('FInal_Machine_Learning/trained_model_audio.pkl')
print("START")

def clean_data(input):
    # Replace square brackets and commas with an empty string
    cleaned_string = input.replace('[', '').replace(']', '').replace(',', '')
    return cleaned_string

def calculate_statistics(array):
    #variance = np.var(array)
    skewness = np.mean((array - np.mean(array))**3) / np.power(np.var(array), 3/2)
    kurtosis = np.mean((array - np.mean(array))**4) / np.power(np.var(array), 2) - 3
    #mean = np.mean(array)
    #median = np.median(array)
    std_deviation = np.std(array)

    return [(skewness, kurtosis, std_deviation)]

try:
    while True:
        
        sample = ser.readline().decode('utf-8').strip()
        #time.sleep(0.5)
        #print(f"Sample reading {sample}")
        
        # Convert the sample string to an array of float values
        sample_array = np.array([int(clean_data(val)) for val in sample.split(',') if val.strip()])

        
        #print(f"Sample reading size {len(sample_array)}")
        
        # Reshape the array to match the expected input shape of the model
        sample_array = sample_array  # Assuming the model expects a single sample
        #print(f"Reshaped Array {sample_array}")

        
        #print(f"Reshaped Array {sample_array}")

        # Predict the material using the loaded model
        predict = loaded_model.predict(calculate_statistics(sample_array))
        print(f" You Said: {materials[predict[0]]}")
        string = str(predict[0]) #
        ser.write(string.encode())
       
        
        
except KeyboardInterrupt:
    print("GOOD-BYE")
    ser.close()