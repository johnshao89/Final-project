#Import modules
from flask import Flask, render_template,request,jsonify
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from collections import defaultdict

#Set up the flask
app=Flask(__name__)
@app.route("/")
def login():
        return render_template("login_verify.html")
#Define the home page
@app.route("/entry")
@app.route("/entry.html")
@app.route("/templates/entry")
def home_page():
    return render_template("entry.html",the_title="Welcome to the Design of Experiment Data Management")

#Define the data collection from entry.html and show in results.html
@app.route("/input_data",methods=["POST"])
def input_data():        
        in_project=request.form["projects"]
        in_temperature=request.form["temperature"]
        in_rate=request.form["rate"]
        in_time=request.form["reaction_time"]
        in_solvent=request.form["solvents"]
        in_purity=request.form["purity"]
        in_yield=request.form["yield"]
        dbconfig={'host':'127.0.0.1','user':'guest','password':'123456','database':'projectresults',}
        conn=mysql.connector.connect(**dbconfig)
        cursor=conn.cursor()
        _SQL1="""Create Table if not exists results (
                id int auto_increment primary key,
                project_code varchar(50),
                temperature varchar(50),
                agitation_rate varchar(50),
                reaction_time varchar(50),
                solvents varchar(50),
                purity varchar(50),
                yield varchar(50)
        );
        """
        cursor.execute(_SQL1)
        _SQL2="""insert into results (project_code,temperature,agitation_rate,reaction_time,solvents,purity,yield)
        values (%s,%s,%s,%s,%s,%s,%s);
        """
        cursor.execute(_SQL2,(in_project,in_temperature,in_rate,in_time,in_solvent,in_purity,in_yield))
        conn.commit()
        cursor.close()
        conn.close()
        with open("project_data.txt","a") as storage:
                print(in_project,in_temperature,in_rate,in_time,in_solvent,in_purity,in_yield, sep="|",file=storage)
        return render_template("results.html", the_project=in_project,
        the_temperature=in_temperature,the_rate=in_rate,the_time=in_time,
        the_solvent=in_solvent,the_purity=in_purity,the_yield=in_yield)

#define the website to view the overall result
@app.route("/sum_info")
def sum_data():
        content=[]
        titles=["Project Code","Temperature","Agitation Rate","Reaction Time","Solvent","Purity","Yield"]
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
        titles=["Project Code","Temperature","Agitation Rate","Reaction Time","Solvent","Purity","Yield"]
        with open ("project_data.txt") as exp_info:
                for line in exp_info:
                        if line.strip().split("|")[0]==project_code:
                                content.append([])
                                for item in line.strip().split("|"):
                                        content[-1].append(item)
        return render_template("single_project.html", row_titles=titles,the_data=content)
@app.route("/metadata/<proj_code>")
def get_json(proj_code):
        content=[]
        with open ("project_data.txt","r") as data:
                for row in data:
                        if row.split("|")[0]==proj_code:
                                metadata_project=defaultdict(list)
                                metadata_project["Project_Code"]=row.split("|")[0]
                                metadata_project["Temperature"]=float(row.split("|")[1])
                                metadata_project["Agitate_Rate"]=float(row.split("|")[2])
                                metadata_project["Reaction_Time"]=float(row.split("|")[3])
                                metadata_project["solvents"]=row.split("|")[4]
                                metadata_project["Purity"]=float(row.split("|")[5])
                                metadata_project["Yield"]=float(row.split("|")[6])
                                content.append(metadata_project)
        return jsonify (content)




if __name__=="__main__":
    app.run(debug=True)

