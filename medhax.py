from flask import Flask,render_template,request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse,Message
import googlemaps
app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyAjkZv3gEGBYTcwv7K4ePX1ZIXTMRadk1c')
sid = "AC8632c0885d33bcf38b8eaa6cc6a33f87"
authtoken = "fba3f82a812fc559b22dd979c7351b9c"
client = Client(sid, authtoken)
statetabledict = {}
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/victim')
def victim():
    return render_template('victim.html')

@app.route('/victim', methods=['POST'])
def registerVictim():
    name = request.form['name']
    phone = request.form['phone']
    location = request.form['location']

@app.route('/rescuer')
def rescuer():
    return render_template('rescuer.html')

@app.route('/rescuer', methods=['POST'])
def registerRescuer():
    name = request.form['name']
    phone = request.form['phone']
    location = request.form['location']

@app.route('/sms', methods=['POST'])
def sms():
    print (request.form)
    number = request.form['From']
    message_body = request.form['Body']
    if number not in statetabledict:
        statetabledict[(str(number))] = {}
        statetabledict[str(number)]['state'] = 'help'

    if("rescue" in message_body.lower() and statetabledict[number]['state'] == 'help'):
        __help__(request.form)
    elif statetabledict[number]['state'] == 'waiting for namevictime':
        __grabName__(request.form)
    elif statetabledict[number]['state'] == 'waiting for address':
        print("state is waiting for address")
        __address__(request.form)
        
    return "done"


def __help__(request_obj):
    number = request_obj['From']
    
    print("calling help") 
    message = client.messages.create(to=str(number), from_="+18722282071",
                                 body="Please send your name")
    statetabledict[number]['state'] = 'waiting for namevictime'
    return str(message)
def __grabName__(request_obj):
    body = request_obj['Body']
    number = request_obj['From']
    name = body

    message = client.messages.create(to=str(number), from_="+18722282071", body="Hi " + str(name) + ", please send your approx location")
    statetabledict[number]['state'] = 'waiting for address'
    statetabledict[number]['name'] = name
    #ask for the name buddy
    return str(message)

def __address__(request_obj):
    #insert into the database
    number = request_obj['From']
    
    message = client.messages.create(to=str(number), from_="+18722282071", body="Stay where you are. Someone will be there shortly.")
    bod = request_obj['Body']
    geocode_rest = gmaps.geocode(str(bod))

    print(geocode_rest[0]['geometry'])
    statetabledict[number]['address'] = geocode_rest[0]['formatted_address']
    statetabledict[number]['location'] = geocode_rest[0]['geometry']['location']
    #insert into the database
    return message

def __messagefirstresponder__(victimnumber,firstresponder):
    firstrespondernumber = firstresponder[1]['phone'] 
    mapsurl = 'https://www.google.com/maps/dir/?api=1&destination='+ str(firstresponder[1]['location']['lat']) + "," + str(firstresponder[1]['location']['lng'])
    message = client.messages.create(to=str(firstrespondernumber), from_="+18722282071", body=statetabledict[victimnumber]['name'] +" needs help "+ str(firstresponder[0]  + " miles away " + " at " + mapsurl))
    #text directions
    
    



    

if __name__ == "__main__":
    app.run(debug=True)
