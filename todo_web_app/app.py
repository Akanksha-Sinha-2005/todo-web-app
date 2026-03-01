from flask import Flask,render_template,request,redirect
import json
import os

app=Flask(__name__)
TASK_FILE="tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE,"r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE,"w") as f:
        json.dump(tasks,f,indent=4)

@app.route("/")
def index():
    tasks=load_tasks()
    search_query=request.args.get("search","")
    status_filter=request.args.get("status","all")
    if search_query:
        tasks=[task for task in tasks if search_query.lower() in task["title"].lower()] 
    if status_filter=="completed":
        tasks=[task for task in tasks if task["completed"]]
    elif status_filter=="pending":
        tasks=[task for task in tasks if not task["completed"]]
    return render_template("index.html",tasks=tasks,search_query=search_query,status_filter=status_filter)

@app.route("/add",methods=["POST"])
def add():
    tasks=load_tasks()
    title=request.form["title"]
    due_date=request.form["due_date"]
    task={"title":title,"due_date":due_date,"completed":False}
    tasks.append(task)
    save_tasks(tasks)
    return redirect("/")

@app.route("/complete/<int:index>")
def complete(index):
    tasks=load_tasks()
    tasks[index]["completed"]=True
    save_tasks(tasks)
    return redirect("/")   

@app.route("/delete/<int:index>")
def delete(index):
    tasks=load_tasks()
    if 0<=index<len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect("/")

@app.route("/edit/<int:index>")
def edit(index):
    tasks=load_tasks()
    task=tasks[index]
    return render_template("edit.html",task=task,index=index)
    
@app.route("/update/<int:index>",methods=["POST"])
def update(index):
    tasks=load_tasks()
    tasks[index]["title"]=request.form["title"]
    tasks[index]["due_date"]=request.form["due_date"]
    tasks[index]["completed"]=True if request.form.get("status")=="completed" else False
    save_tasks(tasks)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)