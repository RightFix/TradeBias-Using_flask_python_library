import time
from flask import Flask, render_template, redirect, url_for
import pandas as pd
from assets.Bias import BiasClass

app = Flask(__name__)

@app.route("/")
def index():
    file_name = "dataset/bias_record.csv"
    df = pd.read_csv(file_name).drop_duplicates()
    data_table = df.to_dict(orient="list")
    zip_data = zip(data_table["Crypto_Currency"], data_table["Strength"], data_table["Trade_Condition"], data_table["Time"])
    return render_template("index.html",data = data_table, zip_data = zip_data)

@app.route("/button_action", methods= ["POST"])
def button_action():
    file_name = "dataset/bias_record.csv"
    df = pd.read_csv(file_name).drop_duplicates()
    # Prepare new data
    data = {
        "Crypto_Currency": [],
        "Strength": [],
        "Trade_Condition": [],
        "Time":[],
    }

    # Coins and Bias class
    coins = sorted(["ETHUSDT", "AAVEUSDT", "SOLUSDT", "COMPUSDT", "BNBUSDT", "BTCUSDT", "BCHUSDT", "XRPUSDT", "LTCUSDT","XMRUSDT","DOGEUSDT","XLMUSDT"])
    BC = BiasClass(coins)
    
    for i in range(len(coins)):
    
        formatted_time = time.strftime("%H:%M %d/%m/%Y",  time.localtime())
    
        Strength = BC.bias_count(i)
        if Strength > 0:
            trade_condition = "Strong Buy" if Strength > 100 else "Weak Buy"
        elif Strength < 0:
            trade_condition = "Strong sell" if Strength < -100 else "Weak Sell"
        else:
            trade_condition = "Not Available"
            
        data["Crypto_Currency"].append(coins[i])
        data["Strength"].append(Strength)
        data["Trade_Condition"].append(trade_condition)
        data["Time"].append(formatted_time)

    # Merge with old data
    data_table = data
    data = pd.DataFrame(data)
    df = pd.concat([data, df], ignore_index=True).drop_duplicates()
    
    # Save locally
    df.to_csv(file_name, index=False)
    return redirect(url_for("index"))
    
# Run the app if the script is executed directly

app.run(debug=False)

