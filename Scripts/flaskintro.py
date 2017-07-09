'''
flaskintro.py

I want to eventually make all of the Albion data available online.
Flask seems like a cool way to do that, so here is a script for
playing around with it!

'''

from flask import Flask
import parsetest
APP = Flask(__name__)

@APP.route('/')
def hello_world():
    ''' First steps into Flask '''
    return parsetest.test_run()
