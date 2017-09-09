from flask import Flask,render_template,request

@app.route('/victim', methods=['POST'])
def registerVictim():
    name = request.form['name']
    phone = request.form['phone']
    location = request.form['location']
    
@app.route('/rescuer', methods=['POST'])
def registerRescuer():
    name = request.form['name']
    phone = request.form['phone']
    location = request.form['location']

