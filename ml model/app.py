from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('house_prediction.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Raw form inputs
    area = request.form['Area_Type']
    city = request.form['City']
    furnish = request.form['Furnishing_Status']
    tenant = request.form['Tenant_Preferred']
    contact = request.form['Point_of_Contact']
    print(request)

    # Manually create one-hot encoded structure
    input_data = {
        'BHK': int(request.form['BHK']),
        'Size': float(request.form['Size']),
        'Bathroom': int(request.form['Bathroom']),
        'Current Floor': float(request.form['Current_Floor']),
        'Total Floors': float(request.form['Total_Floors']),
        'Area Type_Carpet Area': area == 'Carpet Area',
        'Area Type_Super Area': area == 'Super Area',
        'City_Chennai': city == 'Chennai',
        'City_Delhi': city == 'Delhi',
        'City_Hyderabad': city == 'Hyderabad',
        'City_Kolkata': city == 'Kolkata',
        'City_Mumbai': city == 'Mumbai',
        'Furnishing Status_Semi-Furnished': furnish == 'Semi-Furnished',
        'Furnishing Status_Unfurnished': furnish == 'Unfurnished',
        'Tenant Preferred_Bachelors/Family': tenant == 'Bachelors/Family',
        'Tenant Preferred_Family': tenant == 'Family',
        'Point of Contact_Contact Builder': contact == 'Contact Builder',
        'Point of Contact_Contact Owner': contact == 'Contact Owner'
    }

    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    prediction=round(prediction,2)
    return str(prediction)
if __name__ == '__main__':
    app.run(debug=True)