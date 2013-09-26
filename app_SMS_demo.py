# -*- coding: utf-8 -*-
# above line: encoding set from python default unicode to utf-8

#------------------------------------------------------------------------------
#
# Author: Heidi Heffelfinger - CodingDojo
# Dev environment:  Linux - Ubuntu 13.04 (kernel: 3.8.0-30)
#                   virtualenv
#                   git (v1.8.1.2)
#
# App: SMS Text - Demonstration Application w/Twilio API
# Version: 1.0.0 - demo only
# Code: https://github.com/HeidiHeff/SMS_demo
#
# Twilio Number - 415-484-1446
# URL: http://quiet-tundra-1590.herokuapp.com/sms
#
# Language: Python (v2.7.4)
# Framework: Flask (v0.10.1)
# API(s) used: Twilio-python
# Server-type: Green Unicorn (v18.0)
# PaaS: Heroku
#
# First demonstrated on 9/27/2013 at CodingDojo
#
#------------------------------------------------------------------------------

# import needed libraries and modules
from flask import Flask, request, redirect, session
import twilio.twiml
from twilio.rest import TwilioRestClient
import os

# The session object makes use of a secret key.
SECRET_KEY = 'FMy"oSxC8p_sW#7~&9h3?!=nhe$%|wT'

#initialize app
app = Flask(__name__)
app.config.from_object(__name__)

# Render the home page
@app.route('/')
def index():
    return 'hello'

# set URL for Twilio to retrieve and execute the TwiML via the selected HTTP
# method when this number receives a message.
@app.route("/sms/", methods = ['GET', 'POST'])
def sms():	
    """Respond with the number of text messages sent between two parties."""
    counter = session.get('counter', 0)
    # increment the counter
    counter += 1
    # Reset counter after quiz
    if counter > 6:
        counter = 1
    # Save the new counter value in the session
    session['counter'] = counter

    # initialize variables
    score = session.get('score', 0)
    answer = request.values.get('Body', '')
    answer_response = False
    response = False

    # start quiz
    if counter == 1:
        answer_response = "Thanks for taking our 5 question U.S. healthcare knowledge quiz."
    	response = "1st question: What is the average annual premium for family coverage on an employer health plan? A) $7,791, B) $21,248, C) $15,745, or D) $12,375"
    elif counter == 2:
        answer_response = "No, the average premium for family coverage on an employer health plan is $15,745."
    	if answer.lower() == 'c' or answer == "$15,745":
            answer_response = "You are correct!"
            score += 1
        response = "2nd question: What percentage of employer health premiums do workers pay, on average? A) 27.4%, B) 17.1%, C) 50.3%, or D) 5.8%"
    elif counter == 3:
        answer_response = "No, the average percentage of employer health premiums paid by workers is 27.4%."
        if answer.lower() == 'a' or answer == "27.4%":
            answer_response = "You are correct!"
            score += 1
        response = "3rd question: When must most Americans purchase health insurance or face a penalty? A) January 2015, B) January 2014, C) December 2013, or D) December 2015"
    elif counter == 4:
        answer_response = "No, most Americans have to purchase health insurance or face a penalty under the federal healthcare law by January 2014."
        if answer.lower() == 'b' or answer == "January 2014":
            answer_response = "You are correct!"
            score += 1
        response = "4th question: What percentage of U.S. small businesses offered health benefits to their workers in 2010? A) 49%, B) 69%, C) 32%, or D) 58%"
    elif counter == 5:
        answer_response = "No, the percentage of U.S. small businesses which offered health benefits in 2010 was 49%."
        if answer.lower() == 'a' or answer == "49%":
            answer_response = "You are correct!"
            score += 1
        response = "5th question: How many people under 26 have been added to health plans as part of the Affordable Care Act? A) 5.6 mil., B) 0.5 mil., C) 2.9 mil., or D) 1.3 mil."
    elif counter == 6:
        answer_response = "No, 2.9 million young adults under age 26 have been added to their parents' health plans as part of the Affordable Care Act."
        if answer.lower() == 'c' or answer == "2.9 mil.":
            answer_response = "You are correct!"
            score +=1
        # end quiz, provide user with score
        response = "Thanks for taking our healthcare knowledge quiz! You correctly answered %d out of 5 questions." % score
        # reset score to 0
        score = 0

    # set score for the session
    session['score'] = score
    
    # set and return responses to be texted via SMS to user
    resp = twilio.twiml.Response()
    if answer_response:
        resp.sms(answer_response)
    resp.sms(response)
    return str(resp)

# run the app if initialized; run debugger pre-production
if __name__ == "__main__":
	# app.debug = True
	app.run()