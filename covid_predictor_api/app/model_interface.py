import numpy as np
from app.preprocessing import preprocess_input_data
import joblib
import os


# Here we would implement the logic to get the prediction
# and import necessary model or logic.

# importing the model
model = joblib.load(os.path.join(os.path.dirname(__file__), "..", "model", "best_model.pkl"))
    
# Defining the prediction function that calls the model
def get_prediction(features: list) -> str:
    """
    Function to get prediction based on patient data.
    """
    data_dict = features
    processed_data = preprocess_input_data(data_dict)
    
    # numpy array for model input because the model expects a 2D array
    input_array = np.array(processed_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return "Yes" if prediction[0] == 1 else "No"