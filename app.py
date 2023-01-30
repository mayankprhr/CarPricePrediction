from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('xgb_model_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    fuel_Diesel=0
    fuel_CNG=0
    
    seller_type_Dealer=0
    
    owner_Second_Owner=0
    owner_Second_Owner=0
    owner_Third_Owner=0
    owner_Test_Drive_Car=0
    
    transmission_Automatic=0
    transmission_Manual=0
    
    if request.method == 'POST':
        year = int(request.form['year'])
        # Present_Price=float(request.form['Present_Price'])
        km_driven=int(request.form['km_driven'])
        km_driven2=np.log(km_driven)
        
        owner_First_Owner=request.form['owner_First_Owner']
        if(owner_First_Owner=='First Owner'):
            owner_First_Owner=1
            owner_Second_Owner=0
            owner_Second_Owner=0
            owner_Third_Owner=0
            owner_Test_Drive_Car=0
        elif(owner_First_Owner=='Second Owner'):
            owner_First_Owner=0
            owner_Second_Owner=1
            owner_Second_Owner=0
            owner_Third_Owner=0
            owner_Test_Drive_Car=0        
        elif(owner_First_Owner=='Third Owner'):
            owner_First_Owner=0
            owner_Second_Owner=0
            owner_Second_Owner=0
            owner_Third_Owner=1
            owner_Test_Drive_Car=0        
        elif(owner_First_Owner=='Test Drive Owner'):
            owner_First_Owner=0
            owner_Second_Owner=0
            owner_Second_Owner=0
            owner_Third_Owner=0
            owner_Test_Drive_Car=1
        else:
            owner_First_Owner=0
            owner_Second_Owner=0
            owner_Second_Owner=0
            owner_Third_Owner=0
            owner_Test_Drive_Car=0
            
            
        fuel_Petrol=request.form['fuel_Petrol']
        if(fuel_Petrol=='Petrol'):
            fuel_Petrol=1
            fuel_Diesel=0
            fuel_CNG=0
            
        elif(fuel_Petrol=='Diesel'):
            fuel_Petrol=0
            fuel_Diesel=1
            fuel_CNG=0
        elif(fuel_Petrol=='CNG'):
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_CNG=1
        else:
            fuel_Petrol=0
            fuel_Diesel=0
            fuel_CNG=0
        
        year=2023-year
        
        seller_type_Individual=request.form['seller_type_Individual']
        if(seller_type_Individual=='Individual'):
            seller_type_Individual=1
            seller_type_Dealer=0
        elif(seller_type_Individual=='Dealer'):
            seller_type_Individual=0
            seller_type_Dealer=1
        else:
            seller_type_Individual=0
            seller_type_Dealer=0
            
            	
        transmission_manual=request.form['transmission_Manual']
        if(transmission_manual=='Manual'):
            transmission_manual=1
        else:
            transmission_manual=0
            
        seats=int(request.form['seats'])
        seats2=np.log(seats)
        
        engine=int(request.form['engine'])
        engine2=np.log(engine)
            
            
        prediction=model.predict([[year, km_driven,	engine,	seats, fuel_CNG, fuel_Diesel, fuel_Petrol, seller_type_Dealer, seller_type_Individual,	transmission_Manual, owner_First_Owner,	owner_Second_Owner,	owner_Test_Drive_Car, owner_Third_Owner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at Rs. {} Lakhs".format(output))
    else:
        return render_template('index1.html')

if __name__=="__main__":
    app.run(debug=True)


