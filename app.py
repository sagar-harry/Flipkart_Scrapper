from flask import Flask, render_template, request, jsonify, redirect, url_for
from fkart_scraper import run_program
import os

static_folder = os.path.join("webapp", "static")
template_folder = os.path.join("webapp", "template")

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

@app.route("/", methods=["GET", "POST"])
def home():  
    if request.method=="GET":
        return render_template("home.html")        

@app.route("/comments", methods=["GET", "POST"])
def retrieve_comments():
    if request.method == "POST":
        if request.form:
            phone_name = request.form["phone_name"]
            comments = run_program(phone_name=phone_name)
            return render_template("result.html", comments=comments)

        elif request.json:
            phone_name = request.json["phone_name"]
            comments = run_program(phone_name=phone_name)
            return jsonify({"Result":comments})
            
    elif request.method == "GET":
        if request.args:
            phone_name = request.args["phone_name"]
            comments = run_program(phone_name=phone_name)
            return render_template("result.html", comments=comments)

        elif request.json:
            phone_name = request.json["phone_name"]
            comments = run_program(phone_name=phone_name)
            return jsonify({"Result":comments})

    else:
        return {"result": "error"}

    
if __name__=="__main__":
    app.run(debug=True)