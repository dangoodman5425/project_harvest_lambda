import requests
import os


YELP_BASE_URL = os.getenv("YELP_BASE_URL")
YELP_API_KEY = os.getenv("YELP_API_KEY")


def lambda_handler(event, context):
    latitude = event.get("latitude")
    longitude = event.get("longitude")
    limit = event.get("limit", 10)
    radius = event.get("radius", None)
    url = "{base_url}?latitude={latitude}&longitude={longitude}&limit={limit}".format(
        base_url=YELP_BASE_URL, latitude=latitude, longitude=longitude, limit=limit)
    if radius:
        url += "&radius={radius}".format(radius=radius)
    return requests.get(url, headers={"Authorization": "Bearer {access_token}".format(access_token=YELP_API_KEY)}).json()

