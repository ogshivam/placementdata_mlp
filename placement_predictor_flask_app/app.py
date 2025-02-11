from flask import Flask, request, render_template, jsonify
import pandas as pd
import tensorflow as tf
import os
import time

app = Flask(__name__)

# Load model at startup
print("Loading deep learning model... ⏳")
try:
    model = tf.keras.models.load_model("models/best_model.h5")
    print("Model loaded successfully ✅")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_input(df):
    if 'ExtracurricularActivities' in df.columns:
        df['ExtracurricularActivities'] = df['ExtracurricularActivities'].map({'Yes': 1, 'No': 0})
    if 'PlacementTraining' in df.columns:
        df['PlacementTraining'] = df['PlacementTraining'].map({'Yes': 1, 'No': 0})
    return (df - df.min()) / (df.max() - df.min())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        if not file.filename.endswith('.csv'):
            return jsonify({
                'success': False,
                'error': 'Please upload a CSV file'
            }), 400

        # Save uploaded file temporarily
        temp_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(temp_path)

        # Read and preprocess data
        df = pd.read_csv(temp_path)

        # Store StudentID if present
        student_ids = None
        if 'StudentID' in df.columns:
            student_ids = df['StudentID']
            df.drop(columns=['StudentID'], inplace=True)

        # Preprocess and predict
        df_processed = preprocess_input(df)
        predictions = (model.predict(df_processed) >= 0.5).astype(int).flatten()
        probabilities = model.predict(df_processed).flatten()

        # Prepare output DataFrame
        df_output = pd.DataFrame()
        if student_ids is not None:
            df_output['StudentID'] = student_ids
        df_output['Prediction'] = ['Placed' if p else 'Not Placed' for p in predictions]
        df_output['Probability'] = probabilities

        # Save predictions
        os.makedirs('predictions', exist_ok=True)
        output_path = os.path.join('predictions', f'predictions_{int(time.time())}.csv')
        df_output.to_csv(output_path, index=False)

        # Clean up
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'message': f'Predictions saved as {output_path}',
            'predictions': df_output.to_dict('records')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Create HTML template
@app.route('/create_template')
def create_template():
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Placement Prediction</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .prediction-result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .success { background-color: #d4edda; }
        .failure { background-color: #f8d7da; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">Placement Prediction System</h1>

        <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item">
                <a class="nav-link active" id="batch-tab" data-bs-toggle="tab" href="#batch" role="tab">Batch Prediction</a>
            </li>
        </ul>

        <div class="tab-content mt-3">
            <div class="tab-pane fade show active" id="batch" role="tabpanel">
                <form id="batchPredictionForm">
                    <div class="mb-3">
                        <label>Upload CSV File</label>
                        <input type="file" class="form-control" name="file" accept=".csv" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Predict</button>
                </form>
                <div id="batchResult"></div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('batchPredictionForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            try {
                const response = await fetch('/predict_batch', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    const resultDiv = document.getElementById('batchResult');
                    resultDiv.innerHTML = `
                        <div class="prediction-result success">
                            <h4>Predictions Complete!</h4>
                            <p>${result.message}</p>
                            <p>Total predictions: ${result.predictions.length}</p>
                        </div>
                    `;
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error making predictions: ' + error);
            }
        };
    </script>
</body>
</html>
    """

    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w') as f:
        f.write(html_content)
    return "Template created successfully!"

if __name__ == '__main__':
    # Create template on startup
    with app.test_client() as client:
        client.get('/create_template')

    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('predictions', exist_ok=True)

    # Run the app
    app.run(host='0.0.0.0', port=5002, debug=True)
