
from flask import Flask, render_template,jsonify,request
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