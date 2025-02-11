from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import numpy as np

# Load pre-trained ML models
with open("trained_models.pkl", "rb") as f:
    models = pickle.load(f)

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Placement Prediction</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: auto; }
                .form-group { margin-bottom: 20px; }
                select, input[type=file], input[type=submit] { 
                    padding: 10px;
                    margin: 5px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Placement Prediction</h1>
                <form action="/predict" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="file">Upload CSV File:</label><br>
                        <input type="file" id="file" name="file" accept=".csv" required>
                    </div>
                    <div class="form-group">
                        <label for="process_needed">Data needs preprocessing?</label><br>
                        <select id="process_needed" name="process_needed">
                            <option value="yes">Yes</option>
                            <option value="no">No</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="model">Select Model:</label><br>
                        <select id="model" name="model">
                            <option value="logistic_regression">Logistic Regression</option>
                            <option value="svc">SVC</option>
                            <option value="random_forest">Random Forest</option>
                            <option value="stacking_classifier">Stacking Classifier</option>
                        </select>
                    </div>
                    <input type="submit" value="Predict">
                </form>
            </div>
        </body>
    </html>
    '''

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['file']
    process_needed = request.form.get("process_needed", "yes")
    model_name = request.form.get("model", "logistic_regression")
    
    df = pd.read_csv(file)
    if process_needed.lower() == "yes":
        df.drop(columns=['StudentID'], inplace=True, errors='ignore')
        
        label_encoders = {}
        categorical_columns = ['PlacementTraining', 'ExtracurricularActivities', 'PlacementStatus']
        for col in categorical_columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        
        scaler = MinMaxScaler()
        df[df.columns] = scaler.fit_transform(df[df.columns])
    
    if model_name in models:
        model = models[model_name]
        predictions = model.predict(df)
    else:
        return jsonify({"error": "Invalid model choice. Available models: " + ", ".join(models.keys())})
    
    df["Predictions"] = predictions
    df.to_csv("predictions.csv", index=False)
    return jsonify({"message": "Predictions saved as predictions.csv"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
