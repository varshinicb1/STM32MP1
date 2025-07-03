import numpy as np
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def detect_anomaly(temp, gas):
    # Adjust input shape as per the model's requirement
    input_data = np.array([[temp, gas]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    # Use a threshold suitable for your use case
    return bool(output[0] > 0.5)
