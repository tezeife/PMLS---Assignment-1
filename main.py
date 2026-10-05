
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np

app = FastAPI()
@app.get("/")
def home():
    return {
        "message": "Skin Clinic Campaign Analysis API",
        "endpoint": "/campaign-analysis"
    }

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

    # Gender response
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

    # Age group response
    age_response = (
        df.groupby("AgeGroup")["Response"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    age_response.columns = [
        "Age Group",
        "Response Rate (%)"
    ]

    # Purchase in last quarter response
    purchase_response = (
        df.groupby("Purchase_Last_Quarter")["Response"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    purchase_response.columns = [
        "Purchased Last Quarter",
        "Response Rate (%)"
    ]

    # Product usage response
    product_response = (
        df.groupby(
            "Product_Usage",
            observed=False
        )["Response"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    product_response.columns = [
        "Product Usage",
        "Response Rate (%)"
    ]

    html = f"""
    <html>
    <body>

        <h1>Skin Clinic Campaign Analysis</h1>

        <h2>Gender vs Campaign Response</h2>
        {gender_response.to_html(index=False)}

        <h2>Age Group vs Campaign Response</h2>
        {age_response.to_html(index=False)}

        <h2>Purchase in Last Quarter vs Campaign Response</h2>
        {purchase_response.to_html(index=False)}

        <h2>Product Usage vs Campaign Response</h2>
        {product_response.to_html(index=False)}

    </body>
    </html>
    """

    return html
