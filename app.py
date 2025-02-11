from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import numpy as np
import tensorflow as tf

# Load pre-trained ML models
with open("trained_models.pkl", "rb") as f:
    all_models = pickle.load(f)
    models = {
        k: v for k, v in all_models.items() 
        if k in ['logistic_regression', 'svc']
    }

# Load the deep learning model
best_model = tf.keras.models.load_model("best_model.h5")

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
                #result {
                    margin-top: 20px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    display: none;
                }
                .success { color: green; }
                .error { color: red; }
                .note { 
                    background-color: #fff3cd; 
                    padding: 10px; 
                    border-radius: 5px; 
                    margin-bottom: 20px; 
                }
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const form = document.querySelector('form');
                    const result = document.getElementById('result');
                    
                    form.onsubmit = async function(e) {
                        e.preventDefault();
                        
                        const formData = new FormData(form);
                        
                        try {
                            const response = await fetch('/predict', {
                                method: 'POST',
                                body: formData
                            });
                            
                            const data = await response.json();
                            result.style.display = 'block';
                            
                            if (data.error) {
                                result.className = 'error';
                                result.textContent = 'Error: ' + data.error;
                            } else {
                                result.className = 'success';
                                result.textContent = data.message;
                            }
                        } catch (error) {
                            result.style.display = 'block';
                            result.className = 'error';
                            result.textContent = 'Error: ' + error.message;
                        }
                    };
                });
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Placement Prediction</h1>
                <div class="note">
                    <strong>Note:</strong> Please upload preprocessed data (x_test.csv format) for predictions.
                </div>
                <form action="/predict" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="file">Upload Preprocessed CSV File:</label><br>
                        <input type="file" id="file" name="file" accept=".csv" required>
                    </div>
                    <div class="form-group">
                        <label for="model">Select Model:</label><br>
                        <select id="model" name="model">
                            <option value="logistic_regression">Logistic Regression</option>
                            <option value="svc">SVC</option>
                            <option value="deep_learning">Deep Learning Model</option>
                        </select>
                    </div>
                    <input type="submit" value="Predict">
                </form>
                <div id="result"></div>
            </div>
        </body>
    </html>
    '''

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"})
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"})
            
        model_name = request.form.get("model", "logistic_regression")
        
        # Read CSV file
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return jsonify({"error": f"Error reading CSV file: {str(e)}"})
        
        # Make predictions
        try:
            if model_name == "deep_learning":
                predictions = (best_model.predict(df) >= 0.5).astype(int).flatten()
                model_display_name = "deep_learning"
            elif model_name in models:
                model = models[model_name]
                predictions = model.predict(df)
                model_display_name = model_name
            else:
                available_models = list(models.keys()) + ["deep_learning"]
                return jsonify({"error": f"Invalid model choice. Available models: {', '.join(available_models)}"})
            
            # Save predictions with model name
            df["Predictions"] = predictions
            output_file = f"predictions_{model_display_name}.csv"
            df.to_csv(output_file, index=False)
            
            return jsonify({
                "success": True,
                "message": f"Predictions saved as {output_file}",
                "predictions": predictions.tolist()
            })
            
        except Exception as e:
            return jsonify({"error": f"Error during prediction: {str(e)}"})
            
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
