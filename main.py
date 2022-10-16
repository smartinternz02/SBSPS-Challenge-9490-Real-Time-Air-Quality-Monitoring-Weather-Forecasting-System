from copyreg import pickle
from flask import Flask, request, render_template
import pandas as pd
import requests

# Flask constructor
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def submit():
	if request.method == "POST":
		city = request.form.get("CITY")
		pm2 = request.form.get("PM2.5")
		pm10 = request.form.get("PM10")
		no = request.form.get("NO")
		no2 = request.form.get("NO2")
		nox = request.form.get("NOx")
		nh3 = request.form.get("NH3")
		co = request.form.get("CO")
		so2 = request.form.get("SO2")
		o3 = request.form.get("O3")
		benz = request.form.get("BENZENE")
		toul = request.form.get("TOULENE")
		xyl = request.form.get("XYLENE")

		API_KEY = "nBgFH1X8-vTgXCetSWFduXxaymgHu-ZdiMZTU45Ojnz3"
		token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
		API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
		mltoken = token_response.json()["access_token"]

		header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

		payload_scoring = {"input_data": [{"field": [['City','PM2.5','PM10','NO','NO2''NOx','NH3','CO','SO3','O3','Benzene','Toluene','Xylene']], "values": [[city,pm2,pm10,no,no2,nox,nh3,co,so2,o3,benz,toul,xyl]]}]}

		response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/397c6a38-0393-4d72-8a4a-c7a8e962e9a9/predictions?version=2022-10-16', json=payload_scoring,
		headers={'Authorization': 'Bearer ' + mltoken})
		print("Scoring response")
		predictions=response_scoring.json()
		pred=predictions['predictions'][0]['values'][0][0]
		pred=str(pred)
		return "Your Air Quality Index is " + pred
	else:
		return render_template("index.html")

if __name__=='__main__':
	app.run()
