import requests
import os


YELP_BASE_URL = os.getenv("YELP_BASE_URL")
YELP_API_KEY = os.getenv("YELP_API_KEY")
DM_BASE_URL = os.getenv("DM_BASE_URL")
DM_API_KEY = os.getenv("DM_API_KEY")


def lambda_handler(event, context):
    latitude = event.get("latitude")
    longitude = event.get("longitude")
    origins = event.get("origins")
    limit = event.get("limit", 10)
    radius = event.get("radius", None)
    res = yelp_businesses(latitude, longitude, limit, radius)
    businesses = res.json()["businesses"]
    dests, biz_names = [], []
    for b in businesses:
        dests.append([str(b["coordinates"]["latitude"]), str(b["coordinates"]["longitude"])])
        biz_names.append(b["name"])
    res = distance_matrix(origins, dests)
    return res.json()


def yelp_businesses(latitude, longitude, limit, radius):
    url = "{base_url}?latitude={latitude}&longitude={longitude}&limit={limit}".format(
        base_url=YELP_BASE_URL, latitude=latitude, longitude=longitude, limit=limit)
    if radius:
        url += "&radius={radius}".format(radius=radius)
    res = requests.get(url, headers={"Authorization": "Bearer {access_token}".format(access_token=YELP_API_KEY)})
    return res


def format_coords(coords):
    return "|".join([",".join(coord) for coord in coords])


def format_places(places):
    return "place_id:" + "|place_id:".join(places)


def format_polylines(polylines):
    return "enc:" + ":|enc:".join(polylines) + ":"


def format_addresses(addresses):
    return "|".join(addresses)


def distance_matrix(origins, dests, origin_type="coords", dest_type="coords", arr_t=None, modes=None):
    loc_type_map = {"coords": format_coords, "places": format_places, "polylines": format_polylines,
                    "addresses": format_addresses}
    origins = loc_type_map[origin_type](origins)
    dests = loc_type_map[dest_type](dests)
    url = "{base_url}?origins={origins}&destinations={dests}".format(base_url=DM_BASE_URL, origins=origins,
                                                                     dests=dests)
    if arr_t:
        url += "&arrival_time={arr_t}".format(arr_t=arr_t)
    if modes:
        url += "&transit_mode={modes}".format(modes="|".format(modes))
    return requests.get(url + "&key={api_key}".format(api_key=DM_API_KEY))


# def parse_matrix(data, dest_names):
#     return pd.DataFrame(data=[[elem["duration"]["text"] for elem in row["elements"]] for row in data["rows"]],
#                         columns=dest_names, index=data["origin_addresses"])
