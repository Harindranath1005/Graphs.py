import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
default_value = "Wuhqfb3Nva5GVFEMXxJVeussQ8gfU9CRA6ZADTw3Bsj"
x=st.text_input("Enter some text:", default_value)
st.write(x)
url = "https://mainnet.helius-rpc.com/?api-key=5e01c746-318d-4ad9-956f-636b873079d2"

def get_assets_with_native_balance():
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": x,
            "displayOptions": {
                "showFungible": True,
                "showNativeBalance": True
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    result = response.json().get("result", {})
    return result['items']

output = get_assets_with_native_balance()

c=0
r_l={}
def return_data_from_dic(output):
  #symbol, balance, price_per_token, total_price, currency
  #{'symbol' : ‘PYTH', ‘balance’: 34143707, ‘price_per_token': 0.428636,    'total_price': 14.63522248742181,  'currency': 'USDC’}
  if output["interface"]=="V1_NFT":
    return {}
  l=output.get("token_info")
  r_l={"symbol":[],
       "balance":[],
       "price_per_token":[],
       "total_price":[],
       "currency":[]
       }
  r_l["symbol"].append(l.get("symbol"))
  r_l["balance"].append(l.get("balance"))
  r_l["price_per_token"].append(l.get("price_info").get("total_price"))
  r_l["total_price"].append(l.get("price_info").get("total_price"))
  r_l["currency"].append(l.get("price_info").get("currency"))
  return r_l

c=0
l={}
df=pd.DataFrame()
for data in output:
  if data["interface"]=="FungibleToken":
    l=return_data_from_dic(data)
    new_row=pd.DataFrame(l)
    df=pd.concat([df,new_row], ignore_index=True)

df["prercentage"]=((df['total_price']/df['total_price'].sum())*100)
df["cumulative_sum_percentage"]=np.round(df["prercentage"].cumsum(),2)
print(df["prercentage"].sum())
#l1=df[df["cumulative_sum_percentage"]>95].tolist()
#l1=df[df["cumulative_sum_percentage"]>95]
l1=df["cumulative_sum_percentage"].values.tolist()
l2=[]
for x in l1:
    if x<95 and x>7:
      l2.append(x)
print(l2)
st.header("Data Frame")
fig=px.pie(df,values='prercentage',names='symbol')
st.write(fig)
st.dataframe(df)
