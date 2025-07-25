from pydoc import replace

DEFAULT_PASSWORD = ""
WEBSIDE = "https://boris5.test.unibe.ch"

from pprint import pprint
import os
import sys
import requests

from dotenv import load_dotenv

load_dotenv()


from dspace_rest_client.client import DSpaceClient , logging
logging.disable(logging.WARNING)


DEFAULT_URL = f'{WEBSIDE}/server/api'
DEFAULT_USERNAME = '8fee9c6e.unibe365.onmicrosoft.com@ch.teams.ms'

# Configuration from environment variables
URL = os.environ.get('DSPACE_API_ENDPOINT', DEFAULT_URL)
USERNAME = os.environ.get('DSPACE_API_USERNAME', DEFAULT_USERNAME)
PASSWORD = os.environ.get('DSPACE_API_PASSWORD', DEFAULT_PASSWORD)

client = DSpaceClient(api_endpoint=URL, username=USERNAME, password=PASSWORD, fake_user_agent=True)

# Authenticate against the DSpace client
authenticated = client.authenticate()

if not authenticated:
    print('Error logging in! Giving up.')
    sys.exit(1)


def getFiles(id):
    url = f"{WEBSIDE}/server/api/core/edititems/{id}:FULL"
    response = client.api_get(url)
    data = response.json()

    print(data)
    try:
        files = data["sections"]["upload_publication"]["files"]
    except KeyError:
        return None

    return files


def setAcces(id, file_index, accesValue):
    r = client.api_patch(
        f"{WEBSIDE}/server/api/core/edititems/{id}:FULL",
        operation="add",
        path=f"/sections/upload_publication/files/{file_index}/accessConditions",
        value=[{"name": accesValue}])
    return r