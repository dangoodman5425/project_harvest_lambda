import requests
import os

GEOLOCODE_URL = os.getenv("GEOLOCODE_URL")
GEOLOCODE_API_KEY = os.getenv("GEOLOCODE_API_KEY")


def lambda_handler(event, context):
    url = "{base_url}?address={address}&key={api_key}".format(base_url=GEOLOCODE_URL, address=event["address"],
                                                              api_key=GEOLOCODE_API_KEY)
    res = requests.get(url).json()
    if res.status_code == 200:
        return res
    return {"Error": "Request failed"}
