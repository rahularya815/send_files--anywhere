from flask import Flask, request, render_template, session, url_for, logging, redirect, flash
from datetime import datetime
from pymongo import MongoClient
import json
import sqlite3
import re
from werkzeug.utils import secure_filename
import os
import random
import string


app = Flask(__name__,static_folder='uploads')

app.config["VIDEO_UPLOADS"] = "uploads"
app.config["ALLOWED_VIDEO_EXTENSIONS"] = ["MP4", "MPEG", "AVI", "GIF","PPTX","DOCX","PDF","JPG","JPEG","APK","APKX"]
app.config["MAX_VIDEO_FILESIZE"] = 1000* 1024 * 1024

conn=sqlite3.connect('web.sqlite')
cur=conn.cursor()


d=0
auser=list()


@app.route("/haha")
def hello():
    return ("<h1>hello</h1>")

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        conn=sqlite3.connect('web.sqlite')
        cur=conn.cursor()
        cur.execute('SELECT password FROM Counts where username=?',(username,))
        pw=cur.fetchall()
        cur.execute('SELECT name FROM Counts where username=?',(username,))
        pwn=cur.fetchall()
        
        cur.execute('SELECT id FROM Counts where username=?',(username,))
        ptt=cur.fetchall()
        try:
            
            c=pw[0]
            c3=ptt[0]
            c4=pwn[0]
            session['name']=c4[0]
            session['d']=c3[0]
            
            
            if (c[0]==password ):
                    session['log'] = True
                    flash("You are logged in", "success")
                    return redirect('/vid')
                    
                 
            else:
                    flash("Incorrect password", "danger")           
                    return render_template("login.html")
        except:
        
            if not pw:
                flash("You are not registered", "danger")
                return redirect("/register")
            
                
        
        
        
        
    else:
        return render_template('home.html')

@app.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #print(json.dumps(request.form, indent=4))
        name = request.form['name']
        username = request.form['username']

        phone=request.form['phone']
        email=request.form['email']
        
        password = request.form['password']
        confirm = request.form['confirm password']
        conn=sqlite3.connect('web.sqlite')
        cur=conn.cursor()
        cur.execute('SELECT username FROM Counts where username=?',(username,))
        auser=cur.fetchall()
        if not auser:
        
            if(password==confirm):
            
                #cur.execute('DROP TABLE IF EXISTS Counts')
            
                try:
                    cur.execute('CREATE TABLE Counts(id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,name TEXT,username TEXT,phone INTEGER,email TEXT,password TEXT,confirm TEXT)')
                    cur.execute('INSERT INTO Counts(name,username,phone,email,password,confirm) VALUES (?,?,?,?,?,?)',(name,username,phone,email,password,confirm))
                    flash("Registration successful", "success")
                except:
                    cur.execute('INSERT INTO Counts(name,username,phone,email,password,confirm) VALUES (?,?,?,?,?,?)',(name,username,phone,email,password,confirm))
                    flash("Registration successful", "success")
                conn.commit()
                return redirect('/')
            else:
                flash("Password do not match", "danger")
                return render_template("register.html")
        else:
             flash("Username already exist", "danger")
             return render_template("register.html")
    else:
        return render_template('register.html')



@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out!","success")
    return redirect("/")
    
    
    
    
def allowed_video(filename):

    if not "." in filename:
        return False

    ext = filename.split(".")[-1]
    
    if ext.upper() in app.config["ALLOWED_VIDEO_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_video_filesize(filesize):

    if int(filesize) <= app.config["MAX_VIDEO_FILESIZE"]:
        return True
    else:
        return False


@app.route('/vid', methods=["GET", "POST"])
def upload_video():

    if request.method == "POST":

       # if request.form:

                conn=sqlite3.connect('name.sqlite')
                cur=conn.cursor()
                
                
               
                uuid=request.form['uuid']
                teachername=request.form['teachername']
                print(teachername)
                video = request.files["video"]
                ext = video.filename.split(".")[-1]
                ext=ext.upper()
                print(video.filename)
                if video.filename == "":
                    flash("No filename","danger")
                    return redirect('/vid')
                    
                try:
                    cur.execute('CREATE TABLE vidata(id,name TEXT,extension TEXT,teachername TEXT,idd  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')
                    cur.execute('INSERT INTO vidata(id,name,extension,teachername) VALUES (?, ?,?,?)', (int(uuid), video.filename, ext,teachername,) )
                    
                except:
                    cur.execute('INSERT INTO vidata(id,name,extension,teachername) VALUES ( ?,?,?,?)', (int(uuid), video.filename,ext,teachername, ) )
                    
                conn.commit()   

                if allowed_video(video.filename):
                    filename = (video.filename)
                    print(filename)

                    video.save(os.path.join(app.config["VIDEO_UPLOADS"], filename))

                    flash("File Uploaded","success")

                    return redirect('/vid')

                else:
                    flash("File extension is not allowed","danger")
                    return redirect('/vid')
    else:
        conn=sqlite3.connect('name.sqlite')
        
        cur=conn.cursor()
        cur.execute('SELECT*FROM vidata ORDER BY idd DESC')
        #conn.commit()
        #cur.execute('SELECT name FROM vidata')
        a=cur.fetchall()
        #print(a)
        
        
        return render_template("vid.html",vid=a,uid=session.get('d'),name=session.get('name'))
    
@app.route('/vid/delete/<string:name>')   
def delete(name):
    conn=sqlite3.connect('name.sqlite')
    cur=conn.cursor()
    #print(name)
    os.remove(os.path.join(app.config["VIDEO_UPLOADS"],name))
    cur.execute('DELETE FROM vidata WHERE name=(?)',(name,))
    conn.commit()
    return redirect('/vid')  
    



    

app.secret_key="12ddededd"
app.run(debug=True)