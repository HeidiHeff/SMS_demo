# -*- coding: utf-8 -*-
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
#
############
# get local app running
# foreman start to makesure
# git push heroku master to run
# heroku open to verify
############
#--------------------------------------------------------------------------------

# import needed libraries and modules
from flask import Flask, request, redirect, session
import twilio.twiml
from twilio.rest import TwilioRestClient
import os

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
    return 'hello'


# set URL for Twilio to retrieve and execute the TwiML via the selected HTTP
# method when this number receives a message. # Handle a POST request to send a
#text message (via ajax)
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