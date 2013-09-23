#--------------------------------------------------------------------------------
# Heidi Heffelfinger - CodingDojo
# SMS Text - Demonstration Application
# Twilio Number - 415.484.5213
#
# Utilizes:
# Python on a Flask framework
# Twilio API
#
# Special Thanks to Joel Franusic, Developer Advocate at Twilio
#--------------------------------------------------------------------------------


# import needed libraries and modules
from flask import Flask, request, redirect, session
import twilio.twiml
from twilio.rest import TwilioRestClient

# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'

#initialize app
app = Flask(__name__)
app.config.from_object(__name__)

# list of known numbers
callers = {
    "+14158275389": "HH",
    "+14153784497": "BH"
}

# verify app is working
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sms", methods = ['GET', 'POST'])
def sms():	
    """Respond with the number of text messages sent between two parties."""
    counter = session.get('counter', 0)
    # increment the counter
    counter += 1
    # Save the new counter value in the session
    session['counter'] = counter

    from_number = request.values.get('From')
    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Monkey"

    message = "".join([name, " has messaged ", request.values.get('To'), " ", 
        str(counter), " times."])
    response = twilio.twiml.Response()
    response.sms(message)
 
    return str(response)

# run the app if initialized
if __name__ == "__main__":
	app.debug = True
	app.run()