
from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load saved model and columns
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    predicted_price = None

    if request.method == 'POST':
        try:
            category = int(request.form['category'])
            area = int(request.form['area'])
            room_number = int(request.form['room_number'])
            repair = int(request.form['repair'])
            title_deed = int(request.form['title_deed'])
            region = request.form['region']

            # Create empty input dataframe with same columns as training data
            new_house = pd.DataFrame(0, index=[0], columns=columns)

            new_house['category'] = category
            new_house['area'] = area
            new_house['room_number'] = room_number
            new_house['repair'] = repair
            new_house['title_deed'] = title_deed

            region_col = f'region_{region}'
            if region_col in new_house.columns:
                new_house[region_col] = 1

            # Predict
            prediction = model.predict(new_house)[0]
            predicted_price = f"{prediction:,.0f} AZN"

        except Exception as e:
            predicted_price = f"Error: {str(e)}"

    return render_template('index.html', predicted_price=predicted_price)

if __name__ == '__main__':
    app.run(debug=True)