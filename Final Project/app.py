#Import modules
from flask import Flask, render_template,request

#Set up the flask
app=Flask(__name__)

#Define a function to save all the input data each time
def store_data(*args):
    with open ("project_data.txt","a") as data_storage:
        print(args,sep="|",file=data_storage)

#Define the home page
@app.route("/")
@app.route("/entry")
def home_page():
    return render_template("entry.html",the_title="Welcome to the Design of Experiment")

#Define the data collection from entry.html and show in results.html
@app.route("/input_data",methods=["POST"])
def input_data():
    in_project=request.form["projects"]
    in_temperature=request.form["temperature"]
    in_rate=request.form["rate"]
    in_time=request.form["reaction_time"]
    in_solvent=request.form["solvents"]
    store_data(in_project,in_temperature,in_rate,in_time,in_solvent)
    return render_template("results.html", the_project=in_project,
    the_temperature=in_temperature,the_rate=in_rate,the_time=in_time,
    the_solvent=in_solvent)






if __name__=="__main__":
    app.run(debug=True)

