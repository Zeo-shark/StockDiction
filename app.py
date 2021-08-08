import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from predictStocks import predictStocks
from twitter_analyze import twitter_analyze
from yahoo_finance import Share
from datetime import datetime, timedelta
import requests
# import mysql.connector

app = Flask(__name__)

# cnx = mysql.connector.connect(user=os.environ['JW_USERNAME'], password=os.environ['JW_KEY'], host=os.environ['JW_HOST'], database='xcqk05aruwtw0kew')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print(r)
    return r

def processRequest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    stock_symbol = parameters.get("stock_symbol")

    # logMessage(req)

    if req.get("result").get("action") == "CurrentPrice.price":   
        res = makeWebhookResult(getStockCurrentPrice(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "Prediction.stockForecast":
        res = makeWebhookResult(getStockPrediction(req), req, stock_symbol)
        return res 
    elif req.get("result").get("action") == "Feelings.analyze":
        res = makeWebhookResult(getTwitterFeelings(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "DividendDate.Date":
        res = makeWebhookResult(getStockDividendPayDate(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "Stock.info":
        res = makeWebhookResult(getStockInfo(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "Stock.historical":
        res = makeWebhookResult(getHistoricalData(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "Decision.Classification":
        res = makeWebhookResult(getStockClassification(req), req, stock_symbol)
        return res 
    elif req.get("result").get("action") == "input.welcome":
        res = makeWebhookResult(getWelcome(req), req, stock_symbol)
        return res
    elif req.get("result").get("action") == "Visualize.chart":
        res = makeWebhookResult(getChartURL(req), req, stock_symbol)
        return res
    else:
        return {}

def getChartURL(req):
    result = req.get("result")
    parameters = result.get("parameters")
    stock_symbol = parameters.get("stock_symbol")
    chart_url = "https://www.etoro.com/markets/" + stock_symbol + "/chart"
    return chart_url

def logMessage(req):
    print("LOGGING!")
    originalRequest = req.get("originalRequest")
    source = ''

    if originalRequest != None:
        source = originalRequest.get("source")

    if source != 'facebook':
        print("not from facebook")
        return 

    data = originalRequest.get("data")
    time_stamp = data.get("timestamp")
    sender_id = data.get("sender").get("id")
    # recipient_id = data.get("recipient").get("id")
    message = data.get("message")
    text = message.get("text")

    # log incoming messagesw
    response = requests.post("http://api.botimize.io/messages?apikey=ZG2H9YHCZJQS9JTOTXXHL842QDGK5VHI", data={
      "platform": "facebook",
      "direction": "incoming",
      "raw": {
          "object":"page",
          "entry":[
            {
              "id":"986319728104533",
              "time":1458692752478,
              "messaging":[
                {
                  "sender":{
                    "id":sender_id
                  },
                  "recipient":{
                    "id":"986319728104533"
                  }
                }
              ]
            }
          ]
      }
    })
    print(response)
    print(response.content)
    print("Success")


def getWelcome(req):
    response = 'Hi! I am here to help predict financial markets. My predictions are not 100% accurate!'
    return response

# analyze feelings intent