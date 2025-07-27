import pickle
import numpy as np
import json
from flask import Flask, render_template, request, url_for
import os

# Initialize Flask app
app = Flask(__name__)

# Load the saved KNN model
with open('iris_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load accuracy data
with open('accuracy.json', 'r') as f:
    accuracy_data = json.load(f)

# File to log predictions
PREDICTION_LOG_FILE = 'prediction_log.json'

# Mapping from class index to species name and image filename
species_map = {
    0: {"name": "Setosa", "image": "setosa1.jpg"},
    1: {"name": "Versicolor", "image": "versicolour1.jpg"},
    2: {"name": "Virginica", "image": "virginica1.jpg"}
}

def load_prediction_log():
    if os.path.exists(PREDICTION_LOG_FILE):
        with open(PREDICTION_LOG_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def save_prediction_log(log):
    with open(PREDICTION_LOG_FILE, 'w') as f:
        json.dump(log, f)

def calculate_accuracy_over_time(log):
    accuracies = []
    correct_count = 0
    for i, entry in enumerate(log, 1):
        if entry['true_label'] == entry['predicted_label']:
            correct_count += 1
        accuracies.append(correct_count / i)
    return accuracies

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    confidence = None
    image_url = None
    accuracy = None
    accuracy_over_time = []

    if request.method == 'POST':
        try:
            # Get input from the user
            sepal_length = float(request.form['sepal_length'])
            sepal_width = float(request.form['sepal_width'])
            petal_length = float(request.form['petal_length'])
            petal_width = float(request.form['petal_width'])

            # Convert input to NumPy array
            features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

            # Get prediction and probability
            probabilities = model.predict_proba(features)[0]  # Get probability for each class
            class_index = np.argmax(probabilities)  # Get class with highest probability

            # Convert to species name and get image path
            prediction = species_map[class_index]["name"]
            image_filename = species_map[class_index]["image"]
            image_url = url_for('static', filename=image_filename)  # Correct way to serve static files
            confidence = round(probabilities[class_index] * 100, 2)  # Convert to percentage

            # Get accuracy from loaded data
            accuracy = accuracy_data.get("overall_accuracy", None)

            # For demonstration, assume true label is provided in form (optional)
            true_label_name = request.form.get('true_label')
            if true_label_name:
                true_label = None
                for key, val in species_map.items():
                    if val["name"].lower() == true_label_name.lower():
                        true_label = val["name"]
                        break
                if true_label:
                    # Load existing prediction log
                    log = load_prediction_log()
                    # Append current prediction
                    log.append({"true_label": true_label, "predicted_label": prediction})
                    # Save updated log
                    save_prediction_log(log)
                    # Calculate accuracy over time
                    accuracy_over_time = calculate_accuracy_over_time(log)

        except ValueError:
            prediction = "Invalid Input! Enter numbers only."
            confidence = None
            image_url = None
            accuracy = None
            accuracy_over_time = []

    return render_template('index.html', prediction=prediction, confidence=confidence, image_url=image_url, accuracy=accuracy, accuracy_over_time=accuracy_over_time)

if __name__ == '__main__':
    app.run(debug=True)
