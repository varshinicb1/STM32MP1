import numpy as np
import tflite_runtime.interpreter as tflite

# Load your trained TensorFlow Lite model
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def detect_anomaly(temp, gas):
    input_data = np.array([[temp, gas]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    return bool(output[0] > 0.5)
