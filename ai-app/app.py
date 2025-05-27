import pickle
from flask import Flask, request, jsonify
import pandas as pd

# Khởi tạo app Flask
app = Flask(__name__)

# Load mô hình từ file .pkl
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return "Linear Regression Prediction API is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy dữ liệu JSON đầu vào
        data = request.get_json()
        
        df = pd.DataFrame([data])

        # Dự đoán
        prediction = model.predict(df)
        result = prediction[0]

        return jsonify({'prediction': result})

    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
