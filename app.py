### Importing required libraries
import os
from flask import Flask,request,render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pyshorteners

url=""
short_url=""
app=Flask(__name__)

####SQLAlchemy configuration
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)  
Migrate(app,db)

####ceating a model
class Link_Database(db.Model):
    __tablename__='urlshortener'
    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(100))
    short_url = db.Column(db.String(100))
    
    def __init__(self,url,short_url):
        self.url=url
        self.short_url=short_url

####routes     
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/',methods=["GET","POST"])
def home():
    global short_url,original
    if request.method=='POST':
        original=request.form.get('url')
        shortener=pyshorteners.Shortener()
        short_url=shortener.tinyurl.short(original)
        val=Link_Database(original,short_url)
        db.session.add(val)
        db.session.commit()
        
    return render_template('index.html',s_url=short_url)

@app.route('/history')
def history():
    short_links=Link_Database.query.all()
    return render_template('history.html',short_links=short_links)

@app.route('/deleteAll', methods=['POST'])
def delete():
    db.session.query(Link_Database).delete()
    db.session.commit()
    return redirect(url_for('history'))

if __name__=="__main__":
    app.run(debug=True)