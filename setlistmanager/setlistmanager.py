#!/usr/bin/env python3
from flask import Flask
from setlistmanager import *
app = Flask('setlistmanager')
app.env = 'development'
app.run(debug=True)