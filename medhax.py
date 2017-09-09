from flask import Flask,render_template
from twilio.rest import Client

app = Flask(__name__)

sid = "AC8632c0885d33bcf38b8eaa6cc6a33f87"
authtoken = "fba3f82a812fc559b22dd979c7351b9c"
client = Client(sid, authtoken)

@app.route("/")
def index():
    return render_template('home.html')

@app.route('/sms', methods=[POST])
def sms():
    message_body = request.form['Body']
    print(message_body)
message = client.messages.create(to="+12674749730", from_="+18722282071", body="Hello there!")

