from flask import Flask,render_template,request
from twilio.rest import Client

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
    number = request.form['From']
    message_body = request.form['Body']
    if number not in statetabledict:
        statetabledict[(str(number))] = 'help'
    if("rescue" in message_body and statetabledict[number] == 'help'):
        __help__(request.form)
    return "done"

def __help__(request_obj):
    number = request_obj['From']

    message = client.messages.create(to=str(number), from_="+18722282071", body="Please Send An Approx address or leave blank for your current location")
    statetabledict[number] = 'waiting for address'
    return str(message)

