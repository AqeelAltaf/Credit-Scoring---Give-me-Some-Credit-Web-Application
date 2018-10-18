# importing flask libraries
import os
from flask import Flask,request,render_template,redirect, url_for,flash, request

# this line is to start the flassk app 
app = Flask(__name__)
import pandas as pd
import re
import pickle 


##  this route is our Home route where we will have our landing page

@app.route('/', methods=['GET','POST'])

##  this function will run if any one hit the "/" URL
def hello():
    #Rendering the HTML
    render_template("landing_page.html")
    #If anyone PRESS THE button he will be redirect to review   
    if request.method == 'POST':
        return redirect(url_for('review'))
    return render_template("landing_page.html")


#Route for Review page showing 
@app.route('/getdata',methods=['GET','POST'])
##  this function will run if any one hit the "/review" URL
def review():
    #below code is same as you sent me it will be run if any one hit the review URL
    # values = [0.7,0.8,9120,45,0,6]
    values = ['','','','','','']

    if request.method == "POST":
        values[0] = float(request.form['ruul'])
        values[1] = float(request.form['debt-ratio'])
        values[2] = float(request.form['monthly-income'])
        values[3] = float(request.form['age'])
        values[4] = float(request.form['not90dl'])
        values[5] = float(request.form['nrell'])
        
        
        if request.form['submit'] == 'knn':
            to_pred = pd.Series(values[0:5])
            pred = knn_model.predict(to_pred)
        elif request.form['submit'] == 'rf':
            to_pred = pd.Series(values[0:5])
            pred = rf_model.predict(to_pred)

        else:
            to_pred = pd.Series([values[0],values[1],values[4],values[5]]).reshape(1,4)
            pred =gbc_model.predict(to_pred)

        return render_template("getdata.html",pred=pred,value=values,lab='Prediction for this Data is: ')
    else:
        return render_template("getdata.html",pred='',value=values,lab='')


##  this is dummy route just for showing message thsat this page is not found 
@app.route('/<name>')
def hello_name(name):
    return "Sorry {} does not exist!".format(name)

##  this is where the application runs
if __name__ == '__main__':
        
    # Loading the saved KNN model pickle
    knn_pkl = open('knn_gmsc.pkl', 'rb')
    knn_model = pickle.load(knn_pkl)

       
    # Loading the saved GBC model pickle
    gbc_pkl = open('gbc_gmsc.pkl', 'rb')
    gbc_model = pickle.load(gbc_pkl)
       
    # Loading the saved RFS model pickle
    rf_pkl = open('rf_gmsc.pkl', 'rb')
    rf_model = pickle.load(rf_pkl)
    app.run()