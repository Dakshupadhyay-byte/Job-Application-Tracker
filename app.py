from flask import Flask, render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import URL,text

load_dotenv()

app=Flask(__name__)



applications=[]

@app.route("/")
def home():
    return "Homepage"


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello"})

@app.route("/api/applications", methods=["GET"])
def get():
    return jsonify(applications)

@app.route("/api/applications", methods=["POST"])
def post():

    data=request.get_json(silent=True)

    if not isinstance(data,dict):
        return jsonify({"error":"Inavalid json data"}),400
    
    company=data.get("company")
    role=data.get("role")


    if not isinstance(company,str) or not company.strip() :
        return jsonify({"error":"Inavalid json data"}),400

    if not isinstance(role,str) or not role.strip() :
        return jsonify({"error":"Inavalid json data"}),400
    


    applications.append({
        "company":company,
        "role":role
    })

    return jsonify({
        "message":" Upadted succesfully"
    }),201





database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME")
)


app.config["SQLALCHEMY_DATABASE_URI"]= database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app) 


@app.route("/api/db-check")
def db_check():

    result = db.session.execute(
        text("SELECT current_database(), current_user")
    ).one()

    return jsonify({
        "database": result[0],
        "user": result[1]
    })



class Application(db.Model):
    __tablename__="applications"

    id= db.Column(db.Integer,primary_key=True)

    role=db.Column(db.String(50),nullable=False)

    company=db.Column(db.String(70),nullable=False)
    
    status=db.Column(db.String(40),nullable=False,   default="Applied")

    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    user=db.relationship("User", back_populates="applications")


class User(db.Model):

    __tablename__= "users"

    id=db.Column(db.Integer,primary_key=True)

    username=db.Column(db.String(80),nullable=False)

    email=db.Column(db.String(120),unique=True,nullable=False)
    
    password_hash=db.Column(db.String(255),nullable=False)

    applications=db.relationship("Application", back_populates="user")


with app.app_context():
    db.create_all()
    