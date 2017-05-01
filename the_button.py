#!/usr/bin/env python

from __future__ import print_function
import requests
import secrets

PARTICLE_API = "https://api.particle.io/v1/devices"

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# ----------------------- Do some REAL work ------------------------------------
def get_particle_variable(name):
    resp = requests.get("%s/%s/%s?access_token=%s" % (PARTICLE_API, secrets.DEVICE_ID, name, secrets.ACCESS_TOKEN))

    if resp.raise_for_status() == None:
        data = resp.json()

    if 'error' in data and data['error'] != None:
        raise ValueError("Failed to retrieve value for %s: %s" % (name, data['error']))

    return(data['result'])

def call_particle_function(name, str_arg):
    url = "%s/%s/%s" % (PARTICLE_API, secrets.DEVICE_ID, name)
    resp = requests.post(url, data = {'access_token': secrets.ACCESS_TOKEN, 'arg': str_arg});

    if resp.raise_for_status() == None:
        data = resp.json()

    if 'error' in data and data['error'] != None:
        raise ValueError("Failed to call '%s(%s)': %s" % (name, str_arg, data['error']))

    return(data['return_value'])

# ---------------------------- Skill Stuffs ------------------------------------
def on_session_started(request, session):
    pass

def on_session_ended(request, session):
    pass

def on_launch(request, session):
    pass

def on_intent(request, session):

    intent = request['intent']
    intent_name = request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TheButton":
        return handle_the_button(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_ended()
    else:
        raise ValueError("Invalid intent")

# ---------------------------- Handlers ------------------------------------
def handle_demo():
    call_particle_function("remoteCntl", "demo")
    stmt = "Thank you! No need for applause."
    return stmt

def handle_deploy():
    success = call_particle_function("remoteCntl", "deploy")
    if (success):
        stmt = "Deployment successful."
    else:
        stmt = "Deployment failed."

    return stmt

def handle_the_button(intent, session):
    card_title = intent['name']

    action = intent['slots']['action']['value']

    speech_output = ""
    if action == "demo":
        speech_output = handle_demo()
    elif action == "deploy":
        speech_output = handle_deploy()
    else:
        speech_output = "The Button does not know how to " + str(action)

    return build_response(
        None,
        build_speechlet_response(card_title, speech_output, "", True)
    )


def handle_help():
    print("handle_help")

def handle_session_ended():
    card_title = "Session Ended"
    speech_output = "Thanks for using The Button"
    speechlet_response = build_speechlet_response(card_title, speech_output, None, True)

    return build_response({}, speechlet_response)


# ------------------------------ Lambda Main -----------------------------------
def the_button_handler(event, context):

    if (event['session']['application']['applicationId'] != secrets.APPLICATION_ID):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started(event['request'], event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
