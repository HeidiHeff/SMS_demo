#--------------------------------------------------------------------------------
# Heidi Heffelfinger - CodingDojo
# SMS Text - Demonstration Application
# Twilio Number - 415.484.5213
#
# Utilizes:
# Python on a Flask framework
# Twilio API
#
# Demonstrated on 9/27/2013 at CodingDojo via LAMPP with ngrok proxy
#
# Special Thanks to Joel Franusic, Developer Advocate at Twilio
#--------------------------------------------------------------------------------

# import needed libraries and modules
from flask import Flask, request, redirect, session
import twilio.twiml
from twilio.rest import TwilioRestClient
# ?import os for sys config?

# ?Pull in configuration from system environment variables - is this needed w/ngrok?
# TWILIO_ACCOUNT_SID = os.environ.get('ACf99ed41102d88db39566f57ccf293309')
# TWILIO_AUTH_TOKEN = os.environ.get('65a6f4045239f1b5011d820d2b0dd746')
# TWILIO_NUMBER = os.environ.get('+14154841446')

# ?create an authenticated client that can make requests to Twilio for your
# account.
# client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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

# Render the home page
@app.route('/')
def index():
    return render_template('index.html')

# ? Allow users to call twilio number from webpage to demonstrate telephony
# integration with Twilio
# Handle a POST request to make an outbound call. This is called via ajax
# on our web page
# @app.route('/call', methods=['POST'])
# def call():
#     # Make an outbound call to the provided number from your Twilio number
#     call = client.calls.create(to=request.form['to'], from_=TWILIO_NUMBER,
#                                url='')

#     # Return a message indicating the call is coming
#     return 'Call inbound!'

# @app.route("/voice")
# def voice():
#     response = twiml.Response()
#     with response.gather(numDigits=1, action='/gather') as g:
#         g.say('If you would like to leave a recorded message, press 1, else press 2 to listen to the last recorded message.', voice='woman')
#     return str(response)

# Collect voice message
# @app.route("/gather", methods = ["GET", "POST"])
# def gather():
#     response = twiml.Response()
#     if request.form['Digits'] == "1":
#         response.say('Leave your message now.', voice='woman')
#         response.record(maxLength = 30, action = '/record', method = 'POST')
#     elif request.form['Digits'] == "2":
#         response.say("Here is the last message.", voice='woman')
#         with open('last.txt', 'r') as f:
#             theFile = f.readline()
#             response.play(theFile)
#     else:
#         response.say("You didn't choose either 1 or 2. Goodbye.", voice='woman')
#     return str(response)

# Store voice message
# @app.route("/record", methods = ["GET", "POST"])
# def record():
#     response = twiml.Response()
#     f = open('last.txt', 'w')
#     f.write(request.form['RecordingUrl'])
#     f.close()
#     return str(response)
# ?

# set URL for Twilio to retrieve and execute the TwiML via the selected HTTP
# method when this number receives a message. # Handle a POST request to send a
#text message (via ajax)
@app.route("/sms", methods = ['POST'])
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

    # temp code
    message = "".join([name, " has messaged ", request.values.get('To'), " ", 
        str(counter), " times."])
    response = twilio.twiml.Response()
    response.sms(message)
 
    return str(response)

    # PSEUDOCODE FOR FUNCTIONALITY OF TEXTING
    # score = 0
    # if counter == 1:
    	# response "We're excited you've chosen to take our healthcare knowledge quiz.
        # First question: What’s the average annual premium for family coverage
        # on an employer health plan? A) $7,791, B) $21,248, C) $15,745, or D)
        # $12,375"
        # return response
    	# if answer.lower() == 'b':
        #   response "That's correct!"
        #   score += 1
        #   return response
        # else:
        #   response "No, the average annual premium for family coverage on an
        #   employer health plan is $15,745."
        #   return response
    # elif counter == 2:
        # response "Second question: What percentage of employer health premiums do
        # workers pay, on average? A) 27.4%, B) 17.1%, C) 50.3%, or D) 5.8%"
        # return response
        # if answer.lower() == 'a':
        #   response "That's correct!"
        #   score += 1
        #   return response
        # else:
        #   response "No, the average percentage of employer health premiums paid by
        #   workers is 27.4%"
        #   return response
    # elif counter == 3:
        # response "When do most Americans have to purchase health insurance or face
        # a penalty under the federal healthcare law? A) January 2015, B) January
        # 2014, C) December 2013, or D) December 2015."
        # return response
        # if answer.lower() == 'b':
        #   response "That's correct!"
        #   score += 1
        #   return response
        # else:
        #   response "No, most Americans have to purchase health insurance or face a
        #   penalty under the federal healthcare law by January 2014."
        #   return response
    # elif counter == 4:
        # response "What percentage of U.S. small businesses offered health benefits
        # to their workers in 2010? A) 49%, B) 69%, C) 32%, or D) 58%."
        # return response
        # if answer.lower() == 'a':
        #   response "That's correct!"
        #   score += 1
        #   return response
        # else:
        #   response "No, the percentage of U.S. small businesses which
        #   offered health benefits in 2010 was 49%."
        #   return response
    # elif counter == 5:
        # response "How many young adults under age 26 have been added to their
        #  parents’ health plans as part of the Affordable Care Act? A) 5.6 million,
        # B) 0.5 million, C) 2.9 million, or D) 1.3 million."
        # return response
        # if answer.lower() == 'c':
        #   response "That's correct!"
        #   score += 1
        #   return response
        # else:
        #   response "No, 2.9 million young adults under age 26 have been added to
        #   their parents' health plans as part of the Affordable Care Act."
        #   return response

    # response "You got %d out of 5 healthcare questions correct" % score
    # return response

    # destroy conversation state

# run the app if initialized; run debugger pre-production
if __name__ == "__main__":
	app.debug = True
	app.run()