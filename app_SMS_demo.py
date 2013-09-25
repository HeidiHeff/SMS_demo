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
# callers = {
#     "+14158275389": "HH",
#     "+14153784497": "BH"
# }

# Render the home page
@app.route('/')
def index():
    return 'hello'

# set URL for Twilio to retrieve and execute the TwiML via the selected HTTP
# method when this number receives a message.
@app.route("/sms", methods = ['GET', 'POST'])
def sms():	
    """Respond with the number of text messages sent between two parties."""
    counter = session.get('counter', 0)
    # increment the counter
    counter += 1
    # Reset counter of it gets too big
    if counter > 6:
        counter = 1
    # Save the new counter value in the session
    session['counter'] = counter

    # from_number = request.values.get('From')
    # if from_number in callers:
    #     name = callers[from_number]
    # else:
    #     name = "Person"

    # temp code
    # message = "{} has messaged {} {} times.".format(name, request.values.get('To'), counter)
    # response.sms(message)
 
    # return str(response)

    # PSEUDOCODE FOR FUNCTIONALITY OF TEXTING
    score = session.get('score', 0)
    answer = request.values.get('Body', '')
    answer_response = False
    response = False
    if counter == 1:
    	response = "Welcome to our healthcare knowledge quiz. First question: What’s the average annual premium for family coverage on an employer health plan?"
    elif counter == 2:
        answer_response = "No, the average annual premium for family coverage on an employer health plan is $15,745."
    	if answer.lower() == 'b':
            answer_response = "That's correct!"
            score += 1
        response = "Second question: What percentage of employer health premiums do workers pay, on average? A) 27.4%, B) 17.1%, C) 50.3%, or D) 5.8%"
    elif counter == 3:
        answer_response = "No, the average percentage of employer health premiums paid by workers is 27.4%"
        if answer.lower() == 'a':
            answer_response = "That's correct!"
            score += 1
        response = "3rd question: When do Americans have to purchase health insurance or face a penalty? A) January 2015, B) January 2014, C) December 2013, or D) December 2015."
    elif counter == 4:
        answer_response = "No, most Americans have to purchase health insurance or face a penalty under the federal healthcare law by January 2014."
        if answer.lower() == 'b':
            answer_response = "That's correct!"
            score += 1
        response = "4th question: What percentage of U.S. small businesses offered health benefits to their workers in 2010? A) 49%, B) 69%, C) 32%, or D) 58%."
    elif counter == 5:
        answer_response = "No, the percentage of U.S. small businesses which offered health benefits in 2010 was 49%."
        if answer.lower() == 'a':
            answer_response = "That's correct!"
            score += 1
        response = "5th question: How many people under 26 have been added to health plans as part of the Affordable Care Act? A) 5.6 mil., B) 0.5 mil., C) 2.9 mil., or D) 1.3 mil."
    elif counter == 6:
        answer_response = "No, 2.9 million young adults under age 26 have been added to parents' health plans as part of the Affordable Care Act."
        if answer.lower() == 'c':
            answer_response = "That's correct!"
            score +=1
        response = "Thanks for taking the healthcare quiz! You correctly answered %d out of 5 questions" % score
        # destroy conversation state
        session.delete()


    session['score'] = score
    
    resp = twilio.twiml.Response()
    if answer_response:
        resp.sms(answer_response)
    resp.sms(response)
    return str(resp)

# run the app if initialized; run debugger pre-production
if __name__ == "__main__":
	app.debug = True
	app.run()