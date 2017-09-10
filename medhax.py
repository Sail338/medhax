from flask import Flask,render_template,request, redirect,jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse,Message
import dbUtils as dbutils
import googlemaps
app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyAjkZv3gEGBYTcwv7K4ePX1ZIXTMRadk1c')
sid = "AC8632c0885d33bcf38b8eaa6cc6a33f87"
authtoken = "fba3f82a812fc559b22dd979c7351b9c"
client = Client(sid, authtoken)
statetabledict = {}

def __messagefirstresponder__(victimnumber,firstresponder):
        firstrespondernumber = firstresponder[1]['phone'] 
        if '1111111111' in firstrespondernumber:
            return
        mapsurl = 'https://www.google.com/maps/dir/?api=1&destination='+ str(statetabledict[victimnumber]['location']['lat']) + "," + str(statetabledict[victimnumber]['location']['lng'])
        message = client.messages.create(to=str(firstrespondernumber), from_="+18722282071", body=statetabledict[victimnumber]['name'] +" needs help "+ str(round(firstresponder[0],2))  + " miles away " + "at: " + mapsurl)

        dbutils.deleteVictim(statetabledict[victimnumber]['name'])
        statetabledict[firstrespondernumber]['state'] = 'waiting fr done'
        #delete the victim
        
def checkPhone(phone):
    phonenum = []
    for c in phone:
        if c.isdigit() or c == '+':
            phonenum.append(c)
    return ''.join(phonenum)

@app.route('/getAllVictims', methods=['GET'])
def getAllVictims():
    ret = dbutils.getVictimLocations()
    return jsonify(ret)
@app.route('/getAllResponders',methods = ['GET'])
def getAllResoinders():
    ret = dbutils.getResponderLocations()
    return jsonify(ret)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/victim')
def victim():
    return render_template('victim.html')

@app.route('/submitVictim', methods=['POST'])
def submitVictim():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        location = request.form['location']
        victiminfo = {}
        victiminfo['name'] = name
        victiminfo['phone'] = checkPhone(phone)
        victiminfo['location'] = gmaps.geocode(location)[0]['geometry']['location']
        number = victiminfo['phone']
        statetabledict[victiminfo['phone']] = victiminfo 
        firstrespondertuple = dbutils.addVictim(statetabledict[number])
        __messagefirstresponder__(victiminfo['phone'],firstrespondertuple)
        return redirect('/')

@app.route('/rescuer')
def rescuer():
    return render_template('rescuer.html')

@app.route('/submitRescuer', methods=['POST'])
def submitRescuer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        location = request.form['location']
        
        responderinfo = {}
        responderinfo['name'] = name
        responderinfo['phone'] = checkPhone(phone)
        responderinfo['location'] = gmaps.geocode(location)[0]['geometry']['location']
        dbutils.addResponder(responderinfo)
        return redirect('/')

@app.route('/sms', methods=['POST'])
def sms():
    print (request.form)
    number = request.form['From']
    message_body = request.form['Body']
    if number not in statetabledict:
        statetabledict[(str(number))] = {}
        statetabledict[str(number)]['state'] = 'init'
    
    
    if("rescue" in message_body.lower() and statetabledict[number]['state'] == 'init'):
        __help__(request.form)
    elif("responder" in message_body.lower() and statetabledict[number]['state'] == 'init'):
        statetabledict[number]['phone'] = number
        __respondtoinit__(request.form)
    elif statetabledict[number]['state'] == 'waiting for name fr':
        __respondtoname__(request.form)
    
    elif statetabledict[number]['state'] == 'waiting for namevictime':
        __grabName__(request.form)
    elif statetabledict[number]['state'] == 'waiting for address fr':
        __firestresponderaddress__(request.form)
    elif statetabledict[number]['state'] == 'waiting for address':
        print("state is waiting for address")
        __address__(request.form)
    elif statetabledict[number]['state'] == 'waiting fr done' and "done" in message_body.lower():
        __askfornewaddressFirstResponder__(request.form)
    elif statetabledict[number]['state'] == 'waiting for address fr update':
        __updatenewadressFirstResponder__(request.form)


        
    return "done"
