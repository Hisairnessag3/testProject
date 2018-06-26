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


from flask import Flask,escape
from flask import copy_current_request_context
import socketio
from flask_cors import CORS
from socketio import namespace
from decimal import Decimal
from tinydb import TinyDB, Query



class Object(object):
    def __init__(self):
        self.sid = None
        self.balance = 10000
        self.btc = 0
        self.xrp = 0
        self.eth = 0
        self.ltc = 0


db = TinyDB('db.json')
db.insert({'type': 'apple', 'count': 7})
#print(db.all())
Q = Query()



def num(a):
    b = format(Decimal(str(a)).normalize(), 'f')
    print (a,"->",b)

def format(a):
    a =  '{0:.10f}'.format(a)
    return a


sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTXXS'
app.config['SESSION_TYPE'] = 'filesystem'
cors = CORS(app)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
#sess = Session(app)
BITTREX = ccxt.bittrex()
print(BITTREX.balance)
BTC = BITTREX.fetch_ticker("BTC/USDT")['last']
ETH = BITTREX.fetch_ticker("ETH/USDT")['last']
LTC = BITTREX.fetch_ticker("LTC/USDT")['last']
XRP = BITTREX.fetch_ticker("XRP/USDT")['last']

btc,eth,ltc,xrp = 0.0,0.0,0.0,0.0



@app.route('/',methods=['GET'])
def hello():
    print(session)
    c = request.json
    print('hello world')
    return 'Hello World!'

@sio.on('connect',namespace='/trade')
def balance(sid,data):
    sio.emit('logs', '10000',broadcast=True,namespace='/trade',room=sid)
    return 'You are not logged in'

@sio.on('prices',namespace='/trade')
def prices(ssid):

    BTC = str(BITTREX.fetch_ticker("BTC/USDT",)['last'])
    ETH = str(BITTREX.fetch_ticker("ETH/USDT")['last'])
    LTC = str(BITTREX.fetch_ticker("LTC/USDT")['last'])
    XRP = str(BITTREX.fetch_ticker("XRP/USDT")['last'])


    sio.emit('prices', [BTC, ETH, LTC,XRP],broadcast=True,namespace='/trade')

@sio.on('cryptos',namespace='/trade')
def crypto_balance(sid,DATA):
    username = str(DATA)
    query = db.search(Q.username == username)
    try:
        sio.emit('crypto_balance', [str(query[0]['btc']), str(query[0]['eth']), str(query[0]['ltc']), str(query[0]['xrp'])],
             broadcast=True,namespace='/trade',room=sid)
    except:
        sio.emit('crypto_balance', ["0", "0", "0", "0"], broadcast=True,namespace='/trade',room=sid)


@sio.on('buy',namespace='/trade')
def buy(sid,DATA):
    username = str(DATA['USERNAME'])
    query = db.search(Q.username == username)
    Balance = (float(query[0]['balance']))
    usd = float(DATA['AMOUNT'])

    if Balance > usd and Balance != 0:
        print(sid,DATA)
        currency = str(DATA['CURRENCY'])
        crypto = currency + '/USDT'
        price = BITTREX.fetch_ticker(crypto)
        price = price['last']
        Balance = Balance-usd
        btc_balance = (float(query[0]['BTC']))
        eth_balance = (float(query[0]['ETH']))
        ltc_balance = (float(query[0]['LTC']))
        xrp_balance = (float(query[0]['XRP']))
        amount =  usd/price
        if currency == 'BTC':
           btc_balance += amount
           sio.emit('logs', str(Balance),broadcast=True, namespace='/trade')
           sio.emit('crypto_balance', [str(btc_balance), str(eth_balance), str(ltc_balance), str(xrp_balance)],
                    broadcast=True, namespace='/trade',room=sid)
        elif currency == 'ETH':
            eth_balance += amount
            sio.emit('logs', str(Balance), broadcast=True, namespace='/trade')
            sio.emit('crypto_balance',[str(btc_balance),str(eth_balance),str(ltc_balance),str(xrp_balance) ],broadcast=True,namespace='/trade',room=sid)

        elif currency== 'LTC':
            ltc_balance += amount
            sio.emit('logs', str(Balance), broadcast=True, namespace='/trade',room=sid)
            sio.emit('crypto_balance',[str(btc_balance),str(eth_balance),str(ltc_balance),str(xrp_balance) ],broadcast=True,namespace='/trade',room=sid)

        else:
            xrp_balance += amount
            sio.emit('logs', str(Balance), broadcast=True, namespace='/trade',room=sid)
            sio.emit('crypto_balance',[str(btc_balance),str(eth_balance),str(ltc_balance),str(xrp_balance) ],broadcast=True,namespace='/trade',room=sid)

        for q in query:
            q['balance'] = Balance
            q['BTC'] = btc_balance
            q['ETH'] = eth_balance
            q['LTC'] = ltc_balance
            q['XRP'] = xrp_balance
            db.write_back(query)


