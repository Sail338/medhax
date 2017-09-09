from flask import Flask,render_template,request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse,Message
app = Flask(__name__)

sid = "AC8632c0885d33bcf38b8eaa6cc6a33f87"
authtoken = "fba3f82a812fc559b22dd979c7351b9c"
client = Client(sid, authtoken)
statetabledict = {}
@app.route("/")
def index():
    return render_template('home.html')

@app.route('/sms', methods=['POST'])
def sms():
    print (request.form)
    number = request.form['From']
    message_body = request.form['Body']
    if number not in statetabledict:
        statetabledict[(str(number))] = 'help'

    if("rescue" in message_body and statetabledict[number] == 'help'):
        __help__(request.form)
    elif statetabledict[number] == 'waiting for address':
        print("state is waiting for address")
        __address__(request.form)
        statetabledict[(str(number))] = 'RESCUE'
    if("RESCUE" in message_body and statetabledict[number] == 'RESCUE'):
        __help__(request.form)
        statetabledict[(str(number))] = 'RESCUE'
    if("RESCUE" in message_body and statetabledict[number] == 'RESCUE'):
        __help__(request.form)
    if statetabledict[number] == 'waiting for address':
        #parse message bodt
        #request address
        #parse the address and send back someone will be there asap and insert into the db

    return "done"


def __help__(request_obj):
    number = request_obj['From']
    
    print("calling help") 
    message = client.messages.create(to=str(number), from_="+18722282071",
                                 body="Please send aprox location")
    message = client.messages.create(to=str(number), from_="+18722282071", body="Please send an approx address")
    statetabledict[number] = 'waiting for address'
    return str(message)

def __address__(request_obj):
    #insert into the database
    number = request_obj['From']
    message = client.messages.create(to=str(number), from_="+18722282071",
                                 body="Stay where you are")
    return message
if __name__ == "__main__":
    app.run(debug=True)
