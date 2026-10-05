
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np

app = FastAPI()

df = pd.read_csv("skin clinic campaign.csv")

df["Response"] = df["Response_to_Campaign"].map({
    "Yes": 1,
    "No": 0
})

df["Product_Usage"] = pd.cut(
    df["Unique_Products_Purchased"],
    bins=[0, 4, 8, np.inf],
    labels=["1-4", "5-8", ">8"]
)

@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():

    gender_response = (
        df.groupby("Gender")["Response"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    gender_response.columns = [
        "Gender",
        "Response Rate (%)"
    ]

    return gender_response.to_html(index=False)