def __updatenewadressFirstResponder__(request_obj):
        number = request_obj['From']
        bod = request_obj['Body']
        geocode_rest = gmaps.geocode(str(bod))
        print(geocode_rest[0]['geometry'])
        statetabledict[number]['address'] = geocode_rest[0]['formatted_address']
        statetabledict[number]['location'] = geocode_rest[0]['geometry']['location']
        statetabledict[number]['location']['lat'] = float(statetabledict[number]['location']['lat'])
        print ( statetabledict[number]['location']['lat'])
        statetabledict[number]['location']['lng'] = float(statetabledict[number]['location']['lng'])
        victim = dbutils.findNearestVictim(statetabledict[number])
        distance = victim[0]
        victim_data = victim[1]
        if victim_data['phone'] not in statetabledict:
            statetabledict[victim_data['phone']] = victim_data 
        __messagefirstresponder__(victim_data['phone'],(distance,statetabledict[number])) 
        

def __askfornewaddressFirstResponder__(request_obj):
        number = request_obj['From']
        message = client.messages.create(to=str(number), from_="+18722282071",
                                     body=" please update your approximate address to continue helping people.")
        statetabledict[number]['state']= 'waiting for address fr update'

def __help__(request_obj):
    number = request_obj['From']
    
    print("calling help") 
    message = client.messages.create(to=str(number), from_="+18722282071",
                                 body="Please send your name.")
    statetabledict[number]['state'] = 'waiting for namevictime'
    return str(message)
def __grabName__(request_obj):
    body = request_obj['Body']
    number = request_obj['From']
    name = body

    message = client.messages.create(to=str(number), from_="+18722282071",body="Hi " + str(name) + ", please send your approx address")

    statetabledict[number]['state'] = 'waiting for address'
    statetabledict[number]['name'] = name
    statetabledict[number]['phone'] = number
    #ask for the name buddy
    return str(message)

def __address__(request_obj):
    #insert into the database
    number = request_obj['From']
    
    message = client.messages.create(to=str(number), from_="+18722282071",
                                 body="Stay where you are. Someone will be there shortly.")
    bod = request_obj['Body']
    geocode_rest = gmaps.geocode(str(bod))

    print(geocode_rest[0]['geometry'])
    statetabledict[number]['address'] = geocode_rest[0]['formatted_address']
    statetabledict[number]['location'] = geocode_rest[0]['geometry']['location']
    statetabledict[number]['location']['lat'] = float(statetabledict[number]['location']['lat'])
    statetabledict[number]['location']['lng'] = float(statetabledict[number]['location']['lng'])
    #insert into the database
    firstrespondertuple = dbutils.addVictim(statetabledict[number])
    __messagefirstresponder__(number,firstrespondertuple)
    statetabledict[number]['state'] = 'init'
    return message

        
        #text directions
def __respondtoinit__(request_obj):
        
        number = request_obj['From']
        message = client.messages.create(to=str(number), from_="+18722282071",
                                     body="Hi! Thanks for you interest in being a first responder. Please send your name.")
        statetabledict[number]['state'] = 'waiting for name fr'

def __respondtoname__(request_obj):
        number = request_obj['From']
        name = request_obj['Body']
        message = client.messages.create(to=str(number), from_="+18722282071",
                                     body="Hi "  + name + ", please send your approximate address to begin helping people.")
        statetabledict[number]['name'] = name
        statetabledict[number]['state']= 'waiting for address fr'
def __firestresponderaddress__(request_obj):
        number = request_obj['From']
        
        message = client.messages.create(to=str(number), from_="+18722282071",
                                     body="Thanks for the address, you should be getting requests shortly.")
        bod = request_obj['Body']
        geocode_rest = gmaps.geocode(str(bod))

        print(geocode_rest[0]['geometry'])
        statetabledict[number]['address'] = geocode_rest[0]['formatted_address']
        statetabledict[number]['location'] = geocode_rest[0]['geometry']['location']

        statetabledict[number]['location']['lat'] = float(statetabledict[number]['location']['lat'])
        print ( statetabledict[number]['location']['lat'])

        statetabledict[number]['location']['lng'] = float(statetabledict[number]['location']['lng'])
        dbutils.addResponder(statetabledict[number]) 

        
    

if __name__ == "__main__":
   app.run(debug=True)
