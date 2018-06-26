import backtrader as bt
from datetime import datetime, timedelta
import ccxt
from flask import jsonify
import time
import math
import threading
from flask_restful import Resource, reqparse, abort,request,Api,fields
import json

from flask import jsonify,after_this_request,session
from flask_cors import CORS
import tempfile
import os

#from flask_session import Session

from flask import Flask,escape
from flask import copy_current_request_context,g
import flask_restful as restful
from flask_cors import CORS
from decimal import Decimal
from tinydb import TinyDB, Query
from flask_session import Session
from flask_login import LoginManager,login_user,UserMixin,login_required
from socketio import Server
class Object(object):
    def __init__(self):
        self.balance = 10000
        self.btc = 0
        self.xrp = 0
        self.eth = 0
        self.ltc = 0


db = TinyDB('db.json')
db.insert({'type': 'apple', 'count': 7})
#print(db.all())
Q = Query()

class User(UserMixin):
    def __init__(self,name,password):
        self.id = name
        self.password = password
        self.balance = 10000
        self.btc = 0
        self.eth =0
        self.ltc = 0

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

def num(a):
    b = format(Decimal(str(a)).normalize(), 'f')
    print (a,"->",b)

def format(a):
    a =  '{0:.10f}'.format(a)
    return a




app = Flask(__name__)
sio =  Server(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTXXS'
cors = CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session(app)
login_manager = LoginManager()
login_manager.init_app(app)



BITTREX = ccxt.bittrex()
print(BITTREX.balance)
BTC = BITTREX.fetch_ticker("BTC/USDT")['last']
ETH = BITTREX.fetch_ticker("ETH/USDT")['last']
LTC = BITTREX.fetch_ticker("LTC/USDT")['last']
XRP = BITTREX.fetch_ticker("XRP/USDT")['last']

btc,eth,ltc,xrp = 0.0,0.0,0.0,0.0





@app.route('/',methods=['GET','POST'])
def hello():
    print(session)
    c = request.json
    print('hello world')
    return 'Hello World!'

@sio.on('connect',namespace="/trade")
def balance():
    print(session)
    try:


        emit('logs', "0", broadcast=True)
    except:
        emit('logs', "N/A (Please Login or Signup to Use)",broadcast=True)
        return 'You are not logged in'

@sio.on('prices',namespace="/trade")
def prices():
    print(BTC)
    emit('prices',[str(BTC),str(ETH),str(LTC),str(XRP)],broadcast=True)

@sio.on('cryptos',namespace="/trade")
def crypto_balance():
    try:
        print('something')
        emit('crypto_balance',[str(session['btc']),str(session['eth']),str(session['ltc']),str(session['xrp'])],broadcast=True)
    except:
        print('something else')
        emit('crypto_balance',["0","0","0","0"],broadcast=True)

@sio.on('buy',namespace="/trade")
def buy(DATA):
    print(session)
    print(DATA)
    session['balance'], session['eth'], session['btc'], session['ltc'], session['xrp'] = 10000, 0, 0, 0, 0
    usd = float(DATA['AMOUNT'])
    if session['balance']> 0 and session['balance']>usd:
        currency = str(DATA['CURRENCY'])
        crypto = currency + '/USDT'
        price = BITTREX.fetch_ticker(crypto)
        price = price['last']

        session['balance'] = session['balance'] - usd
        amount =  usd/price
        if currency == 'BTC':
            session['btc'] += amount
        elif currency == 'ETH':
            session['eth'] += amount
        elif currency== 'LTC':
            session['ltc'] += amount
        else:
            session['xrp'] += amount

        emit('balance', str(session['balance']),broadcast=True)
        emit('crypto_balance',[str(session['btc']),str(session['eth']),str(session['ltc']),str(session['xrp'])],broadcast=True)
    else:
        emit('log','Not enough funds')
        return


def sell_actions(currency,crypto_amount,session):
    crypto = currency + '/USDT'
    price = BITTREX.fetch_ticker(crypto)
    price = price['last']

    amount = crypto_amount*price
    BALANCE = session['balance'] + amount
    if currency == 'BTC':
        session['btc'] -= crypto_amount
    elif currency == 'ETH':
        session['eth'] -= crypto_amount
    elif currency == 'LTC':
        session['ltc'] -= crypto_amount
    else:
        session['xrp'] -= crypto_amount
    emit('balance', session['balance'], broadcast=True)
    emit('crypto_balance', [session['btc'],session['eth'],session['ltc'],session['xrp']])


@sio.on('sell',namespace='/trade')
@login_required
def sell(DATA):
    crypto_amount = float(DATA['AMOUNT'])
    currency = str(DATA['CURRENCY'])
    if currency == 'BTC' and crypto_amount < btc:
        sell_actions(currency,crypto_amount,session)
    else:
        emit('log','Not enough crypto to sell')

    if currency == 'ETH' and crypto_amount <eth:
        sell_actions(currency,crypto_amount,session)
    else:
        emit('log','Not enough crypto to sell')

    if currency == 'LTC' and crypto_amount <ltc:
        sell_actions(currency,crypto_amount,session)
    else:
        emit('log','Not enough crypto to sell')

    if currency == 'XRP' and crypto_amount < xrp:
        sell_actions(currency,crypto_amount,session)
    else:
        emit('log','Not enough crypto to sell')



@login_manager.user_loader
def load_user(user_id,password):
    return User(user_id,password=password)

@app.route('/login',methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    print(username,password)
    query = db.search(Q.username == username and Q.password == password)
    user =  User(db.search(Q.username == username and Q.password == password)[0]['username'],password)
    print(query)
    try:
        if query:


            print (user,'this is user')
            user.authenticated = True
            g.user = user
            login_user(user,remember=True)
            session['balance']  = float(query[0]['balance'])
            session['btc'] = float(query[0]['BTC'])
            session['eth']= float(query[0]['ETH'])
            session['ltc'] = float(query[0]['LTC'])
            session['xrp'] = float(query[0]['XRP'])
            g.user.btc = session['balance']
            g.user.eth = session['eth']
            g.user.ltc = session['ltc']
            session['username'] = username
            data = [query[0]['username'],query[0]['balance']]
            print (session)
            sio.emit('logs', str(query[0]['balance']), broadcast=True)
            sio.emit('crypto_balance', ["1000","0","0","0"],broadcast=True)
            return jsonify('true')
    except:
        import traceback
        print(traceback.print_exc())
        session['balance'] = 10000
        sio.emit('logs', "10000", broadcast=True)

        return jsonify('Invalid credentials')



@app.route('/signup',methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    if username != '' or None and password != '' or None:
        print(username,password)
        query = db.search(Q.username == username and Q.password == password)

        if query:
            return jsonify('Already Exists')
        else:
            import random
            db.insert({'username':username,'password':password,'balance':10000,'BTC':0.0,'ETH':0.0,'LTC':0.0,'XRP':0.0})
            session['balance'],session['eth'],session['btc'],session['ltc'],session['xrp'] = 10000,0,0,0,0
            emit('crypto_balance', [session['btc'], session['eth'], session['ltc'], session['xrp']])
            return jsonify('true')




if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTXXS'
    app.run(port=5000,debug=True)
    sess.init_app(app)
