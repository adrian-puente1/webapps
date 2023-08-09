import time
import pandas as pd
import urllib.parse
import requests
import urllib.parse
import pathlib
import uuid
import plotly.express as px
from decouple import config

def translate_addresses_to_coordinates(new_addresses:list[str], filepath:str, addresses:dict[str]=[], 
                                       geocode_auth:str=str(config('GEOCODE_AUTH'))):
    for idx,address in enumerate(new_addresses):
        params = urllib.parse.urlencode({
            'auth': geocode_auth,
            'locate': address,
            'region': 'Japan',
            'json': 1,
            })

        response = requests.get("https://geocode.xyz", params=params)

        #TODO add logic based on API response? needs verification
        addresses.append({
            "latitude": response.json()['latt'],
            "longitude": response.json()['longt'],
            "country": response.json()['standard']['countryname'],
            "city": response.json()['standard']['city'],
            "street": response.json()['standard']['addresst'],
        })
        print(f"{idx+1} ingested - {address}")
        time.sleep(1) # added because I'm using geocode.xyz for free
    df = pd.DataFrame(data=addresses)
    df.to_csv(f"{filepath}.csv", index_label='index')

def addresses_as_html(filepath:str):
    df = pd.read_csv(f"{filepath}.csv")
    #TODO digest latitude + longitude to determine radius, center, and zoom used
    fig = px.density_mapbox(df, lat=df['latitude'], lon=df['longitude'], radius=20, 
                            center=dict(lat=35.65464,lon=139.75417), 
                            zoom=8, mapbox_style='stamen-terrain')
    fig.write_html(f"{filepath}.html", full_html=False)

def destination_heatmap_wrapper(**kwargs):
    filepath = f"files/{str(uuid.uuid4())}"
    pathlib.Path(filepath[::-1].split('/',1)[-1][::-1]).mkdir(parents=True, exist_ok=True)
    addresses = [
        'Japan, 〒105-0012 Tokyo, Minato City, Shibadaimon, 2 Chome−3−1 常泉ビル １Ｆ',
        '2 Chome-13-8 Kichijoji Minamicho, Musashino, Tokyo 180-0003, Japan'
    ]

    #TODO use kwargs in logic to determine functions used
    translate_addresses_to_coordinates(addresses,filepath)
    addresses_as_html(filepath)

if __name__ == "__main__":
    destination_heatmap_wrapper()


#TODO preserve uuid with some kind of {id:str="japan_trip", uuid:"uuid is here"} so that it can be fetched on-demand. 
# MongoDB: https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application

