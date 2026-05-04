# Heartattack--prediction--System-dproject
A Machine Learning-based Heart Attack Prediction System built using Flask, MySQL, and Scikit-learn. The system analyzes medical parameters like blood pressure, cholesterol, and heart rate to predict the risk of heart attack.
# ❤️ Heart Attack Prediction System

## 📌 Project Overview

This project is a web-based application that predicts the risk of heart attack using Machine Learning algorithms. It allows users to register, login, upload datasets, and get predictions based on health parameters.

---

## 🚀 Features

* User Registration & Login System
* Upload CSV Dataset
* Data Storage using MySQL
* Machine Learning Prediction (SVM Algorithm)
* Heart Attack Risk Prediction
* Simple and User-Friendly Interface

---

## 🛠️ Technologies Used

* Python
* Flask
* MySQL
* Pandas
* Scikit-learn
* HTML, CSS, JavaScript

---

## 📊 Machine Learning Model

* Algorithm Used: Support Vector Machine (SVM)
* Data Preprocessing: StandardScaler
* Train-Test Split
* Accuracy Evaluation

---

## 📂 Project Structure

```
Heart-Attack-Prediction-System/
│── app.py
│── templates/
│── static/
│── heartattack
.sql
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/Heart-Attack-Prediction-System.git
cd Heart-Attack-Prediction-System
```

### 2. Install Dependencies

```
pip install flask mysql-connector-python pandas scikit-learn flask-cors
```

### 3. Setup Database

* Create database in MySQL:

```
CREATE DATABASE heartattack;
```

* Import SQL file:

```
mysql -u root -p heartattack < heartattackdb.sql
```

### 4. Run Application

```
python app.py
```

### 5. Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📈 Input Parameters for Prediction

* Age
* Sex
* Chest Pain Type (cp)
* Resting Blood Pressure (trtbps)
* Cholesterol (chol)
* Fasting Blood Sugar (fbs)
* Resting ECG (restecg)
* Maximum Heart Rate (thalachh)
* Exercise Induced Angina (exng)
* Oldpeak
* Slope (slp)
* Number of Major Vessels (caa)
* Thalassemia (thall)

---

## 🎯 Conclusion

This system helps in early detection of heart attack risk using machine learning, which can assist healthcare professionals and patients in taking preventive measures.

---

## 👩‍💻 Author

Vaishnavi 
