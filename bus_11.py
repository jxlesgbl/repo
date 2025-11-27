from flask import Flask, jsonify
import pandas as pd

URL = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv"

app = Flask(__name__)

@app.get("/eta")
def eta():
    df = pd.read_csv(URL, sep=";")
    df['delay_min'] = (df['delay_sec'] / 60).round()
    f = df[
        (df["route_short_name"] == "11")
        & (df["direction_id"] == 1)
        & (df["stop_name"] == "SAPORTA")
    ].sort_values("delay_min", ascending=True)

    val = f.iloc[0]["delay_min"]
    return jsonify({"eta": val})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5500))
    app.run(host="0.0.0.0", port=port)
