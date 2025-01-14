# Loan Risk Assessment
#-----------------------------------------------------------------------------
# Create a csv learning set for a risk level machine learning file
#-----------------------------------------------------------------------------
## More likely data
import pandas as pd # type: ignore
import numpy as np # type: ignore

#-----------------------------------------------------------------------------
# python for predicting
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.metrics import classification_report # type: ignore

# disable warnings
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

# Or if you are using > Python 3.11:
with warnings.catch_warnings(action="ignore"):
    fxn()
    
warnings.filterwarnings("ignore")

#print("Inside risk_Assessment.py code.")

# Load your dataset
csvPath = '/Users/joyce.johnson/Cdata/Camunda/data/code/creditRisk2.csv'
data = pd.read_csv(csvPath)
# need to drop NaN
data = data.dropna(axis=0)

# 'risk' is the target variable with values 'low', 'medium', 'high', 'dnl' for Do Not Lend

# Preprocessing
X = data[['creditScore', 'latePayments', 'monthsJob', 'dtiRatio', 'loanAmt', 'liquidAssets', 'numCC']]
y = data['creditRisk']

# Encoding target variable
y = y.map({'low': 0, 'medium': 1, 'high': 2, 'dnl': 3})

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.17, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

### Training the Logistic Regression Model
# Training the model
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

#print("Prediction Model built and ready for input.")

### Creating the Prediction Function
# Finally, create a function that takes in the inputs (credit score, mortgage payment, DTI ratio, 
# annual salary) and outputs the risk category.

#print("Defining the predict_risk function.")
def predict_risk(creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC):
    input_data = [[creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC]]
    input_data = scaler.transform(input_data)  # Apply the same scaling
    prediction = model.predict(input_data)
    risk_map = {0: 'low', 1: 'medium', 2: 'high', 3: 'dnl'}
    return risk_map[prediction[0]]



from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    creditScore = int(request.form['credit_score'])
    numCC = int(request.form['credit_cards'])
    latePayments = int(request.form['late_payments'])
    monthsJob = int(request.form['months_position'])
    dtiRatio = float(request.form['debt_income_ratio'])
    loanAmt = float(request.form['loan_amount'])
    liquidAssets = float(request.form['liquid_assets'])
    
    # Calculate the result
    result = predict_risk(creditScore, latePayments, monthsJob, dtiRatio, loanAmt, liquidAssets, numCC)
    
    # Send result back to the page
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

