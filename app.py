from flask import Flask,render_template,request,make_response
import mysql.connector
import json
from werkzeug.utils import secure_filename
import os
import csv
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from flask_cors import CORS, cross_origin

app=Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dataloader')
def dataloader():
    return render_template('dataloader.html')

@app.route('/planning')
def planning():
    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
    sqlquery="select * from dataset limit 100"
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('planning.html',tbdata=data)

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/regdata')
def regdata():
	nm=request.args['stname']
	em=request.args['email']
	ph=request.args['phone']
	gen=request.args['gender']
	addr=request.args['addr1']
	pwd=request.args['pswd']
	connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
	sqlquery="insert into userdata(uname,email,phone,gender,addr,pswd) values('"+nm+"','"+em+"','"+ph+"','"+gen+"','"+addr+"','"+pwd+"')"
	print(sqlquery)
	cursor = connection.cursor()
	try:
		cursor.execute(sqlquery)
	except mysql.connector.IntegrityError:
		connection.commit()
		cursor.close()
		connection.close()
		msg="Email already present"
		resp=json.dumps(msg)
		return resp
     
	connection.commit()
	cursor.close()
	connection.close()
	msg="Data Saved Successfully"
	resp=json.dumps(msg)
	return resp



@app.route('/logdata')
def logdata():
	em=request.args['email']
	pwd=request.args['pswd']
	msg=''
	connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
	if(em == "admin" and pwd == "admin"):
		msg='admin'
	else:
		sqlquery="select count(*) from userdata where email='"+em+"' and pswd='"+pwd+"'"
		cursor = connection.cursor()
		cursor.execute(sqlquery)
		data=cursor.fetchall()
		if data[0][0]>0:
			msg='success'
		else:
			msg='failure'
		print(sqlquery)
		cursor.close()
		connection.close()
	resp=json.dumps(msg)
	return resp



@app.route('/dataparser',methods=['GET','POST'])
def dataparser():   
    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='') 
    cursor = connection.cursor()
    prod_mas = request.files['csvfile']
    filename = secure_filename(prod_mas.filename)
    prod_mas.save(os.path.join("./static/Upload/", filename))

    #csv reader
    fn = os.path.join("./static/Upload/", filename)

    # initializing the titles and rows list 
    fields = [] 
    rows = []

    with open(fn, 'r') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)  

        # extracting each data row one by one 
        for row in csvreader:
            rows.append(row)
            print(row)
        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":                
                    query="";
                    query="insert into dataset values (";
                    for col in row: 
                        query =query+"'"+col+"',"
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()

    connection.commit()
    cursor.close()
    connection.close()
    resp=json.dumps("Data loaded successfully to database")
    return resp

@app.route('/datadelete')
def datadelete():   
    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='') 
    cursor = connection.cursor()
    sqlquery="TRUNCATE TABLE dataset;"
    cursor.execute(sqlquery)
    connection.commit()
    cursor.close()
    connection.close()
    for f in os.listdir("./static/Upload/"):
        if not f.endswith(".csv"):
            continue
        os.remove(os.path.join("./static/Upload/", f))
    resp=json.dumps("Data Cleared")
    return resp

@app.route('/contactdata')
def contactdata():
    nm=request.args['stname']
    em=request.args['email']
    ph=request.args['phone']
    msg=request.args['msg']
    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
    sqlquery="insert into contactform(name,email,phone,msg) values('"+nm+"','"+em+"','"+ph+"','"+msg+"')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit()
    cursor.close()
    connection.close()
    msg="Data Saved! We will get back to you soon!"
    resp=json.dumps(msg)
    return resp

@app.route('/predictdata')
def predictdata():
    age=request.args['age']
    sex=request.args['sex']
    cp=request.args['cp']
    trtbps=request.args['trtbps']
    chol=request.args['chol']
    fbs=request.args['fbs']
    restecg=request.args['restecg']
    thalachh=request.args['thalachh']
    exng=request.args['exng']
    oldpeak=request.args['oldpeak']
    slp=request.args['slp']
    caa=request.args['caa']
    thall=request.args['thall']
    print(f"{age} {sex} {cp} {trtbps} {chol} {fbs} {restecg} {thalachh} {exng} {oldpeak} {slp} {caa} {thall}")
    data = {
    'age':[age],
    'sex':[sex],
    'cp':[cp],
    'trtbps':[trtbps],
    'chol':[chol],
    'fbs':[fbs],
    'restecg':[restecg],
    'thalachh':[thalachh],
    'exng':[exng],
    'oldpeak':[oldpeak],
    'slp':[slp],
    'caa':[caa],
    'thall':[thall]
    }

    # Create a DataFrame from the dictionary
    predf = pd.DataFrame(data)

    # Display the DataFrame
    print(predf)

    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
    sqlquery="select * from dataset"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    dataset=cursor.fetchall()
    datasetLL=[]
    for i in range(len(dataset)):
        templist=[]        
        for j in range(len(dataset[i])):
            templist.append(dataset[i][j])
        datasetLL.append(templist)


    df = pd.DataFrame(datasetLL,columns = ['age','sex','cp','trtbps','chol','fbs','restecg','thalachh','exng','oldpeak','slp','caa','thall','output'])
    print(type(df))
    print(df)
    cursor.close()
    connection.close()

    x = df.drop("output",axis=1)
    y = df["output"]
    scaler=StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3,stratify=y)
    X_train=scaler.fit_transform(X_train)
    X_test=scaler.fit_transform(X_test)


    classifier = SVC(kernel = 'rbf' , gamma=0.5, C=1.0)
    classifier.fit(X_train,y_train)
    
    y_pred2=classifier.predict(X_test)
    score_log=accuracy_score(y_test,y_pred2)
    print(score_log)
    y_pred_new = classifier.predict(predf)
    print("#########")
    print(y_pred_new)
    print(type(y_pred_new))
    targetList=y_pred_new.tolist()
    print("#########")

    msg=str(targetList)
    resp=json.dumps(msg)
    print(resp)
    return resp



@app.route('/deletedata')
def deletedata():
    age=request.args['age']
    sex=request.args['sex']
    cp=request.args['cp']
    trtbps=request.args['trtbps']
    chol=request.args['chol']
    fbs=request.args['fbs']
    restecg=request.args['restecg']
    thalachh=request.args['thalachh']
    exng=request.args['exng']
    oldpeak=request.args['oldpeak']
    slp=request.args['slp']
    caa=request.args['caa']
    thall=request.args['thall']
    output=request.args['output']
    print(f"{age} {sex} {cp} {trtbps} {chol} {fbs} {restecg} {thalachh} {exng} {oldpeak} {slp} {caa} {thall} {output}")
    connection = mysql.connector.connect(host='localhost',database='heartattack',user='root',password='')
    sqlquery="delete from dataset where age='"+age+"' AND sex='"+sex+"' AND cp='"+cp+"' AND trtbps='"+trtbps+"' AND chol='"+chol+"' AND fbs='"+fbs+"' AND restecg='"+restecg+"' AND thalachh='"+thalachh+"' AND exng='"+exng+"' AND oldpeak='"+oldpeak+"' AND slp='"+slp+"' AND caa='"+caa+"' AND thall='"+thall+"' AND output='"+output+"'"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit()
    cursor.close()
    connection.close()

    msg="Row Deleted Succesfully!"
    resp=json.dumps(msg)
    return resp
	
if __name__=="__main__":
    app.run(debug=True)
