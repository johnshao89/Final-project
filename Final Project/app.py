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
    with open("project_data.txt","a") as storage:
            print(in_project,in_temperature,in_rate,in_time,in_solvent, sep="|",file=storage)
    return render_template("results.html", the_project=in_project,
    the_temperature=in_temperature,the_rate=in_rate,the_time=in_time,
    the_solvent=in_solvent)

#define the website to view the overall result
@app.route("/sum_info")
def sum_data():
        content=[]
        titles=["Project Code","Temperature","Agitation Rate","Reaction Time","Solvent"]
        with open ("project_data.txt") as exp_info:
                for line in exp_info:
                        content.append([])
                        for item in line.strip().split("|"):
                                content[-1].append(item)
        return render_template("sum_info.html", row_titles=titles,the_data=content)

#define the website for specific project results
@app.route("/project",methods=["POST"])
def sel_project():
        project_code=request.form["sum_projects"]
        content=[]
        titles=["Project Code","Temperature","Agitation Rate","Reaction Time","Solvent"]
        with open ("project_data.txt") as exp_info:
                for line in exp_info:
                        if line.strip().split("|")[0]==project_code:
                                content.append([])
                                for item in line.strip().split("|"):
                                        content[-1].append(item)
        return render_template("single_project.html", row_titles=titles,the_data=content)






if __name__=="__main__":
    app.run(debug=True)

