import pickle
import pandas as pd
import numpy as np
from flask import Flask,render_template,request
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.base")

from sklearn.preprocessing import OrdinalEncoder
le = OrdinalEncoder()

app = Flask(__name__)
# app.static_folder = 'images'
ccfd = pickle.load(open('ccfd.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict():
    # print('inside function')
    Card_Number = request.args.get('Card-Number')
    Card_Expiry = request.args.get('card-Expiry')
    Encode_employment = {
        "employed":1,
        "unemployed":2,
        "self-employed":3,
        "selfemployed":3
    }
    Employment = Encode_employment[request.args.get('employment')]
    Mobile_Number = request.args.get('mobile-number')
    Card_Limit = request.args.get('card-limit')
    Transaction_Amount = request.args.get('transaction-amount')
    Encode_card_verification = {
        "Online":1,
        "Offline":2
    }
    Card_Verification_Method = Encode_card_verification[request.args.get('card-verification')]                                                  
    Monthly_Income = int(request.args.get('monthly-income'))
    Annual_Income = int(request.args.get('annual-income'))
    Encode_is_foreign_transaction = {
        "true":1,
        "false":0
    }
    Is_Foreign_Transaction = Encode_is_foreign_transaction[request.args.get('foreign-transaction')]
    Transaction_Frequency_Weekday = int(request.args.get('transaction-frequency-weekday'))
    Transaction_Frequency_Weekend = int(request.args.get('transaction-frequency-weekend'))


    input_data = [[Card_Number,Card_Expiry,Employment,Mobile_Number,Card_Limit,Transaction_Amount,Card_Verification_Method,
                   Monthly_Income,Annual_Income,Is_Foreign_Transaction,Transaction_Frequency_Weekday,Transaction_Frequency_Weekend]]  # List of input values, complete with other features


    prediction = ccfd.predict(input_data)
    output = prediction[0]
    prediction_text = ''
    if output == 0:
        prediction_text = "This is not fraud."
    elif output == 1:
        prediction_text = "This is fraud."
    
    # print('result: ' + prediction_text)
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)