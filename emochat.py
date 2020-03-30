#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import ToneAnalyzer

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print ('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    if 'message' in msg.keys():
        msg_emo = msg['message']
        emotion = tone_analyze.analyze_tone(msg_emo)
        if emotion == ':|':
            emotion = '&#128528;'
        elif emotion == ':)':
            emotion = '&#128512;'
        else:
            emotion = '&#128577;'
        msg['emotion'] = emotion

    socketio.emit('my response', msg, callback=messageReceived)


# Sample run

def sample_API_call():
	print("sample API call")
	sample_text = 'I am happy. Being good is awesome.'
	sample_text = tone_analyze.analyze_tone(sample_text)
	print ('sample_call --->', sample_text)


# Declaration and Initialization

tone_analyze = ToneAnalyzer.ToneAnalyzer()
sample_API_call()

if __name__ == '__main__':
    socketio.run(app, debug = True)
