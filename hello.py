from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import json

app = Flask(__name__)
app.secret_key = "wearethechapions*1234"

@app.route('/')
def home():
    return render_template("home.html", codes=session)

@app.route('/<string:code>')
def fetch(code):
    with open("db.json",'r') as json_file:
        db = json.load(json_file)
    
    if code not in db.keys():
        return abort(404)
    
    return redirect(db[code]['url'])

@app.route('/your_url', methods=['GET','POST'])
def your_url():
    if request.method == 'GET':
        #flash("Invalid Request. Please Shorten using the below form")
        #return redirect(url_for('home'))
        return render_template("your_url.html",code='')
    
    Code = request.form['code']

    with open('db.json','r') as json_file:
        db = json.load(json_file)

    if Code in db.keys():
        flash("The Name has Already been taken. Please Choose an other name")
        return redirect(url_for('home'))
        
    db[Code] = {'url':request.form['url']}
    session[Code] = request.form['url']

    with open('db.json','w') as json_file:
        json.dump(db,json_file)

    return render_template("your_url.html",code=Code)

@app.route('/reset/<string:password>')
def reset(password):
    passkey = "thisisme123"
    if password == passkey:
        session.clear()
        with open('db.json','w') as json_file:
            json.dump({},json_file)
    
    return redirect(url_for('home'))
    
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404
    

if __name__ == '__main__':
    app.run(debug=True)