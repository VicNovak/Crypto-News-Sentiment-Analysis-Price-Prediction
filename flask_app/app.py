from flask import Flask, render_template, request, jsonify
import pandas as pd
import keras
import pickle

app = Flask(__name__)

@app.route('/')
def input_form():
    return render_template('index.html')

def preprocess_input_data(input_data):
    # Загрузка scaler из файла
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Масштабирование признаков
    X_scaled = scaler.transform(input_data)

    return X_scaled

@app.route('/predict', methods=['POST'])
def get_prediction():
    sentiment = int(request.form['sentiment'])
    btc_pct_after_15m = float(request.form['btc_pct_after_15m'])
    btc_pct_after_30m = float(request.form['btc_pct_after_30m'])
    open_price = float(request.form['open_price'])
    high_price = float(request.form['high_price'])
    low_price = float(request.form['low_price'])
    close_price = float(request.form['close_price'])

    input_data = pd.DataFrame({
        'Sentiment': [sentiment],
        'btc_pct_after_15m':[btc_pct_after_15m],
        'btc_pct_after_30m':[btc_pct_after_30m],
        'open_price': [open_price],
        'high_price': [high_price],
        'low_price': [low_price],
        'close_price': [close_price]
    })

    preprocessed_data = preprocess_input_data(input_data)
    model = keras.models.load_model("trained_mlp.h5")
    prediction = model.predict(preprocessed_data)
    print(prediction)
    
    decision = "Buy" if prediction[0][0] > 0.6 else "Sell"

    return jsonify({"Prediction": decision})

if __name__ == '__main__':
    app.run(debug=True)

