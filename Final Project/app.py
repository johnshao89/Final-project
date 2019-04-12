#Import modules
from flask import Flask, render_template,request
import mysql.connector

#Set up the flask
app=Flask(__name__)

#Define a function to save all the input data into sql database
'''@app.route("/database")
def view_database():
        dbconfig={'host':'127.0.0.1','user':'guest','password':'123456','database':'projectresults',}
        conn=mysql.connector.connect(**dbconfig)
        cursor=conn.cursor()
        _SQL="""insert into results (project_code,temperature,agitation_rate,reaction_time,solvents)
        values (%s,%s,%s,%s,%s)
        """
        cursor.execute(_SQL,())
'''
#Define the home page
@app.route("/")
@app.route("/entry")
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
        _SQL="""insert into results (project_code,temperature,agitation_rate,reaction_time,solvents,purity,yield)
        values (%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(_SQL,(in_project,in_temperature,in_rate,in_time,in_solvent,in_purity,in_yield))
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


#define the website for holding json data for each project
@app.route("/json/<pro_code>")
def project_json(pro_code):
        pass




if __name__=="__main__":
    app.run(debug=True)