def sell_actions(currency,crypto_amount,session,sid,username):
    crypto = currency + '/USDT'
    price = BITTREX.fetch_ticker(crypto)
    price = price['last']
    query = db.search(Q.username == username)
    amount = crypto_amount*price
    BALANCE = session['balance'] + amount
    if currency == 'BTC':
        session['BTC'] -= crypto_amount
    elif currency == 'ETH':
        session['ETH'] -= crypto_amount
    elif currency == 'LTC':
        session['LTC'] -= crypto_amount
    else:
        session['XRP'] -= crypto_amount
    sio.emit('balance', str(BALANCE), broadcast=True, namespace='/trade',room=sid)
    sio.emit('crypto_balance', [str(session['BTC']),str(session['ETH']),str(session['LTC']),str(session['XRP'])], broadcast=True, namespace='/trade',room=sid)
    for q in query:
        q['balance'] = BALANCE
        q['BTC'] = session['BTC']
        q['ETH'] = session['ETH']
        q['LTC'] = session['LTC']
        q['XRP'] = session['XRP']
        db.write_back(query)

@sio.on('sell',namespace='/trade')
def sell(sid,DATA):
    crypto_amount = float(DATA['AMOUNT'])
    currency = str(DATA['CURRENCY'])
    username =str(DATA['USERNAME'])
    query = db.search(Q.username == username)
    Balance = (float(query[0]['balance']))
    btc_balance = (float(query[0]['BTC']))
    eth_balance = (float(query[0]['ETH']))
    ltc_balance = (float(query[0]['LTC']))
    xrp_balance = (float(query[0]['XRP']))
    cryptos = {'balance':Balance,'BTC':btc_balance,'ETH':eth_balance,'LTC':ltc_balance,'XRP':xrp_balance}


    if currency == 'BTC' and crypto_amount < btc_balance:
        sell_actions(currency,crypto_amount,cryptos,sid,username)
    else:
        sio.emit('log','Not enough crypto to sell', broadcast=True, namespace='/trade',room=sid)

    if currency == 'ETH' and crypto_amount < eth_balance:
        sell_actions(currency,crypto_amount,cryptos,sid,username)
    else:
        sio.emit('log','Not enough crypto to sell', broadcast=True, namespace='/trade',room=sid)

    if currency == 'LTC' and crypto_amount < ltc_balance:
        sell_actions(currency,crypto_amount,cryptos,sid,username)
    else:
        sio.emit('log','Not enough crypto to sell', broadcast=True, namespace='/trade',room=sid)

    if currency == 'XRP' and crypto_amount < xrp_balance:
        sell_actions(currency,crypto_amount,cryptos,sid,username)
    else:
        sio.emit('log','Not enough crypto to sell', broadcast=True, namespace='/trade',room=sid)




@sio.on('login',namespace='/trade')
def login(sid,DATA):
    username = DATA['username']
    password = DATA['password']
    query = db.search(Q.username == username and Q.password == password)
    try:
        if query[0]:
            Balance = str(float(query[0]['balance']))
            btc_balance = str(float(query[0]['BTC']))
            eth_balance= str(float(query[0]['ETH']))
            ltc_balance = str(float(query[0]['LTC']))
            xrp_balance = str(float(query[0]['XRP']))

            data = [query[0]['username'],query[0]['balance']]
            sio.emit('logs', str(Balance), broadcast=True,namespace='/trade',room=sid)
            sio.emit('crypto_balance',[btc_balance,eth_balance,ltc_balance,xrp_balance], broadcast=True,namespace='/trade',room=sid)
            sio.emit('loginreturn','true', broadcast=True,namespace='/trade',room=sid)
    except:
        session['balance'] = 10000
        sio.emit('log','Invalid Credentials', broadcast=True, namespace='/trade', room=sid)


@sio.on('signup',namespace="/trade")
def signup(sid,DATA):
    username = DATA['username']
    password = DATA['password']
    if username != '' or None and password != '' or None:
        query = db.search(Q.username == username and Q.password == password)

        if query:
            sio.emit('signupreturn','Already Exists', broadcast=True,namespace='/trade',room=sid)
        else:
            db.insert({'username':username,'password':password,'balance':10000,'BTC':0.0,'ETH':0.0,'LTC':0.0,'XRP':0.0,'sid':sid})
            BALANCE,ETHER,BITCOIN,LITE,RIPPLE = "10000","0","0",'0','0'
            sio.emit('logs', BALANCE,broadcast=True,namespace='/trade',room=sid)

            sio.emit('crypto_balance', [ETHER,BITCOIN,LITE,RIPPLE],broadcast=True,namespace='/trade',room=sid)
            sio.emit('signupreturn','true', broadcast=True,namespace='/trade',room=sid)



if __name__ == '__main__':
    app.run(port=5000,threaded=True)
    sess.init_app(app)
