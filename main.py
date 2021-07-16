"""
This script "honks" a stock in the virtual New Vooperis Stock Exchange (NVSE). "Honking" refers to the process of aggressively buying stocks until the owner gets 50% or more of the company ownership worth of stocks.

This is the intellectual property of Danish. Use wisely and don't be dumb.
"""

import requests
import json
import sseclient
import sys
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://nvse.vtech.cf/Api/"
stream = "https://nvse.vtech.cf/stream"
client = sseclient.SSEClient(stream)
apikey = os.getenv('apikey')
svid = os.getenv('svid')

try:
  for event in client:
    data = json.loads(event.data)
    print(data)
    event = data['event']

    if event == "other" or event == "ClassicalStockEvent":
      if event == "ClassicalStockEvent":
        if(data['data']['owner'] != "u-c60c6bd8-0409-4cbd-8bb8-3c87e24c55f8"):
          
        #for issuing stock, stock splits, depositing, withdriawing

          available = data['data']['available']
          shares = data['data']['shares']
          ticker = data['data']['ticker']

          link_1 = f"{base_url}/Classical/GetSharesOwned?accountid={svid}&ticker={ticker}"

          my_own = requests.get(link_1).text
          print(my_own)
          print(f"I own: {my_own}")

          if available != 0:
            if (available + int(my_own)) >= 0.45*shares or shares <= 15:
              link_2 = f"{base_url}/Classical/BuySecurity?accountid={svid}&apikey={apikey}&ticker={ticker}&amount={available}"
              print(link_2)
              requests.get(link_2).text
              print("YOU HAVE BEEN HONKED")
      else:
          available = data['data']['available']
          shares = data['data']['shares']
          ticker = data['data']['ticker']

          link_1 = f"{base_url}/Classical/GetSharesOwned?accountid={svid}&ticker={ticker}"

          my_own = requests.get(link_1).text
          print(my_own)
          print(f"I own: {my_own}")

          if available != 0:
            if (available + int(my_own)) >= shares/2 or shares <= 15:
              link_2 = f"{base_url}/Classical/BuySecurity?accountid={svid}&apikey={apikey}&ticker={ticker}&amount={available}"
              print(link_2)
              requests.get(link_2).text
              print("YOU HAVE BEEN HONKED")

except Exception as e:
  print(e)
  sys.stdout.flush()