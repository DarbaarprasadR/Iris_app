import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import json

# Load the Iris dataset
from sklearn.datasets import load_iris
iris = load_iris()

# Create a DataFrame from the dataset
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df["species"] = iris.target  # Target values (0, 1, 2)

# Split data into training and testing sets
X = df.iloc[:, :-1]  # Features (Sepal/Petal Length & Width)
y = df["species"]    # Target (Species)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Save the trained model as 'iris_model.pkl'
with open("iris_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save accuracy to a JSON file
accuracy_data = {
    "overall_accuracy": accuracy
}

with open("accuracy.json", "w") as f:
    json.dump(accuracy_data, f)

print("✅ Model training complete! Saved as 'iris_model.pkl' and accuracy saved as 'accuracy.json'")
