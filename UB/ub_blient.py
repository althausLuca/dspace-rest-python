from pydoc import replace


from pprint import pprint
import os
import sys
import requests

from dotenv import load_dotenv

loaded =  load_dotenv(os.path.dirname(os.path.abspath(__file__))+"/.env")


from dspace_rest_client.client import DSpaceClient , logging
logging.disable(logging.WARNING)

# Configuration from environment variables
WEBSIDE = os.environ.get('WEBSIDE', "https://boris4.test.unibe.ch")
URL = f'{WEBSIDE}/server/api'
USERNAME = os.environ.get('DSPACE_API_USERNAME' , "")
PASSWORD = os.environ.get('DSPACE_API_PASSWORD' , "")

WEBSIDE_NAME = replace(WEBSIDE, "https://" , "")
WEBSIDE_NAME = replace(WEBSIDE_NAME, ".unibe.ch" , "")


client = DSpaceClient(api_endpoint=URL, username=USERNAME, password=PASSWORD, fake_user_agent=True)
authenticated = client.authenticate()

if not authenticated:
    TOKEN = os.environ.get('TOKEN')
    client.session.headers.update({"Authorization": f"Bearer {TOKEN}"})
    authenticated = client.authenticate()
    if not authenticated:
        print(f'Error logging in with {USERNAME} or using token')
        # sys.exit(1)
    else:
        print("Token login succeeded")


def getFiles(id):
    url = f"{WEBSIDE}/server/api/core/edititems/{id}:FULL"
    response = client.api_get(url)
    data = response.json()

    url = f"{WEBSIDE}/server/api/core/bitstreams/search/showableByItem?uuid={id}&name=ORIGINAL"

    response = client.api_get(url)

    if response.status_code != 200:
        print(f"ERROR: Could not find bitstreams {id} , id: {response.status_code}")

    data = response.json()
    bitstreams = data.get("_embedded", {}).get("bitstreams", [])
    fileNames = [bitstream["name"] for bitstream in bitstreams]
    return fileNames


def setAcces(id, file_index, accesValue):
    r = client.api_patch(
        f"{WEBSIDE}/server/api/core/edititems/{id}:FULL",
        operation="add",
        path=f"/sections/upload_publication/files/{file_index}/accessConditions",
        value=[{"name": accesValue}])
    return r


def deleteBitstream(id):
    url = f"{WEBSIDE}/server/api/core/bitstreams/{id}"
    r = client.api_delete(url, params=None)
    return r

def deleteItem(id):
    url = f"{WEBSIDE}/server/api/core/items/{id}"
    r = client.api_delete(url, params=None)
    return r