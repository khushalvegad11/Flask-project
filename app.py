from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///vk.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),primary_key=False)
    desc = db.Column(db.String(500),primary_key=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
    
@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method =='POST':
        title = request.form["title"]
        desc = request.form["desc"]
        
        todo = Todo(title= title, desc= desc)
        #db.session.add(admin)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method =="POST":
        title= request.form['title']
        desc= request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)




@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect('/')

@app.route("/show")
def vk():
    alltodo = Todo.query.all()
    print(alltodo)
    return "<p>khushal vegad</p>"

if __name__ == "__main__":
    app.run(debug=True)