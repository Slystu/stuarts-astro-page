# Imports required to run the web app
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import datetime
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Users, Items
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, flash, jsonify
import requests
	
def application():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    output = "The current session state is %s" % state

    print output

application()
