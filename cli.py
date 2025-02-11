import pandas as pd
import pickle
import numpy as np
import tensorflow as tf
import os
import time

def load_models():
    print("Loading models... ⏳")
    with open("trained_models.pkl", "rb") as f:
        all_models = pickle.load(f)
        models = {k: v for k, v in all_models.items() if k in ['logistic_regression', 'svc']}
    deep_model = tf.keras.models.load_model("best_model.h5")
    print("Models loaded successfully ✅")
    return models, deep_model

def preprocess_input(df):
    if 'ExtracurricularActivities' in df.columns:
        df['ExtracurricularActivities'] = df['ExtracurricularActivities'].map({'Yes': 1, 'No': 0})
    if 'PlacementTraining' in df.columns:
        df['PlacementTraining'] = df['PlacementTraining'].map({'Yes': 1, 'No': 0})
    return (df - df.min()) / (df.max() - df.min())

def get_valid_input(prompt, is_float=True):
    while True:
        value = input(prompt)
        if is_float:
            try:
                return float(value)
            except ValueError:
                print("⚠️ Invalid input! Please enter a numeric value.")
        else:
            if value.lower() in ["yes", "no"]:
                return 1 if value.lower() == "yes" else 0
            print("⚠️ Invalid input! Please enter 'Yes' or 'No'.")

def predict_single(models, deep_model):
    print("\n🔍 Enter student details for placement prediction:")
    features = {
        'CGPA': True, 'Internships': True, 'Projects': True, 
        'Workshops/Certifications': True, 'AptitudeTestScore': True, 
        'SoftSkillsRating': True, 'ExtracurricularActivities': False, 
        'PlacementTraining': False, 'SSC_Marks': True, 'HSC_Marks': True
    }
    
    user_input = {feature: get_valid_input(f"{feature}: ", is_float) for feature, is_float in features.items()}
    
    df = pd.DataFrame([user_input])
    df = preprocess_input(df)

    model_choice = input("\n🤖 Choose model (logistic_regression, svc, deep_learning): ").strip().lower()
    
    if model_choice == "deep_learning":
        print("Running prediction... 🧠")
        time.sleep(1)
        prediction = (deep_model.predict(df) >= 0.5).astype(int).flatten()[0]
    elif model_choice in models:
        print("Running prediction... 📊")
        time.sleep(1)
        prediction = models[model_choice].predict(df)[0]
    else:
        print("❌ Invalid model choice! Try again.")
        return

    print("\n🎯 Prediction Result: ", "✅ Placed" if prediction else "❌ Not Placed")

def predict_from_csv(models, deep_model):
    file_path = input("\n📂 Enter the CSV file path: ").strip()
    
    if not os.path.exists(file_path):
        print("❌ File not found! Please check the path and try again.")
        return
    
    df = pd.read_csv(file_path)
    df = preprocess_input(df)

    model_choice = input("\n🤖 Choose model (logistic_regression, svc, deep_learning): ").strip().lower()

    print("\n📊 Running batch predictions...")
    time.sleep(1)
    
    if model_choice == "deep_learning":
        predictions = (deep_model.predict(df) >= 0.5).astype(int).flatten()
    elif model_choice in models:
        predictions = models[model_choice].predict(df)
    else:
        print("❌ Invalid model choice! Try again.")
        return
    
    df['Predictions'] = predictions
    output_file = f"predictions_{model_choice}.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Predictions saved successfully as '{output_file}'!")

def main():
    models, deep_model = load_models()
    
    while True:
        print("\n📌 Placement Prediction CLI")
        print("1️⃣ Predict for a single student")
        print("2️⃣ Predict from a CSV file")
        print("3️⃣ Exit")

        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            predict_single(models, deep_model)
        elif choice == '2':
            predict_from_csv(models, deep_model)
        elif choice == '3':
            print("\n👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
