
    # importing modules
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
import bs4
import numpy as np
from flask import Flask, render_template,request,session,logging,url_for,redirect,flash
from flaskext.mysql import MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from passlib.hash import sha256_crypt
import pymysql
import routes
import pickle


engine =create_engine("mysql+pymysql://root:@localhost/register")

                    #(mysql+pymysql://username:password@localhost/databasename)

db=scoped_session(sessionmaker(bind=engine))


app=Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

#register form

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
            name=request.form.get("name")
            username=request.form.get("username")
            password=request.form.get("password")
            confirm=request.form.get("confirm")
            secure_password =sha256_crypt.encrypt(str(password))

            if password == confirm:
                db.execute("INSERT INTO users(name,username,password) VALUES(:name,:username,:password)",
                                                {"name":name,"username":username,"password":secure_password})
                db.commit()
                flash("you are register and can login","success")
                return redirect(url_for('login'))
            else:
                flash("password does not match","danger")
                return render_template("register.html")

    return render_template("register.html")

#login
@app.route('/login',methods=['GET','POST','DELETE'])
def login():
    if request.method =='POST':
        username=request.form.get("name")
        password=request.form.get("password")


        usernamedata= db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone ()
        passwordata=db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("no username", "danger")
            return render_template("login.html")
        else:
            for passwor_data in passwordata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"]=True

                    # flash ("you are now login","success")
                    return redirect(url_for('updates'))
                
                else:
                    flash("incorrect password","danger")
                    return render_template("login.html")
      


    return render_template("login.html")
#updates
@app.route("/updates")
def updates():
    
    #						Realtime analysis on corona virus

    # requesting data from website
    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)

        # parsing it to beautiful soup
    
    data = r.text
    soup = bs4.BeautifulSoup(data,'html.parser')
    live_data=soup.find_all(id='maincounter-wrap')

    # print(live_data)
    for i in live_data:
        ldata1=(live_data[0].get_text().strip("['Coronavirus Cases:'\n\n/["))
        ldata2=(live_data[1].get_text().strip("['Deaths:'\n\n"))
        ldata3=(live_data[2].get_text().strip("['Recovered:\n\n"))

        print('Analysis based on individual countries')
    print()

    # Extracting table data
    table_body = soup.find('tbody')
    table_rows = table_body.find_all('tr')

    countries = []
    cases = []
    deaths = []
    recovered = []

    for tr in table_rows:
        td = tr.find_all('td')
        countries.append(td[1].text.strip())
        cases.append(td[2].text.strip())
        deaths.append(td[4].text.strip())
        recovered.append(td[6].text.strip())


    # indices = [i for i in range(1,len(countries)+1)]
    headers = ['Countries','Total Cases','Todays Deaths','Total Recovered']
    df = pd.DataFrame(list(zip(countries,cases,deaths,recovered)),columns=headers)
    # print(df)

    # Saving it to csv file
    df.to_csv('corona-virus-cases.csv')


    return render_template("updates.html", data1=[ldata1], data2=[ldata2], data3=[ldata3])

# open a file, where you stored the pickled data
file =open('model.pkl','rb')
clf =pickle.load(file) 
file.close()

@app.route('/index', methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        myDict=request.form
        age=int(myDict['age'])
        fever=int(myDict['fever'])
        pain=int(myDict['pain'])
        runnyNose=int(myDict['runnyNose'])
        diffBreath=int(myDict['diffBreath'])

        # Code for inference
        inputFeatures=[fever,pain,age,runnyNose,diffBreath]
        infProb=clf.predict_proba([inputFeatures])[0][1]
        print(infProb)
        return render_template('show.html', inf=round(infProb*100))
    else:
        return render_template('index.html')
    
    return render_template('index.html')
      
#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logout","success")
    return redirect(url_for('login'))

if __name__=='__main__':
    app.secret_key="1234567"
    app.run(debug=True)
