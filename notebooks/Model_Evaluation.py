import pandas as pd
from Model_Training import fit_classifiers, evaluate_classifiers
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

#Load the data
X_train = pd.read_csv("../data/splitted_data/X_train.csv")
X_test = pd.read_csv("../data/splitted_data/X_test.csv")
y_train = pd.read_csv("../data/splitted_data/y_train.csv")['Reinfection']
y_test = pd.read_csv("../data/splitted_data/y_test.csv")['Reinfection']

#Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
fitted_models = fit_classifiers(X_train_scaled, y_train)

# Evaluate models
evaluation_df = evaluate_classifiers(fitted_models, X_test_scaled, y_test)

# Show results
print("\n Final Comparison:\n")
print(evaluation_df)

# Save the best performing model
joblib.dump(fitted_models["Decision Tree"], "../models/best_model.pkl")

