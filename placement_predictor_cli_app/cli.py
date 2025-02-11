import pandas as pd
import tensorflow as tf
import os
import time

def load_model():
    print("Loading deep learning model... ⏳")
    deep_model = tf.keras.models.load_model("models/best_model.h5")
    print("Model loaded successfully ✅")
    return deep_model

def preprocess_input(df):
    if 'ExtracurricularActivities' in df.columns:
        df['ExtracurricularActivities'] = df['ExtracurricularActivities'].map({'Yes': 1, 'No': 0})
    if 'PlacementTraining' in df.columns:
        df['PlacementTraining'] = df['PlacementTraining'].map({'Yes': 1, 'No': 0})
    return (df - df.min()) / (df.max() - df.min())

def get_valid_input(prompt, is_float=True, example=""):
    while True:
        value = input(f"{prompt} (Example: {example}): ").strip()
        if is_float:
            try:
                return float(value)
            except ValueError:
                print("⚠️ Invalid input! Please enter a numeric value.")
        else:
            if value.lower() in ["yes", "no"]:
                return 1 if value.lower() == "yes" else 0
            print("⚠️ Invalid input! Please enter 'Yes' or 'No'.")

def predict_single(deep_model):
    print("\n🔍 Enter student details for placement prediction:")
    features = {
        'CGPA': (True, "8.5"), 
        'Internships': (True, "1"), 
        'Projects': (True, "3"), 
        'Workshops/Certifications': (True, "2"), 
        'AptitudeTestScore': (True, "85"), 
        'SoftSkillsRating': (True, "4.5"), 
        'ExtracurricularActivities': (False, "Yes/No"), 
        'PlacementTraining': (False, "Yes/No"), 
        'SSC_Marks': (True, "85"), 
        'HSC_Marks': (True, "80")
    }
    
    user_input = {feature: get_valid_input(feature, is_float, example) for feature, (is_float, example) in features.items()}
    
    df = pd.DataFrame([user_input])
    df = preprocess_input(df)

    print("Running prediction... 🧠")
    time.sleep(1)
    prediction = (deep_model.predict(df) >= 0.5).astype(int).flatten()[0]

    print("\n🎯 Prediction Result: ", "✅ Placed" if prediction else "❌ Not Placed")

def predict_from_csv(deep_model):
    file_path = input("\n📂 Enter the CSV file path: ").strip()
    
    if not os.path.exists(file_path):
        print("❌ File not found! Please check the path and try again.")
        return
    
    df = pd.read_csv(file_path)
    
    # Drop 'StudentID' if it exists
    if 'StudentID' in df.columns:
        df.drop(columns=['StudentID'], inplace=True)
    
    df = preprocess_input(df)

    print("\n📊 Running batch predictions...")
    time.sleep(1)

    predictions = (deep_model.predict(df) >= 0.5).astype(int).flatten()
    
    # Load original file again to keep StudentID in output
    df_output = pd.read_csv(file_path)
    df_output['Predictions'] = predictions

    # Ensure the 'predictions' folder exists
    os.makedirs("predictions", exist_ok=True)

    output_file = "predictions/predictions_deep_learning.csv"
    df_output.to_csv(output_file, index=False)
    
    print(f"\n✅ Predictions saved successfully as '{output_file}'!")

def main():
    deep_model = load_model()
    
    while True:
        print("\n📌 Placement Prediction CLI")
        print("1️⃣ Predict for a single student")
        print("2️⃣ Predict from a CSV file")
        print("3️⃣ Exit")

        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            predict_single(deep_model)
        elif choice == '2':
            predict_from_csv(deep_model)
        elif choice == '3':
            print("\n👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
